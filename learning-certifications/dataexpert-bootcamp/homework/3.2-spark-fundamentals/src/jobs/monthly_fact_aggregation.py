#!/usr/bin/env python3
"""
Week 3.2 - Monthly Fact Aggregation Job
Converted from PostgreSQL to SparkSQL
Handles monthly reduced fact table aggregations
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
        .appName("MonthlyFactAggregation") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .getOrCreate()
    
    return spark

def get_daily_metrics(spark, events_df):
    """Calculate daily metrics for each host"""
    
    daily_metrics = events_df \
        .withColumn("month", date_trunc("month", col("event_time"))) \
        .withColumn("activity_date", date(col("event_time"))) \
        .groupBy("month", "host", "activity_date") \
        .agg(
            count("*").alias("daily_hits"),
            countDistinct("user_id").alias("daily_unique_visitors")
        )
    
    return daily_metrics

def get_existing_monthly_data(spark, host_activity_reduced_df):
    """Get existing monthly data for the current month"""
    
    current_month = date_trunc("month", current_date())
    
    existing_monthly_data = host_activity_reduced_df \
        .filter(col("month") == current_month) \
        .select("month", "host", "hit_array", "unique_visitors_array")
    
    return existing_monthly_data

def calculate_day_of_month(spark, daily_metrics_df):
    """Calculate day of month for array positioning"""
    
    day_of_month = daily_metrics_df \
        .withColumn("day_number", day(col("activity_date")))
    
    return day_of_month

def update_monthly_arrays(spark, day_of_month_df, existing_monthly_data_df):
    """Update monthly arrays with new daily data"""
    
    # Join daily metrics with existing monthly data
    updated_data = day_of_month_df \
        .join(existing_monthly_data_df, ["month", "host"], "left") \
        .withColumn("hit_array", 
            when(col("hit_array").isNull(), array(col("daily_hits")))
            .otherwise(
                concat(
                    slice(col("hit_array"), 1, col("day_number") - 1),
                    array(col("daily_hits")),
                    slice(col("hit_array"), col("day_number") + 1, size(col("hit_array")))
                )
            )
        ) \
        .withColumn("unique_visitors_array",
            when(col("unique_visitors_array").isNull(), array(col("daily_unique_visitors")))
            .otherwise(
                concat(
                    slice(col("unique_visitors_array"), 1, col("day_number") - 1),
                    array(col("daily_unique_visitors")),
                    slice(col("unique_visitors_array"), col("day_number") + 1, size(col("unique_visitors_array")))
                )
            )
        ) \
        .select("month", "host", "hit_array", "unique_visitors_array")
    
    return updated_data

def monthly_fact_aggregation(spark, events_df, host_activity_reduced_df):
    """
    Perform monthly fact aggregation
    Converted from PostgreSQL query to SparkSQL
    """
    
    logger.info("Starting monthly fact aggregation process")
    
    try:
        # Step 1: Calculate daily metrics
        logger.info("Calculating daily metrics")
        daily_metrics = get_daily_metrics(spark, events_df)
        
        # Step 2: Get existing monthly data
        logger.info("Loading existing monthly data")
        existing_monthly_data = get_existing_monthly_data(spark, host_activity_reduced_df)
        
        # Step 3: Calculate day of month
        logger.info("Calculating day of month for array positioning")
        day_of_month = calculate_day_of_month(spark, daily_metrics)
        
        # Step 4: Update monthly arrays
        logger.info("Updating monthly arrays with new daily data")
        result = update_monthly_arrays(spark, day_of_month, existing_monthly_data)
        
        logger.info("Monthly fact aggregation completed successfully")
        return result
        
    except Exception as e:
        logger.error(f"Error in monthly fact aggregation: {e}")
        raise

def analyze_monthly_trends(spark, host_activity_reduced_df):
    """Analyze monthly trends from aggregated data"""
    
    logger.info("Analyzing monthly trends")
    
    # Calculate monthly totals
    monthly_totals = host_activity_reduced_df \
        .withColumn("total_hits", aggregate("hit_array", lit(0), lambda acc, x: acc + x)) \
        .withColumn("total_unique_visitors", aggregate("unique_visitors_array", lit(0), lambda acc, x: acc + x)) \
        .withColumn("avg_daily_hits", aggregate("hit_array", lit(0), lambda acc, x: acc + x) / size("hit_array")) \
        .withColumn("avg_daily_visitors", aggregate("unique_visitors_array", lit(0), lambda acc, x: acc + x) / size("unique_visitors_array"))
    
    # Top hosts by total hits
    top_hosts_by_hits = monthly_totals \
        .orderBy(col("total_hits").desc()) \
        .select("month", "host", "total_hits", "avg_daily_hits")
    
    # Top hosts by unique visitors
    top_hosts_by_visitors = monthly_totals \
        .orderBy(col("total_unique_visitors").desc()) \
        .select("month", "host", "total_unique_visitors", "avg_daily_visitors")
    
    return top_hosts_by_hits, top_hosts_by_visitors

def main():
    """Main execution function"""
    
    spark = create_spark_session()
    
    try:
        # Load data (in real scenario, these would be actual data sources)
        logger.info("Loading events data")
        events_df = spark.read.parquet("events.parquet")
        
        logger.info("Loading host_activity_reduced data")
        host_activity_reduced_df = spark.read.parquet("host_activity_reduced.parquet")
        
        # Perform monthly fact aggregation
        result = monthly_fact_aggregation(spark, events_df, host_activity_reduced_df)
        
        # Show results
        logger.info("Monthly Aggregation Results:")
        result.show(10)
        
        # Analyze trends
        top_hits, top_visitors = analyze_monthly_trends(spark, result)
        
        logger.info("Top hosts by hits:")
        top_hits.show(5)
        
        logger.info("Top hosts by unique visitors:")
        top_visitors.show(5)
        
        # Save results
        result.write.mode("overwrite").parquet("monthly_fact_aggregation_result.parquet")
        
        logger.info("Monthly fact aggregation job completed")
        
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
        raise
    finally:
        spark.stop()

if __name__ == "__main__":
    main() 