#!/usr/bin/env python3
"""
Week 4 - Apache Flink Sessionization Job Tests
Tests for the sessionization functionality and metrics calculation
"""

import pytest
import json
import tempfile
import os
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'jobs'))

from sessionization_job import (
    WebEvent, 
    Session, 
    SessionizationFunction,
    create_flink_environment,
    process_web_events,
    sessionize_events,
    calculate_session_metrics,
    analyze_tech_creator_sessions
)

class TestWebEvent:
    """Test WebEvent data class"""
    
    def test_web_event_creation(self):
        """Test creating a WebEvent instance"""
        event_time = datetime.now()
        event = WebEvent(
            ip_address="192.168.1.1",
            host="zachwilson.techcreator.io",
            event_time=event_time,
            user_id="user123",
            event_type="page_view"
        )
        
        assert event.ip_address == "192.168.1.1"
        assert event.host == "zachwilson.techcreator.io"
        assert event.event_time == event_time
        assert event.user_id == "user123"
        assert event.event_type == "page_view"
    
    def test_web_event_to_dict(self):
        """Test converting WebEvent to dictionary"""
        event_time = datetime(2023, 1, 1, 12, 0, 0)
        event = WebEvent(
            ip_address="192.168.1.1",
            host="zachwilson.techcreator.io",
            event_time=event_time,
            user_id="user123",
            event_type="page_view"
        )
        
        event_dict = event.to_dict()
        
        assert event_dict['ip_address'] == "192.168.1.1"
        assert event_dict['host'] == "zachwilson.techcreator.io"
        assert event_dict['event_time'] == "2023-01-01T12:00:00"
        assert event_dict['user_id'] == "user123"
        assert event_dict['event_type'] == "page_view"
    
    def test_web_event_from_dict(self):
        """Test creating WebEvent from dictionary"""
        event_dict = {
            'ip_address': "192.168.1.1",
            'host': "zachwilson.techcreator.io",
            'event_time': "2023-01-01T12:00:00",
            'user_id': "user123",
            'event_type': "page_view"
        }
        
        event = WebEvent.from_dict(event_dict)
        
        assert event.ip_address == "192.168.1.1"
        assert event.host == "zachwilson.techcreator.io"
        assert event.event_time == datetime(2023, 1, 1, 12, 0, 0)
        assert event.user_id == "user123"
        assert event.event_type == "page_view"

class TestSession:
    """Test Session data class"""
    
    def test_session_creation(self):
        """Test creating a Session instance"""
        start_time = datetime(2023, 1, 1, 12, 0, 0)
        end_time = datetime(2023, 1, 1, 12, 5, 0)
        
        session = Session(
            ip_address="192.168.1.1",
            host="zachwilson.techcreator.io",
            start_time=start_time,
            end_time=end_time,
            event_count=10
        )
        
        assert session.ip_address == "192.168.1.1"
        assert session.host == "zachwilson.techcreator.io"
        assert session.start_time == start_time
        assert session.end_time == end_time
        assert session.event_count == 10
        assert session.duration_minutes == 5.0
    
    def test_session_to_dict(self):
        """Test converting Session to dictionary"""
        start_time = datetime(2023, 1, 1, 12, 0, 0)
        end_time = datetime(2023, 1, 1, 12, 5, 0)
        
        session = Session(
            ip_address="192.168.1.1",
            host="zachwilson.techcreator.io",
            start_time=start_time,
            end_time=end_time,
            event_count=10
        )
        
        session_dict = session.to_dict()
        
        assert session_dict['ip_address'] == "192.168.1.1"
        assert session_dict['host'] == "zachwilson.techcreator.io"
        assert session_dict['start_time'] == "2023-01-01T12:00:00"
        assert session_dict['end_time'] == "2023-01-01T12:05:00"
        assert session_dict['event_count'] == 10
        assert session_dict['duration_minutes'] == 5.0

class TestSessionizationFunction:
    """Test SessionizationFunction"""
    
    def test_sessionization_function_initialization(self):
        """Test SessionizationFunction initialization"""
        function = SessionizationFunction(session_gap_minutes=5)
        
        assert function.session_gap_minutes == 5
        assert function.session_gap_ms == 300000  # 5 minutes in milliseconds
        assert function.sessions == []
        assert function.current_session_start is None
        assert function.current_session_events == 0
        assert function.timer_registered is False
    
    def test_sessionization_function_open(self):
        """Test SessionizationFunction open method"""
        function = SessionizationFunction(session_gap_minutes=5)
        mock_context = Mock()
        
        with patch('sessionization_job.logger') as mock_logger:
            function.open(mock_context)
            mock_logger.info.assert_called_with("Initializing sessionization with 5 minute gap")

