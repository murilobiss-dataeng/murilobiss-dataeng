#!/usr/bin/env python3
"""
Week 3.2 - SCD Incremental Update Job
Converted from PostgreSQL to SparkSQL
Handles Slowly Changing Dimension incremental updates for actors
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.window import Window
from pyspark.sql.types import *
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_spark_session():
    """Create and configure Spark session"""
    spark = SparkSession.builder \
        .appName("SCDIncrementalUpdate") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .getOrCreate()
    
    return spark

def get_latest_data(spark, actor_films_df):
    """Get latest data for actors with quality classification"""
    
    # Group by actor and year, calculate quality based on most recent year
    films_grouped = actor_films_df \
        .groupBy("actorid", "actor", "year") \
        .agg(
            collect_list(struct("film", "votes", "rating", "filmid")).alias("films"),
            avg("rating").alias("avg_rating"),
            max("year").over(Window.partitionBy("actorid")).alias("max_year")
        )
    
    # Determine quality class and active status
    quality_analysis = films_grouped \
        .withColumn("quality_class", 
            when(col("avg_rating") > 8, "star")
            .when((col("avg_rating") > 7) & (col("avg_rating") <= 8), "good")
            .when((col("avg_rating") > 6) & (col("avg_rating") <= 7), "average")
            .otherwise("bad")
        ) \
        .withColumn("is_active", col("year") == col("max_year"))
    
    # Get latest data for each actor
    latest_data = quality_analysis \
        .filter(col("year") == col("max_year")) \
        .select("actorid", "actor", "quality_class", "is_active") \
        .withColumn("start_date", current_date())
    
    return latest_data

def get_existing_current_records(spark, actors_history_scd_df):
    """Get existing current records and prepare to close them"""
    
    existing_current = actors_history_scd_df \
        .filter(col("current_flag") == True) \
        .withColumn("end_date", 
            when(col("current_flag") == True, date_sub(current_date(), 1))
            .otherwise(col("end_date"))
        ) \
        .withColumn("current_flag", lit(False))
    
    return existing_current

def identify_changed_records(spark, latest_data, existing_current):
    """Identify records where quality_class or is_active changed"""
    
    records_with_changes = latest_data \
        .join(existing_current, "actorid", "inner") \
        .filter(
            (col("latest_data.quality_class") != col("existing_current.quality_class")) |
            (col("latest_data.is_active") != col("existing_current.is_active"))
        ) \
        .select(
            col("latest_data.actorid"),
            col("latest_data.actor"),
            col("latest_data.quality_class"),
            col("latest_data.is_active"),
            col("latest_data.start_date"),
            lit("9999-12-31").cast("date").alias("end_date"),
            lit(True).alias("current_flag")
        )
    
    return records_with_changes

def identify_unchanged_records(spark, existing_current, latest_data):
    """Identify records that didn't change - keep existing"""
    
    records_no_changes = existing_current \
        .join(latest_data, "actorid", "inner") \
        .filter(
            (col("latest_data.quality_class") == col("existing_current.quality_class")) &
            (col("latest_data.is_active") == col("existing_current.is_active"))
        ) \
        .select(
            col("existing_current.actorid"),
            col("existing_current.actor"),
            col("existing_current.quality_class"),
            col("existing_current.is_active"),
            col("existing_current.start_date"),
            col("existing_current.end_date"),
            col("existing_current.current_flag")
        )
    
    return records_no_changes

def identify_new_actors(spark, latest_data, existing_current):
    """Identify completely new actors"""
    
    new_actors_only = latest_data \
        .join(existing_current, "actorid", "left") \
        .filter(col("existing_current.actorid").isNull()) \
        .select(
            col("latest_data.actorid"),
            col("latest_data.actor"),
            col("latest_data.quality_class"),
            col("latest_data.is_active"),
            col("latest_data.start_date"),
            lit("9999-12-31").cast("date").alias("end_date"),
            lit(True).alias("current_flag")
        )
    
    return new_actors_only

def scd_incremental_update(spark, actor_films_df, actors_history_scd_df):
    """
    Perform SCD incremental update
    Converted from PostgreSQL query to SparkSQL
    """
    
    logger.info("Starting SCD incremental update process")
    
    try:
        # Step 1: Get latest data
        logger.info("Getting latest actor data")
        latest_data = get_latest_data(spark, actor_films_df)
        
        # Step 2: Get existing current records
        logger.info("Processing existing current records")
        existing_current = get_existing_current_records(spark, actors_history_scd_df)
        
        # Step 3: Identify changed records
        logger.info("Identifying changed records")
        records_with_changes = identify_changed_records(spark, latest_data, existing_current)
        
        # Step 4: Identify unchanged records
        logger.info("Identifying unchanged records")
        records_no_changes = identify_unchanged_records(spark, existing_current, latest_data)
        
        # Step 5: Identify new actors
        logger.info("Identifying new actors")
        new_actors_only = identify_new_actors(spark, latest_data, existing_current)
        
        # Step 6: Combine all records
        logger.info("Combining all record types")
        final_result = existing_current \
            .filter(col("current_flag") == False) \
            .union(records_no_changes) \
            .union(records_with_changes) \
            .union(new_actors_only)
        
        logger.info("SCD incremental update completed successfully")
        return final_result
        
    except Exception as e:
        logger.error(f"Error in SCD incremental update: {e}")
        raise

def main():
    """Main execution function"""
    
    spark = create_spark_session()
    
    try:
        # Load data (in real scenario, these would be actual data sources)
        logger.info("Loading actor_films data")
        actor_films_df = spark.read.parquet("actor_films.parquet")
        
        logger.info("Loading actors_history_scd data")
        actors_history_scd_df = spark.read.parquet("actors_history_scd.parquet")
        
        # Perform SCD incremental update
        result = scd_incremental_update(spark, actor_films_df, actors_history_scd_df)
        
        # Show results
        logger.info("SCD Update Results:")
        result.show(10)
        
        # Save results (optional)
        result.write.mode("overwrite").parquet("scd_incremental_update_result.parquet")
        
        logger.info("SCD incremental update job completed")
        
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
        raise
    finally:
        spark.stop()

if __name__ == "__main__":
    main() 