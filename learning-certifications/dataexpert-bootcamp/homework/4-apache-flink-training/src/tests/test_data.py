#!/usr/bin/env python3
"""
Week 4 - Apache Flink Test Data Generation
Generates test web events for sessionization testing
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any

def generate_web_events_for_sessionization() -> List[Dict[str, Any]]:
    """
    Generate test web events for sessionization testing
    Creates realistic scenarios with different hosts and timing patterns
    """
    base_time = datetime(2023, 1, 1, 12, 0, 0)
    events = []
    
    # Scenario 1: zachwilson.techcreator.io - Multiple sessions
    # Session 1: 12:00-12:04 (5 events, 4 minutes apart)
    for i in range(5):
        event = {
            'ip_address': '192.168.1.1',
            'host': 'zachwilson.techcreator.io',
            'event_time': (base_time + timedelta(minutes=i)).isoformat(),
            'user_id': 'user1',
            'event_type': 'page_view'
        }
        events.append(event)
    
    # Gap of 6 minutes (should start new session)
    # Session 2: 12:10-12:13 (4 events, 3 minutes apart)
    for i in range(4):
        event = {
            'ip_address': '192.168.1.1',
            'host': 'zachwilson.techcreator.io',
            'event_time': (base_time + timedelta(minutes=10+i)).isoformat(),
            'user_id': 'user1',
            'event_type': 'click'
        }
        events.append(event)
    
    # Scenario 2: zachwilson.tech - Single long session
    # Session: 12:00-12:20 (10 events, 2 minutes apart)
    for i in range(10):
        event = {
            'ip_address': '192.168.1.2',
            'host': 'zachwilson.tech',
            'event_time': (base_time + timedelta(minutes=i*2)).isoformat(),
            'user_id': 'user2',
            'event_type': 'scroll'
        }
        events.append(event)
    
    # Scenario 3: lulu.techcreator.io - Multiple short sessions
    # Session 1: 12:00-12:02 (3 events, 1 minute apart)
    for i in range(3):
        event = {
            'ip_address': '192.168.1.3',
            'host': 'lulu.techcreator.io',
            'event_time': (base_time + timedelta(minutes=i)).isoformat(),
            'user_id': 'user3',
            'event_type': 'page_view'
        }
        events.append(event)
    
    # Gap of 7 minutes (should start new session)
    # Session 2: 12:09-12:11 (3 events, 1 minute apart)
    for i in range(3):
        event = {
            'ip_address': '192.168.1.3',
            'host': 'lulu.techcreator.io',
            'event_time': (base_time + timedelta(minutes=9+i)).isoformat(),
            'user_id': 'user3',
            'event_type': 'click'
        }
        events.append(event)
    
    # Gap of 8 minutes (should start new session)
    # Session 3: 12:19-12:21 (3 events, 1 minute apart)
    for i in range(3):
        event = {
            'ip_address': '192.168.1.3',
            'host': 'lulu.techcreator.io',
            'event_time': (base_time + timedelta(minutes=19+i)).isoformat(),
            'user_id': 'user3',
            'event_type': 'scroll'
        }
        events.append(event)
    
    # Scenario 4: Multiple users on same host
    # User 4 on zachwilson.techcreator.io
    for i in range(4):
        event = {
            'ip_address': '192.168.1.4',
            'host': 'zachwilson.techcreator.io',
            'event_time': (base_time + timedelta(minutes=i*3)).isoformat(),
            'user_id': 'user4',
            'event_type': 'page_view'
        }
        events.append(event)
    
    # User 5 on zachwilson.tech
    for i in range(6):
        event = {
            'ip_address': '192.168.1.5',
            'host': 'zachwilson.tech',
            'event_time': (base_time + timedelta(minutes=i*2+1)).isoformat(),
            'user_id': 'user5',
            'event_type': 'click'
        }
        events.append(event)
    
    return events

def generate_expected_sessions() -> List[Dict[str, Any]]:
    """
    Generate expected session results based on the test data
    """
    base_time = datetime(2023, 1, 1, 12, 0, 0)
    expected_sessions = [
        # zachwilson.techcreator.io - user1, session 1
        {
            'ip_address': '192.168.1.1',
            'host': 'zachwilson.techcreator.io',
            'start_time': base_time.isoformat(),
            'end_time': (base_time + timedelta(minutes=4)).isoformat(),
            'event_count': 5,
            'duration_minutes': 4.0
        },
        # zachwilson.techcreator.io - user1, session 2
        {
            'ip_address': '192.168.1.1',
            'host': 'zachwilson.techcreator.io',
            'start_time': (base_time + timedelta(minutes=10)).isoformat(),
            'end_time': (base_time + timedelta(minutes=13)).isoformat(),
            'event_count': 4,
            'duration_minutes': 3.0
        },
        # zachwilson.tech - user2, single session
        {
            'ip_address': '192.168.1.2',
            'host': 'zachwilson.tech',
            'start_time': base_time.isoformat(),
            'end_time': (base_time + timedelta(minutes=18)).isoformat(),
            'event_count': 10,
            'duration_minutes': 18.0
        },
        # lulu.techcreator.io - user3, session 1
        {
            'ip_address': '192.168.1.3',
            'host': 'lulu.techcreator.io',
            'start_time': base_time.isoformat(),
            'end_time': (base_time + timedelta(minutes=2)).isoformat(),
            'event_count': 3,
            'duration_minutes': 2.0
        },
        # lulu.techcreator.io - user3, session 2
        {
            'ip_address': '192.168.1.3',
            'host': 'lulu.techcreator.io',
            'start_time': (base_time + timedelta(minutes=9)).isoformat(),
            'end_time': (base_time + timedelta(minutes=11)).isoformat(),
            'event_count': 3,
            'duration_minutes': 2.0
        },
        # lulu.techcreator.io - user3, session 3
        {
            'ip_address': '192.168.1.3',
            'host': 'lulu.techcreator.io',
            'start_time': (base_time + timedelta(minutes=19)).isoformat(),
            'end_time': (base_time + timedelta(minutes=21)).isoformat(),
            'event_count': 3,
            'duration_minutes': 2.0
        },
        # zachwilson.techcreator.io - user4
        {
            'ip_address': '192.168.1.4',
            'host': 'zachwilson.techcreator.io',
            'start_time': base_time.isoformat(),
            'end_time': (base_time + timedelta(minutes=9)).isoformat(),
            'event_count': 4,
            'duration_minutes': 9.0
        },
        # zachwilson.tech - user5
        {
            'ip_address': '192.168.1.5',
            'host': 'zachwilson.tech',
            'start_time': (base_time + timedelta(minutes=1)).isoformat(),
            'end_time': (base_time + timedelta(minutes=11)).isoformat(),
            'event_count': 6,
            'duration_minutes': 10.0
        }
    ]
    
    return expected_sessions

def generate_expected_metrics() -> Dict[str, Any]:
    """
    Generate expected metrics based on the test data
    """
    return {
        'tech_creator_avg_events_per_session': 4.0,  # Average across all Tech Creator hosts
        'host_comparison': {
            'zachwilson.techcreator.io': {
                'avg_events': 4.33,  # (5+4+4)/3 sessions
                'total_sessions': 3,
                'total_events': 13
            },
            'zachwilson.tech': {
                'avg_events': 8.0,  # (10+6)/2 sessions
                'total_sessions': 2,
                'total_events': 16
            },
            'lulu.techcreator.io': {
                'avg_events': 3.0,  # (3+3+3)/3 sessions
                'total_sessions': 3,
                'total_events': 9
            }
        }
    }

def create_test_data_file(output_path: str = "data/web_events.json"):
    """
    Create a test data file with web events
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Generate test events
    events = generate_web_events_for_sessionization()
    
    # Write to file
    with open(output_path, 'w') as f:
        for event in events:
            f.write(json.dumps(event) + '\n')
    
    print(f"Created test data file: {output_path}")
    print(f"Generated {len(events)} web events")
    
    return output_path

def get_test_data_summary():
    """
    Get a summary of the test data for verification
    """
    events = generate_web_events_for_sessionization()
    
    # Group by host
    host_counts = {}
    for event in events:
        host = event['host']
        if host not in host_counts:
            host_counts[host] = 0
        host_counts[host] += 1
    
    print("Test Data Summary:")
    print("==================")
    for host, count in host_counts.items():
        print(f"{host}: {count} events")
    
    print(f"\nTotal events: {len(events)}")
    print(f"Expected sessions: {len(generate_expected_sessions())}")
    
    return host_counts

if __name__ == "__main__":
    # Create test data file
    create_test_data_file()
    
    # Print summary
    get_test_data_summary() 