class TestSessionizationJob:
    """Test the main sessionization job functions"""
    
    def test_create_flink_environment(self):
        """Test creating Flink execution environment"""
        with patch('sessionization_job.StreamExecutionEnvironment') as mock_env_class:
            mock_env = Mock()
            mock_env_class.get_execution_environment.return_value = mock_env
            
            env = create_flink_environment()
            
            mock_env.set_parallelism.assert_called_with(1)
            mock_env.set_stream_time_characteristic.assert_called()
    
    def test_analyze_tech_creator_sessions(self):
        """Test analyzing Tech Creator sessions"""
        mock_stream = Mock()
        
        result = analyze_tech_creator_sessions(mock_stream)
        
        assert 'tech_creator_avg_events_per_session' in result
        assert 'host_comparison' in result
        assert 'zachwilson.techcreator.io' in result['host_comparison']
        assert 'zachwilson.tech' in result['host_comparison']
        assert 'lulu.techcreator.io' in result['host_comparison']

class TestDataGeneration:
    """Test data generation utilities"""
    
    def test_generate_test_web_events(self):
        """Test generating test web events"""
        events = self._generate_test_web_events()
        
        assert len(events) > 0
        for event in events:
            assert 'ip_address' in event
            assert 'host' in event
            assert 'event_time' in event
            assert event['host'] in ['zachwilson.techcreator.io', 'zachwilson.tech', 'lulu.techcreator.io']
    
    def _generate_test_web_events(self):
        """Generate test web events for testing"""
        base_time = datetime(2023, 1, 1, 12, 0, 0)
        events = []
        
        # Generate events for zachwilson.techcreator.io
        for i in range(5):
            event = {
                'ip_address': f'192.168.1.{i+1}',
                'host': 'zachwilson.techcreator.io',
                'event_time': (base_time + timedelta(minutes=i)).isoformat(),
                'user_id': f'user{i+1}',
                'event_type': 'page_view'
            }
            events.append(event)
        
        # Generate events for zachwilson.tech
        for i in range(3):
            event = {
                'ip_address': f'192.168.2.{i+1}',
                'host': 'zachwilson.tech',
                'event_time': (base_time + timedelta(minutes=i*2)).isoformat(),
                'user_id': f'user{i+10}',
                'event_type': 'click'
            }
            events.append(event)
        
        # Generate events for lulu.techcreator.io
        for i in range(4):
            event = {
                'ip_address': f'192.168.3.{i+1}',
                'host': 'lulu.techcreator.io',
                'event_time': (base_time + timedelta(minutes=i*3)).isoformat(),
                'user_id': f'user{i+20}',
                'event_type': 'scroll'
            }
            events.append(event)
        
        return events
    
    def test_create_test_data_file(self):
        """Test creating a test data file"""
        events = self._generate_test_web_events()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            for event in events:
                f.write(json.dumps(event) + '\n')
            temp_file = f.name
        
        try:
            # Verify file was created and contains data
            assert os.path.exists(temp_file)
            
            with open(temp_file, 'r') as f:
                lines = f.readlines()
                assert len(lines) == len(events)
                
                # Verify first line is valid JSON
                first_event = json.loads(lines[0])
                assert 'ip_address' in first_event
                assert 'host' in first_event
                
        finally:
            # Clean up
            os.unlink(temp_file)

class TestIntegration:
    """Integration tests for the complete workflow"""
    
    def test_complete_sessionization_workflow(self):
        """Test the complete sessionization workflow"""
        # This would be a more comprehensive integration test
        # that tests the entire Flink job pipeline
        # For now, we'll test the individual components
        
        # Test WebEvent creation
        event = WebEvent(
            ip_address="192.168.1.1",
            host="zachwilson.techcreator.io",
            event_time=datetime.now(),
            user_id="user123",
            event_type="page_view"
        )
        assert event is not None
        
        # Test Session creation
        session = Session(
            ip_address="192.168.1.1",
            host="zachwilson.techcreator.io",
            start_time=datetime.now(),
            end_time=datetime.now() + timedelta(minutes=5),
            event_count=10
        )
        assert session is not None
        
        # Test analysis function
        mock_stream = Mock()
        analysis = analyze_tech_creator_sessions(mock_stream)
        assert analysis is not None

if __name__ == "__main__":
    pytest.main([__file__]) 