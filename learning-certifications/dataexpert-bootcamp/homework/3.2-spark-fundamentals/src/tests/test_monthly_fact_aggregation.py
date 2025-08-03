#!/usr/bin/env python3
"""
Tests for Monthly Fact Aggregation Job
Tests the conversion from PostgreSQL to SparkSQL
"""

import unittest
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from datetime import date
import sys
import os

# Add src to path to import jobs
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'jobs'))

from monthly_fact_aggregation import (
    monthly_fact_aggregation, 
    get_daily_metrics, 
    get_existing_monthly_data,
    update_monthly_arrays
)
from test_data import (
    generate_events_test_data, 
    generate_host_activity_reduced_test_data,
    get_expected_monthly_aggregation_output
)

class TestMonthlyFactAggregation(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Set up Spark session for all tests"""
        cls.spark = SparkSession.builder \
            .appName("TestMonthlyFactAggregation") \
            .master("local[2]") \
            .getOrCreate()
        
        # Generate test data
        cls.events_df = generate_events_test_data(cls.spark)
        cls.host_activity_df = generate_host_activity_reduced_test_data(cls.spark)
        cls.expected_output = get_expected_monthly_aggregation_output()
    
    @classmethod
    def tearDownClass(cls):
        """Clean up Spark session"""
        cls.spark.stop()
    
    def test_get_daily_metrics(self):
        """Test calculating daily metrics"""
        
        daily_metrics = get_daily_metrics(self.spark, self.events_df)
        
        # Check schema
        expected_schema = StructType([
            StructField("month", DateType(), False),
            StructField("host", StringType(), False),
            StructField("activity_date", DateType(), False),
            StructField("daily_hits", LongType(), False),
            StructField("daily_unique_visitors", LongType(), False)
        ])
        
        self.assertEqual(daily_metrics.schema, expected_schema)
        
        # Check data
        daily_metrics_list = daily_metrics.collect()
        
        # Should have data for 3 hosts for 15 days each
        self.assertEqual(len(daily_metrics_list), 45)  # 3 hosts * 15 days
        
        # Check specific host data
        host1_data = [row for row in daily_metrics_list if row.host == "host1.example.com"]
        self.assertEqual(len(host1_data), 15)  # 15 days
        
        # Check that daily hits are reasonable
        for row in host1_data:
            self.assertGreater(row.daily_hits, 0)
            self.assertLessEqual(row.daily_unique_visitors, 5)  # Max 5 users
    
    def test_get_existing_monthly_data(self):
        """Test getting existing monthly data"""
        
        existing_monthly_data = get_existing_monthly_data(self.spark, self.host_activity_df)
        
        # Check schema
        expected_schema = StructType([
            StructField("month", DateType(), False),
            StructField("host", StringType(), False),
            StructField("hit_array", ArrayType(IntegerType()), False),
            StructField("unique_visitors_array", ArrayType(IntegerType()), False)
        ])
        
        self.assertEqual(existing_monthly_data.schema, expected_schema)
        
        # Check data
        existing_data_list = existing_monthly_data.collect()
        
        # Should have 3 hosts
        self.assertEqual(len(existing_data_list), 3)
        
        # Check that arrays have 14 elements (existing data)
        for row in existing_data_list:
            self.assertEqual(len(row.hit_array), 14)
            self.assertEqual(len(row.unique_visitors_array), 14)
    
    def test_update_monthly_arrays(self):
        """Test updating monthly arrays with new daily data"""
        
        # Get daily metrics for day 15
        daily_metrics = get_daily_metrics(self.spark, self.events_df)
        day_15_metrics = daily_metrics.filter(col("activity_date") == date(2024, 1, 15))
        
        # Get existing monthly data
        existing_monthly_data = get_existing_monthly_data(self.spark, self.host_activity_df)
        
        # Update arrays
        updated_data = update_monthly_arrays(self.spark, day_15_metrics, existing_monthly_data)
        
        # Check that arrays now have 15 elements
        updated_data_list = updated_data.collect()
        
        for row in updated_data_list:
            self.assertEqual(len(row.hit_array), 15)
            self.assertEqual(len(row.unique_visitors_array), 15)
        
        # Check specific host data
        host1_updated = [row for row in updated_data_list if row.host == "host1.example.com"][0]
        
        # Check that day 15 data was added correctly
        self.assertEqual(host1_updated.hit_array[14], 85)  # Day 15 hits
        self.assertEqual(host1_updated.unique_visitors_array[14], 5)  # Day 15 visitors
    
    def test_monthly_fact_aggregation_complete(self):
        """Test complete monthly fact aggregation process"""
        
        result = monthly_fact_aggregation(self.spark, self.events_df, self.host_activity_df)
        
        # Check schema
        expected_schema = StructType([
            StructField("month", DateType(), False),
            StructField("host", StringType(), False),
            StructField("hit_array", ArrayType(IntegerType()), False),
            StructField("unique_visitors_array", ArrayType(IntegerType()), False)
        ])
        
        self.assertEqual(result.schema, expected_schema)
        
        # Check that we have the expected number of records
        result_count = result.count()
        expected_count = len(self.expected_output)
        self.assertEqual(result_count, expected_count)
        
        # Check specific records
        result_list = result.collect()
        
        # Check host1 data
        host1_data = [row for row in result_list if row.host == "host1.example.com"][0]
        self.assertEqual(len(host1_data.hit_array), 15)
        self.assertEqual(len(host1_data.unique_visitors_array), 15)
        
        # Check that day 15 data was added
        self.assertEqual(host1_data.hit_array[14], 85)
        self.assertEqual(host1_data.unique_visitors_array[14], 5)
    
    def test_array_manipulation_logic(self):
        """Test array manipulation logic"""
        
        # Test with a simple case
        from pyspark.sql.functions import array, lit, concat, slice, size
        
        # Create test data
        test_data = [
            (date(2024, 1, 1), "test_host", [1, 2, 3, 4], [1, 1, 1, 1], 5, 10, 5)  # day 5, hits 10, visitors 5
        ]
        
        test_df = self.spark.createDataFrame(test_data, ["month", "host", "hit_array", "unique_visitors_array", "day_number", "daily_hits", "daily_unique_visitors"])
        
        # Apply array update logic
        updated_df = test_df \
            .withColumn("hit_array", 
                concat(
                    slice(col("hit_array"), 1, col("day_number") - 1),
                    array(col("daily_hits")),
                    slice(col("hit_array"), col("day_number") + 1, size(col("hit_array")))
                )
            ) \
            .withColumn("unique_visitors_array",
                concat(
                    slice(col("unique_visitors_array"), 1, col("day_number") - 1),
                    array(col("daily_unique_visitors")),
                    slice(col("unique_visitors_array"), col("day_number") + 1, size(col("unique_visitors_array")))
                )
            )
        
        result = updated_df.collect()[0]
        
        # Check that array was updated correctly
        expected_hits = [1, 2, 3, 4, 10]  # Original + new value at position 5
        expected_visitors = [1, 1, 1, 1, 5]  # Original + new value at position 5
        
        self.assertEqual(result.hit_array, expected_hits)
        self.assertEqual(result.unique_visitors_array, expected_visitors)
    
    def test_data_consistency(self):
        """Test data consistency across the aggregation"""
        
        result = monthly_fact_aggregation(self.spark, self.events_df, self.host_activity_df)
        result_list = result.collect()
        
        # Check that all hosts have the same month
        months = [row.month for row in result_list]
        self.assertTrue(all(month == date(2024, 1, 1) for month in months))
        
        # Check that arrays have consistent lengths
        for row in result_list:
            self.assertEqual(len(row.hit_array), len(row.unique_visitors_array))
            self.assertEqual(len(row.hit_array), 15)  # 15 days
        
        # Check that hit counts are reasonable
        for row in result_list:
            for hit_count in row.hit_array:
                self.assertGreaterEqual(hit_count, 0)
        
        # Check that visitor counts are reasonable
        for row in result_list:
            for visitor_count in row.unique_visitors_array:
                self.assertGreaterEqual(visitor_count, 0)
                self.assertLessEqual(visitor_count, 5)  # Max 5 users per host
    
    def test_performance_optimization(self):
        """Test performance optimization features"""
        
        # Test that the job can handle larger datasets
        # Create a larger events dataset
        large_events_data = []
        for day in range(1, 16):
            for host_id in range(1, 11):  # 10 hosts
                for user_id in range(1, 21):  # 20 users per host
                    for event in range(5):  # 5 events per user per day
                        large_events_data.append((
                            len(large_events_data) + 1,
                            user_id,
                            f"host{host_id}.example.com",
                            date(2024, 1, day),
                            "page_view"
                        ))
        
        large_events_df = self.spark.createDataFrame(large_events_data, ["event_id", "user_id", "host", "event_time", "event_type"])
        
        # Test that the job completes without errors
        try:
            result = monthly_fact_aggregation(self.spark, large_events_df, self.host_activity_df)
            self.assertIsNotNone(result)
            self.assertGreater(result.count(), 0)
        except Exception as e:
            self.fail(f"Job failed with large dataset: {e}")

if __name__ == "__main__":
    unittest.main() 