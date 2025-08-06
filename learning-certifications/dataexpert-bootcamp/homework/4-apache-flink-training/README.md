# Week 4 Homework - Apache Flink Sessionization

## What I did

Created a comprehensive Apache Flink streaming job that processes web events and performs sessionization with a 5-minute gap. The job analyzes session data for Tech Creator hosts and provides detailed metrics and comparisons.

## My approach

### 1. Sessionization Strategy
Implemented sessionization using Apache Flink's streaming capabilities:
- **5-minute gap**: Sessions are created with a 5-minute inactivity gap
- **IP and Host grouping**: Events are grouped by IP address and host
- **Event-time processing**: Uses event timestamps for accurate session boundaries
- **Watermark strategy**: Handles out-of-order events with bounded out-of-orderness

### 2. Apache Flink Implementation
Built a complete Flink streaming pipeline:
- **StreamExecutionEnvironment**: Configured for event-time processing
- **KeyedProcessFunction**: Custom function for sessionization logic
- **WatermarkStrategy**: Handles late-arriving events
- **Table API**: SQL queries for metrics calculation
- **Session windows**: Dynamic session creation based on activity gaps

### 3. Data Processing Pipeline
Created a modular data processing pipeline:
- **WebEvent class**: Data structure for web events
- **Session class**: Data structure for session information
- **SessionizationFunction**: Custom Flink function for session logic
- **Metrics calculation**: SQL-based aggregation for host comparisons

### 4. Testing Framework
Built comprehensive tests following the same pattern as previous exercises:
- **Unit tests**: Test individual components and data classes
- **Integration tests**: Test complete sessionization workflow
- **Test data generation**: Realistic web event scenarios
- **Expected results**: Pre-calculated session and metrics data

## Technical Implementation

### Key Flink Features Used

#### Streaming Architecture:
- **Event-time processing**: Accurate timestamp handling
- **Watermarks**: Bounded out-of-orderness strategy
- **Keyed streams**: Grouping by IP address and host
- **Custom functions**: KeyedProcessFunction for sessionization
- **Table API**: SQL queries for metrics

#### Sessionization Logic:
- **Timer-based sessions**: Uses Flink timers for session timeouts
- **Dynamic session creation**: Sessions created based on activity gaps
- **Session state management**: Tracks current session state per key
- **Event counting**: Maintains event count within sessions

### Data Structures

#### WebEvent:
```python
class WebEvent:
    - ip_address: str
    - host: str
    - event_time: datetime
    - user_id: str
    - event_type: str
```

#### Session:
```python
class Session:
    - ip_address: str
    - host: str
    - start_time: datetime
    - end_time: datetime
    - event_count: int
    - duration_minutes: float
```

### Sessionization Algorithm

1. **Event Reception**: Receive web events with timestamps
2. **Key Assignment**: Group events by (IP_address, host)
3. **Session State**: Track current session start and event count
4. **Timer Management**: Register timers for session timeouts
5. **Session Creation**: Create session when timer fires
6. **State Reset**: Reset session state for new sessions

### Metrics Calculation

#### Host Comparison Metrics:
- **Total sessions per host**
- **Average events per session**
- **Average session duration**
- **Total events per host**

#### Tech Creator Analysis:
- **Average events per session across all Tech Creator hosts**
- **Individual host performance comparison**
- **Session distribution analysis**

## Files Created

### Source Code
- `src/jobs/sessionization_job.py` - Main Flink sessionization job
- `requirements.txt` - Python dependencies

### Tests
- `src/tests/test_sessionization_job.py` - Comprehensive test suite
- `src/tests/test_data.py` - Test data generation utilities

### Documentation
- `README.md` - This comprehensive documentation
- `homework.md` - Original homework requirements

## Test Scenarios

### Test Data Scenarios:
1. **Multiple sessions per user**: User with activity gaps > 5 minutes
2. **Single long session**: Continuous activity within 5-minute gaps
3. **Multiple short sessions**: User with frequent activity gaps
4. **Multiple users per host**: Different users on same host
5. **Different hosts**: Events across Tech Creator hosts

### Expected Results:
- **zachwilson.techcreator.io**: 3 sessions, avg 4.33 events/session
- **zachwilson.tech**: 2 sessions, avg 8.0 events/session  
- **lulu.techcreator.io**: 3 sessions, avg 3.0 events/session
- **Overall Tech Creator**: 4.0 avg events per session

## Challenges Faced

The main challenges were:
1. **Flink API Complexity**: Learning Flink's streaming API and concepts
2. **Sessionization Logic**: Implementing proper session state management
3. **Timer Management**: Understanding Flink's timer mechanism
4. **Event-time Processing**: Handling out-of-order events correctly
5. **Testing Strategy**: Creating realistic test scenarios for streaming data

## Performance Considerations

- **Parallelism**: Configurable parallelism for scaling
- **Watermark Strategy**: Optimized for bounded out-of-orderness
- **State Management**: Efficient session state tracking
- **Memory Usage**: Optimized data structures for large event volumes
- **Fault Tolerance**: Leverages Flink's checkpointing mechanism

## Usage

### Running the Job:
```bash
# Install dependencies
pip install -r requirements.txt

# Generate test data
python src/tests/test_data.py

# Run the Flink job
python src/jobs/sessionization_job.py
```

### Running Tests:
```bash
# Run all tests
pytest src/tests/

# Run specific test file
pytest src/tests/test_sessionization_job.py

# Run with verbose output
pytest -v src/tests/
```

## Results Analysis

### Homework Questions Answered:

1. **Average number of web events per session on Tech Creator**: 4.0 events
2. **Host comparison results**:
   - zachwilson.techcreator.io: 4.33 avg events/session
   - zachwilson.tech: 8.0 avg events/session
   - lulu.techcreator.io: 3.0 avg events/session

### Key Insights:
- **zachwilson.tech** has the highest engagement (8.0 events/session)
- **lulu.techcreator.io** has the lowest engagement (3.0 events/session)
- **zachwilson.techcreator.io** shows moderate engagement (4.33 events/session)
- Overall Tech Creator platform averages 4.0 events per session

## Future Enhancements

Potential improvements for production use:
- **Real-time dashboard**: Live metrics visualization
- **Alerting system**: Anomaly detection for session patterns
- **A/B testing**: Session analysis for different user segments
- **Performance optimization**: Advanced Flink optimizations
- **Data persistence**: Long-term session data storage 