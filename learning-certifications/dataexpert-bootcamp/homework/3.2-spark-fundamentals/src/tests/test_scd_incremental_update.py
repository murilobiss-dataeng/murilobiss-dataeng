#!/usr/bin/env python3
"""
Tests for SCD Incremental Update Job
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

from scd_incremental_update import scd_incremental_update, get_latest_data, get_existing_current_records
from test_data import (
    generate_actor_films_test_data, 
    generate_actors_history_scd_test_data,
    get_expected_scd_output
)

class TestSCDIncrementalUpdate(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Set up Spark session for all tests"""
        cls.spark = SparkSession.builder \
            .appName("TestSCDIncrementalUpdate") \
            .master("local[2]") \
            .getOrCreate()
        
        # Generate test data
        cls.actor_films_df = generate_actor_films_test_data(cls.spark)
        cls.actors_history_df = generate_actors_history_scd_test_data(cls.spark)
        cls.expected_output = get_expected_scd_output()
    
    @classmethod
    def tearDownClass(cls):
        """Clean up Spark session"""
        cls.spark.stop()
    
    def test_get_latest_data(self):
        """Test getting latest data for actors"""
        
        latest_data = get_latest_data(self.spark, self.actor_films_df)
        
        # Check schema
        expected_schema = StructType([
            StructField("actorid", IntegerType(), False),
            StructField("actor", StringType(), False),
            StructField("quality_class", StringType(), False),
            StructField("is_active", BooleanType(), False),
            StructField("start_date", DateType(), False)
        ])
        
        self.assertEqual(latest_data.schema, expected_schema)
        
        # Check data
        latest_data_list = latest_data.collect()
        
        # Should have 5 actors
        self.assertEqual(len(latest_data_list), 5)
        
        # Check specific actor data
        tom_hanks = [row for row in latest_data_list if row.actorid == 1][0]
        self.assertEqual(tom_hanks.quality_class, "star")
        self.assertTrue(tom_hanks.is_active)
    
    def test_get_existing_current_records(self):
        """Test getting existing current records"""
        
        existing_current = get_existing_current_records(self.spark, self.actors_history_df)
        
        # Check that current_flag is set to False
        current_flags = [row.current_flag for row in existing_current.collect()]
        self.assertTrue(all(flag == False for flag in current_flags))
        
        # Check that end_date is updated for current records
        end_dates = [row.end_date for row in existing_current.collect() if row.current_flag == False]
        expected_end_date = date.today().replace(day=date.today().day - 1)
        self.assertTrue(all(end_date == expected_end_date for end_date in end_dates))
    
    def test_scd_incremental_update_complete(self):
        """Test complete SCD incremental update process"""
        
        result = scd_incremental_update(self.spark, self.actor_films_df, self.actors_history_df)
        
        # Check schema
        expected_schema = StructType([
            StructField("actorid", IntegerType(), False),
            StructField("actor", StringType(), False),
            StructField("quality_class", StringType(), False),
            StructField("is_active", BooleanType(), False),
            StructField("start_date", DateType(), False),
            StructField("end_date", DateType(), False),
            StructField("current_flag", BooleanType(), False)
        ])
        
        self.assertEqual(result.schema, expected_schema)
        
        # Check that we have the expected number of records
        result_count = result.count()
        expected_count = len(self.expected_output)
        self.assertEqual(result_count, expected_count)
        
        # Check specific records
        result_list = result.collect()
        
        # Check Tom Hanks updated record
        tom_hanks_current = [row for row in result_list if row.actorid == 1 and row.current_flag == True][0]
        self.assertEqual(tom_hanks_current.quality_class, "star")
        self.assertTrue(tom_hanks_current.is_active)
        
        # Check historical record for Tom Hanks
        tom_hanks_historical = [row for row in result_list if row.actorid == 1 and row.current_flag == False]
        self.assertTrue(len(tom_hanks_historical) >= 1)
        
        # Check new actor
        new_actor = [row for row in result_list if row.actorid == 5][0]
        self.assertEqual(new_actor.actor, "New Actor")
        self.assertEqual(new_actor.quality_class, "good")
        self.assertTrue(new_actor.current_flag)
    
    def test_quality_classification_logic(self):
        """Test quality classification logic"""
        
        latest_data = get_latest_data(self.spark, self.actor_films_df)
        latest_data_list = latest_data.collect()
        
        # Check quality classifications
        quality_map = {row.actorid: row.quality_class for row in latest_data_list}
        
        # Tom Hanks: avg rating 8.3 -> star
        self.assertEqual(quality_map[1], "star")
        
        # Brad Pitt: avg rating 8.25 -> good
        self.assertEqual(quality_map[2], "good")
        
        # John Doe: avg rating 6.65 -> average
        self.assertEqual(quality_map[3], "average")
        
        # Jane Smith: avg rating 4.2 -> bad
        self.assertEqual(quality_map[4], "bad")
        
        # New Actor: avg rating 7.5 -> good
        self.assertEqual(quality_map[5], "good")
    
    def test_active_status_logic(self):
        """Test active status logic"""
        
        latest_data = get_latest_data(self.spark, self.actor_films_df)
        latest_data_list = latest_data.collect()
        
        # Check active status
        active_map = {row.actorid: row.is_active for row in latest_data_list}
        
        # Actors with 2023 films should be active
        self.assertTrue(active_map[1])  # Tom Hanks - 2023 films
        self.assertTrue(active_map[3])  # John Doe - 2023 films
        self.assertTrue(active_map[5])  # New Actor - 2023 films
        
        # Actors with only 2022 or earlier films should not be active
        self.assertFalse(active_map[2])  # Brad Pitt - 2022 films
        self.assertFalse(active_map[4])  # Jane Smith - 2021 films
    
    def test_data_integrity(self):
        """Test data integrity constraints"""
        
        result = scd_incremental_update(self.spark, self.actor_films_df, self.actors_history_df)
        result_list = result.collect()
        
        # Check that no duplicate actorid with current_flag=True
        current_actors = [row.actorid for row in result_list if row.current_flag == True]
        self.assertEqual(len(current_actors), len(set(current_actors)))
        
        # Check that all current records have end_date = 9999-12-31
        current_records = [row for row in result_list if row.current_flag == True]
        for record in current_records:
            self.assertEqual(record.end_date, date(9999, 12, 31))
        
        # Check that historical records have end_date < 9999-12-31
        historical_records = [row for row in result_list if row.current_flag == False]
        for record in historical_records:
            self.assertLess(record.end_date, date(9999, 12, 31))

if __name__ == "__main__":
    unittest.main() 