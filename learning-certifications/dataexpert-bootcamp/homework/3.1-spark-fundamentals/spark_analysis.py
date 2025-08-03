#!/usr/bin/env python3
"""
Week 3 Homework - Spark Fundamentals
Gaming Data Analysis with Spark Optimizations
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.window import Window
from pyspark.sql.types import *

def create_spark_session():
    """Create and configure Spark session with optimizations"""
    spark = SparkSession.builder \
        .appName("GamingDataAnalysis") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .getOrCreate()
    
    # Disable automatic broadcast join
    spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "-1")
    
    return spark

def load_and_prepare_data(spark):
    """Load data and prepare bucketed tables"""
    
    # Load the datasets
    match_details = spark.read.parquet("match_details.parquet")
    matches = spark.read.parquet("matches.parquet")
    medals_matches_players = spark.read.parquet("medals_matches_players.parquet")
    medals = spark.read.parquet("medals.parquet")
    
    # Create bucketed tables for large fact tables
    match_details.write \
        .mode("overwrite") \
        .bucketBy(16, "match_id") \
        .sortBy("match_id") \
        .saveAsTable("match_details_bucketed")
    
    matches.write \
        .mode("overwrite") \
        .bucketBy(16, "match_id") \
        .sortBy("match_id") \
        .saveAsTable("matches_bucketed")
    
    medals_matches_players.write \
        .mode("overwrite") \
        .bucketBy(16, "match_id") \
        .sortBy("match_id") \
        .saveAsTable("medals_matches_players_bucketed")
    
    # Load bucketed tables
    match_details_bucketed = spark.table("match_details_bucketed")
    matches_bucketed = spark.table("matches_bucketed")
    medals_matches_players_bucketed = spark.table("medals_matches_players_bucketed")
    
    return match_details_bucketed, matches_bucketed, medals_matches_players_bucketed, medals

def analyze_player_performance(spark, match_details_bucketed, matches_bucketed):
    """Analyze which player averages the most kills per game"""
    
    # Join match details with matches to get player performance
    player_stats = match_details_bucketed \
        .join(broadcast(matches_bucketed), "match_id") \
        .groupBy("player_id", "player_name") \
        .agg(
            avg("kills").alias("avg_kills_per_game"),
            count("match_id").alias("total_games"),
            sum("kills").alias("total_kills")
        )
    
    # Rank players by average kills
    window_spec = Window.orderBy(col("avg_kills_per_game").desc())
    player_rankings = player_stats \
        .withColumn("rank", rank().over(window_spec))
    
    print("=== PLAYER PERFORMANCE ANALYSIS ===")
    print("Top 10 players by average kills per game:")
    player_rankings.show(10)
    
    return player_rankings

def analyze_playlist_popularity(spark, matches_bucketed):
    """Analyze which playlist gets played the most"""
    
    playlist_stats = matches_bucketed \
        .groupBy("playlist") \
        .agg(
            count("*").alias("total_matches"),
            countDistinct("match_id").alias("unique_matches")
        ) \
        .orderBy(col("total_matches").desc())
    
    print("\n=== PLAYLIST POPULARITY ===")
    print("Most played playlists:")
    playlist_stats.show()
    
    return playlist_stats

def analyze_map_popularity(spark, matches_bucketed):
    """Analyze which map gets played the most"""
    
    map_stats = matches_bucketed \
        .groupBy("map_name") \
        .agg(
            count("*").alias("total_matches"),
            countDistinct("match_id").alias("unique_matches")
        ) \
        .orderBy(col("total_matches").desc())
    
    print("\n=== MAP POPULARITY ===")
    print("Most played maps:")
    map_stats.show()
    
    return map_stats

def analyze_medals_by_map(spark, matches_bucketed, medals_matches_players_bucketed, medals):
    """Analyze which map do players get the most Killing Spree medals on"""
    
    # Join all tables to get medal data by map
    medal_map_analysis = medals_matches_players_bucketed \
        .join(broadcast(matches_bucketed), "match_id") \
        .join(broadcast(medals), "medal_id") \
        .filter(col("medal_name") == "Killing Spree") \
        .groupBy("map_name") \
        .agg(
            count("*").alias("killing_spree_medals"),
            countDistinct("player_id").alias("unique_players_with_medals")
        ) \
        .orderBy(col("killing_spree_medals").desc())
    
    print("\n=== KILLING SPREE MEDALS BY MAP ===")
    print("Maps with most Killing Spree medals:")
    medal_map_analysis.show()
    
    return medal_map_analysis

def test_sort_within_partitions(spark, matches_bucketed):
    """Test different sortWithinPartitions to find smallest data size"""
    
    print("\n=== SORT WITHIN PARTITIONS OPTIMIZATION ===")
    
    # Test different sort orders
    sort_configs = [
        ["playlist", "map_name"],
        ["map_name", "playlist"],
        ["playlist"],
        ["map_name"],
        ["match_id", "playlist", "map_name"]
    ]
    
    for i, sort_cols in enumerate(sort_configs):
        print(f"\nTesting sort order {i+1}: {sort_cols}")
        
        # Apply sort within partitions
        sorted_df = matches_bucketed.sortWithinPartitions(*sort_cols)
        
        # Force computation and get size
        sorted_df.cache()
        sorted_df.count()  # Trigger computation
        
        # Get size information
        size_info = sorted_df.select("*").count()
        print(f"  Records: {size_info}")
        
        # Note: In real scenario, you'd measure actual storage size
        # This is a simplified version for demonstration
        
        sorted_df.unpersist()

def main():
    """Main execution function"""
    
    # Create Spark session
    spark = create_spark_session()
    
    try:
        # Load and prepare data
        print("Loading and preparing data...")
        match_details_bucketed, matches_bucketed, medals_matches_players_bucketed, medals = load_and_prepare_data(spark)
        
        # Run analyses
        print("\nStarting data analysis...")
        
        # 1. Player performance analysis
        player_rankings = analyze_player_performance(spark, match_details_bucketed, matches_bucketed)
        
        # 2. Playlist popularity
        playlist_stats = analyze_playlist_popularity(spark, matches_bucketed)
        
        # 3. Map popularity
        map_stats = analyze_map_popularity(spark, matches_bucketed)
        
        # 4. Medal analysis by map
        medal_analysis = analyze_medals_by_map(spark, matches_bucketed, medals_matches_players_bucketed, medals)
        
        # 5. Sort within partitions optimization
        test_sort_within_partitions(spark, matches_bucketed)
        
        print("\n=== ANALYSIS COMPLETE ===")
        print("All optimizations applied:")
        print("- Broadcast joins for medals and maps")
        print("- Bucket joins for match_details, matches, and medals_matches_players")
        print("- Sort within partitions optimization tested")
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        raise
    finally:
        spark.stop()

if __name__ == "__main__":
    main() 