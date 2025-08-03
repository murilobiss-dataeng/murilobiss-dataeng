#!/usr/bin/env python3
"""
Test data generators for Spark jobs
Provides fake input and expected output data for testing
"""

from pyspark.sql import SparkSession
from pyspark.sql.types import *
from datetime import date, datetime
import random

def create_spark_session():
    """Create Spark session for testing"""
    return SparkSession.builder \
        .appName("TestDataGenerator") \
        .master("local[2]") \
        .getOrCreate()

def generate_actor_films_test_data(spark):
    """Generate test data for actor_films table"""
    
    # Define schema
    schema = StructType([
        StructField("actorid", IntegerType(), False),
        StructField("actor", StringType(), False),
        StructField("film", StringType(), False),
        StructField("votes", IntegerType(), False),
        StructField("rating", DoubleType(), False),
        StructField("filmid", IntegerType(), False),
        StructField("year", IntegerType(), False)
    ])
    
    # Generate test data
    test_data = [
        # Actor 1 - Star quality, active
        (1, "Tom Hanks", "Forrest Gump", 1000000, 8.8, 101, 2023),
        (1, "Tom Hanks", "Cast Away", 800000, 7.8, 102, 2023),
        (1, "Tom Hanks", "Saving Private Ryan", 900000, 8.5, 103, 2022),
        
        # Actor 2 - Good quality, not active
        (2, "Brad Pitt", "Fight Club", 1200000, 8.8, 201, 2022),
        (2, "Brad Pitt", "Ocean's Eleven", 600000, 7.7, 202, 2022),
        
        # Actor 3 - Average quality, active
        (3, "John Doe", "Action Movie", 300000, 6.5, 301, 2023),
        (3, "John Doe", "Drama Film", 250000, 6.8, 302, 2023),
        
        # Actor 4 - Bad quality, not active
        (4, "Jane Smith", "B Movie", 50000, 4.2, 401, 2021),
        
        # Actor 5 - New actor, active
        (5, "New Actor", "Recent Film", 400000, 7.5, 501, 2023),
    ]
    
    return spark.createDataFrame(test_data, schema)

def generate_actors_history_scd_test_data(spark):
    """Generate test data for actors_history_scd table"""
    
    schema = StructType([
        StructField("actorid", IntegerType(), False),
        StructField("actor", StringType(), False),
        StructField("quality_class", StringType(), False),
        StructField("is_active", BooleanType(), False),
        StructField("start_date", DateType(), False),
        StructField("end_date", DateType(), False),
        StructField("current_flag", BooleanType(), False)
    ])
    
    test_data = [
        # Actor 1 - Current record (will be updated)
        (1, "Tom Hanks", "good", True, date(2022, 1, 1), date(9999, 12, 31), True),
        
        # Actor 2 - Current record (no change)
        (2, "Brad Pitt", "good", False, date(2022, 1, 1), date(9999, 12, 31), True),
        
        # Actor 3 - Current record (will be updated)
        (3, "John Doe", "bad", True, date(2022, 1, 1), date(9999, 12, 31), True),
        
        # Actor 4 - Current record (no change)
        (4, "Jane Smith", "bad", False, date(2021, 1, 1), date(9999, 12, 31), True),
        
        # Historical records for Actor 1
        (1, "Tom Hanks", "average", False, date(2021, 1, 1), date(2021, 12, 31), False),
    ]
    
    return spark.createDataFrame(test_data, schema)

def generate_events_test_data(spark):
    """Generate test data for events table"""
    
    schema = StructType([
        StructField("event_id", IntegerType(), False),
        StructField("user_id", IntegerType(), False),
        StructField("host", StringType(), False),
        StructField("event_time", TimestampType(), False),
        StructField("event_type", StringType(), False)
    ])
    
    # Generate events for different hosts and dates
    test_data = []
    event_id = 1
    
    # Host 1 - High activity
    for day in range(1, 16):  # First 15 days of month
        for user in range(1, 6):  # 5 users
            for event in range(10):  # 10 events per user per day
                test_data.append((
                    event_id,
                    user,
                    "host1.example.com",
                    datetime(2024, 1, day, random.randint(0, 23), random.randint(0, 59)),
                    "page_view"
                ))
                event_id += 1
    
    # Host 2 - Medium activity
    for day in range(1, 16):
        for user in range(1, 4):  # 3 users
            for event in range(5):  # 5 events per user per day
                test_data.append((
                    event_id,
                    user + 10,  # Different user IDs
                    "host2.example.com",
                    datetime(2024, 1, day, random.randint(0, 23), random.randint(0, 59)),
                    "page_view"
                ))
                event_id += 1
    
    # Host 3 - Low activity
    for day in range(1, 16):
        for user in range(1, 3):  # 2 users
            for event in range(2):  # 2 events per user per day
                test_data.append((
                    event_id,
                    user + 20,  # Different user IDs
                    "host3.example.com",
                    datetime(2024, 1, day, random.randint(0, 23), random.randint(0, 59)),
                    "page_view"
                ))
                event_id += 1
    
    return spark.createDataFrame(test_data, schema)

