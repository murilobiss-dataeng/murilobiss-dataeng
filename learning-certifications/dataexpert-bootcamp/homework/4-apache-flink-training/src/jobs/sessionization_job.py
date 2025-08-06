#!/usr/bin/env python3
"""
Week 4 - Apache Flink Sessionization Job
Processes web events and creates sessions with 5-minute gaps
Analyzes session data for Tech Creator hosts
"""

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings
from pyflink.common.time import Time
from pyflink.datastream.connectors import FileSystem, OutputFileConfig
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream.window import EventTimeSessionWindows
from pyflink.datastream.functions import ProcessWindowFunction, RuntimeContext
from pyflink.common import Types
from pyflink.datastream.functions import KeyedProcessFunction
from pyflink.common.watermark_strategy import WatermarkStrategy
from pyflink.common.time import Duration
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebEvent:
    """Data class for web events"""
    def __init__(self, ip_address: str, host: str, event_time: datetime, user_id: str = None, event_type: str = None):
        self.ip_address = ip_address
        self.host = host
        self.event_time = event_time
        self.user_id = user_id
        self.event_type = event_type
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'ip_address': self.ip_address,
            'host': self.host,
            'event_time': self.event_time.isoformat(),
            'user_id': self.user_id,
            'event_type': self.event_type
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WebEvent':
        return cls(
            ip_address=data['ip_address'],
            host=data['host'],
            event_time=datetime.fromisoformat(data['event_time']),
            user_id=data.get('user_id'),
            event_type=data.get('event_type')
        )

class Session:
    """Data class for session information"""
    def __init__(self, ip_address: str, host: str, start_time: datetime, end_time: datetime, event_count: int):
        self.ip_address = ip_address
        self.host = host
        self.start_time = start_time
        self.end_time = end_time
        self.event_count = event_count
        self.duration_minutes = (end_time - start_time).total_seconds() / 60
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'ip_address': self.ip_address,
            'host': self.host,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat(),
            'event_count': self.event_count,
            'duration_minutes': self.duration_minutes
        }

class SessionizationFunction(KeyedProcessFunction):
    """Custom function to handle sessionization logic"""
    
    def __init__(self, session_gap_minutes: int = 5):
        self.session_gap_minutes = session_gap_minutes
        self.session_gap_ms = session_gap_minutes * 60 * 1000
        self.sessions: List[Session] = []
        self.current_session_start = None
        self.current_session_events = 0
        self.timer_registered = False
    
    def open(self, runtime_context: RuntimeContext):
        """Initialize the function"""
        logger.info(f"Initializing sessionization with {self.session_gap_minutes} minute gap")
    
    def process_element(self, value, ctx: 'KeyedProcessFunction.OnTimerContext'):
        """Process each web event"""
        event = WebEvent.from_dict(value)
        current_time = event.event_time.timestamp() * 1000  # Convert to milliseconds
        
        if self.current_session_start is None:
            # Start new session
            self.current_session_start = event.event_time
            self.current_session_events = 1
            self._register_timer(current_time + self.session_gap_ms)
        else:
            # Continue current session
            self.current_session_events += 1
            # Update timer
            self._register_timer(current_time + self.session_gap_ms)
    
    def on_timer(self, timestamp: int, ctx: 'KeyedProcessFunction.OnTimerContext'):
        """Handle session timeout"""
        if self.current_session_start is not None:
            # Create session
            session = Session(
                ip_address=ctx.get_current_key()[0],
                host=ctx.get_current_key()[1],
                start_time=self.current_session_start,
                end_time=datetime.fromtimestamp(timestamp / 1000),
                event_count=self.current_session_events
            )
            self.sessions.append(session)
            
            # Reset session
            self.current_session_start = None
            self.current_session_events = 0
            self.timer_registered = False
    
    def _register_timer(self, timestamp: int):
        """Register timer for session timeout"""
        if not self.timer_registered:
            ctx = self.get_runtime_context()
            ctx.timer_service().register_event_time_timer(timestamp)
            self.timer_registered = True

def create_flink_environment() -> StreamExecutionEnvironment:
    """Create and configure Flink execution environment"""
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)  # Set parallelism for development
    env.set_stream_time_characteristic(TimeCharacteristic.EventTime)
    
    return env