def generate_host_activity_reduced_test_data(spark):
    """Generate test data for host_activity_reduced table"""
    
    schema = StructType([
        StructField("month", DateType(), False),
        StructField("host", StringType(), False),
        StructField("hit_array", ArrayType(IntegerType()), False),
        StructField("unique_visitors_array", ArrayType(IntegerType()), False)
    ])
    
    # Generate existing monthly data for January 2024
    test_data = [
        # Host 1 - Existing data for first 14 days
        (date(2024, 1, 1), "host1.example.com", 
         [50, 45, 52, 48, 55, 60, 58, 62, 65, 70, 68, 72, 75, 80],  # hits
         [5, 4, 5, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]),  # unique visitors
        
        # Host 2 - Existing data for first 14 days
        (date(2024, 1, 1), "host2.example.com",
         [15, 12, 18, 14, 16, 20, 19, 22, 25, 24, 26, 28, 30, 32],  # hits
         [3, 2, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]),  # unique visitors
        
        # Host 3 - Existing data for first 14 days
        (date(2024, 1, 1), "host3.example.com",
         [4, 3, 5, 4, 6, 5, 4, 6, 7, 5, 6, 8, 7, 9],  # hits
         [2, 1, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2]),  # unique visitors
    ]
    
    return spark.createDataFrame(test_data, schema)

def get_expected_scd_output():
    """Get expected output for SCD incremental update"""
    
    # Expected results based on test data
    expected_data = [
        # Actor 1 - Updated to star quality, still active
        (1, "Tom Hanks", "star", True, date(2024, 1, 15), date(9999, 12, 31), True),
        
        # Actor 2 - No change, keep existing
        (2, "Brad Pitt", "good", False, date(2022, 1, 1), date(9999, 12, 31), True),
        
        # Actor 3 - Updated to average quality, still active
        (3, "John Doe", "average", True, date(2024, 1, 15), date(9999, 12, 31), True),
        
        # Actor 4 - No change, keep existing
        (4, "Jane Smith", "bad", False, date(2021, 1, 1), date(9999, 12, 31), True),
        
        # Actor 5 - New actor
        (5, "New Actor", "good", True, date(2024, 1, 15), date(9999, 12, 31), True),
        
        # Historical records
        (1, "Tom Hanks", "good", True, date(2022, 1, 1), date(2024, 1, 14), False),
        (1, "Tom Hanks", "average", False, date(2021, 1, 1), date(2021, 12, 31), False),
        (3, "John Doe", "bad", True, date(2022, 1, 1), date(2024, 1, 14), False),
    ]
    
    return expected_data

def get_expected_monthly_aggregation_output():
    """Get expected output for monthly fact aggregation"""
    
    # Expected results for day 15 (new data being added)
    expected_data = [
        # Host 1 - Updated with day 15 data
        (date(2024, 1, 1), "host1.example.com", 
         [50, 45, 52, 48, 55, 60, 58, 62, 65, 70, 68, 72, 75, 80, 85],  # hits + day 15
         [5, 4, 5, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]),  # visitors + day 15
        
        # Host 2 - Updated with day 15 data
        (date(2024, 1, 1), "host2.example.com",
         [15, 12, 18, 14, 16, 20, 19, 22, 25, 24, 26, 28, 30, 32, 35],  # hits + day 15
         [3, 2, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]),  # visitors + day 15
        
        # Host 3 - Updated with day 15 data
        (date(2024, 1, 1), "host3.example.com",
         [4, 3, 5, 4, 6, 5, 4, 6, 7, 5, 6, 8, 7, 9, 10],  # hits + day 15
         [2, 1, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2]),  # visitors + day 15
    ]
    
    return expected_data

if __name__ == "__main__":
    """Test data generation script"""
    spark = create_spark_session()
    
    print("Generating test data...")
    
    # Generate all test datasets
    actor_films_df = generate_actor_films_test_data(spark)
    actors_history_df = generate_actors_history_scd_test_data(spark)
    events_df = generate_events_test_data(spark)
    host_activity_df = generate_host_activity_reduced_test_data(spark)
    
    print("Test data generated successfully!")
    print(f"Actor films: {actor_films_df.count()} records")
    print(f"Actors history: {actors_history_df.count()} records")
    print(f"Events: {events_df.count()} records")
    print(f"Host activity: {host_activity_df.count()} records")
    
    spark.stop() 