def create_table_environment(env: StreamExecutionEnvironment) -> StreamTableEnvironment:
    """Create and configure Flink Table environment"""
    settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
    table_env = StreamTableEnvironment.create(env, settings)
    
    return table_env

def process_web_events(env: StreamExecutionEnvironment, input_path: str) -> 'DataStream':
    """Process web events from input source"""
    
    # Create watermark strategy
    watermark_strategy = WatermarkStrategy \
        .for_bounded_out_of_orderness(Duration.of_seconds(10)) \
        .with_timestamp_assigner(lambda event, timestamp: 
            datetime.fromisoformat(event['event_time']).timestamp() * 1000)
    
    # Read input stream
    input_stream = env \
        .read_text_file(input_path) \
        .map(lambda line: json.loads(line), output_type=Types.STRING()) \
        .assign_timestamps_and_watermarks(watermark_strategy)
    
    return input_stream

def sessionize_events(input_stream: 'DataStream') -> 'DataStream':
    """Apply sessionization to web events"""
    
    # Key by IP address and host
    keyed_stream = input_stream \
        .key_by(lambda event: (event['ip_address'], event['host']))
    
    # Apply sessionization function
    sessionized_stream = keyed_stream \
        .process(SessionizationFunction(session_gap_minutes=5))
    
    return sessionized_stream

def calculate_session_metrics(sessionized_stream: 'DataStream') -> 'DataStream':
    """Calculate session metrics and statistics"""
    
    # Convert to table for SQL operations
    table_env = StreamTableEnvironment.create(sessionized_stream.get_execution_environment())
    
    # Create temporary view
    sessionized_stream.create_temporary_view("sessions", sessionized_stream)
    
    # Calculate metrics by host
    metrics_query = """
        SELECT 
            host,
            COUNT(*) as total_sessions,
            AVG(event_count) as avg_events_per_session,
            AVG(duration_minutes) as avg_session_duration,
            SUM(event_count) as total_events
        FROM sessions
        WHERE host IN ('zachwilson.techcreator.io', 'zachwilson.tech', 'lulu.techcreator.io')
        GROUP BY host
    """
    
    metrics_table = table_env.sql_query(metrics_query)
    
    return metrics_table.to_data_stream()

def analyze_tech_creator_sessions(sessionized_stream: 'DataStream') -> Dict[str, Any]:
    """Analyze sessions specifically for Tech Creator hosts"""
    
    tech_creator_hosts = ['zachwilson.techcreator.io', 'zachwilson.tech', 'lulu.techcreator.io']
    
    # Filter for Tech Creator hosts
    tech_creator_sessions = sessionized_stream \
        .filter(lambda session: session['host'] in tech_creator_hosts)
    
    # Calculate average events per session for Tech Creator
    total_sessions = 0
    total_events = 0
    
    # This would be implemented with proper aggregation in a real Flink job
    # For now, we'll return a placeholder structure
    return {
        'tech_creator_avg_events_per_session': 0.0,
        'host_comparison': {
            'zachwilson.techcreator.io': {'avg_events': 0.0, 'total_sessions': 0},
            'zachwilson.tech': {'avg_events': 0.0, 'total_sessions': 0},
            'lulu.techcreator.io': {'avg_events': 0.0, 'total_sessions': 0}
        }
    }

def main():
    """Main function to run the Flink sessionization job"""
    
    logger.info("Starting Apache Flink Sessionization Job")
    
    try:
        # Create Flink environment
        env = create_flink_environment()
        table_env = create_table_environment(env)
        
        # Process web events
        input_stream = process_web_events(env, "data/web_events.json")
        
        # Apply sessionization
        sessionized_stream = sessionize_events(input_stream)
        
        # Calculate metrics
        metrics_stream = calculate_session_metrics(sessionized_stream)
        
        # Analyze Tech Creator sessions
        analysis_results = analyze_tech_creator_sessions(sessionized_stream)
        
        # Output results
        sessionized_stream.print("Sessions")
        metrics_stream.print("Metrics")
        
        # Execute the job
        env.execute("Web Event Sessionization Job")
        
        logger.info("Sessionization job completed successfully")
        
        return analysis_results
        
    except Exception as e:
        logger.error(f"Error in sessionization job: {e}")
        raise

if __name__ == "__main__":
    main() 