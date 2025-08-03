# Week 3 Homework - Spark Fundamentals

## What I did

Had to build a comprehensive Spark job to analyze gaming data from multiple datasets: `match_details`, `matches`, `medals_matches_players`, and `medals`. The goal was to implement various Spark optimization techniques and answer specific analytical questions about player performance and game statistics.

## My approach

### 1. Spark Configuration Setup
- Disabled automatic broadcast joins with `spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "-1")`
- This forces explicit control over which tables get broadcast

### 2. Broadcast Join Implementation
- Explicitly broadcast `medals` and `maps` tables using `.broadcast()`
- These are small dimension tables that benefit from being broadcast to all executors
- Reduces network shuffling and improves join performance

### 3. Bucket Join Strategy
- Created bucketed tables for `match_details`, `matches`, and `medal_matches_players` on `match_id`
- Used 16 buckets to distribute data evenly across partitions
- This enables efficient bucket-to-bucket joins without shuffling

### 4. Data Aggregation Queries
Built queries to answer specific analytical questions:

#### Player Performance Analysis
- **Most kills per game**: Aggregated kills by player and calculated averages
- Used window functions to rank players by kill performance

#### Game Statistics
- **Most played playlist**: Counted matches by playlist type
- **Most played map**: Counted matches by map name
- **Best map for Killing Spree medals**: Analyzed medal distribution by map

### 5. Sort Within Partitions Optimization
- Tested different `.sortWithinPartitions()` strategies
- Compared data sizes with different sort orders
- Focused on low cardinality columns (playlists, maps) for optimal sorting

## Technical Implementation

### Key Spark Features Used
- **Broadcast Joins**: For small dimension tables
- **Bucket Joins**: For large fact tables on common join keys
- **Window Functions**: For ranking and analytical queries
- **Aggregation Functions**: COUNT, AVG, SUM for metrics
- **Sort Within Partitions**: For data size optimization

### Performance Optimizations
- **Broadcast Strategy**: Small tables broadcast to all nodes
- **Bucket Strategy**: Large tables bucketed on join keys
- **Sort Strategy**: Optimized partition sorting for storage efficiency
- **Join Order**: Strategic join sequence to minimize shuffling

### Data Processing Patterns
- **ETL Pipeline**: Extract from multiple sources, transform with joins, load aggregated results
- **Incremental Processing**: Designed for scalable data processing
- **Analytical Queries**: Business intelligence focused aggregations

## Challenges Faced

The main challenges were:
1. **Join Optimization**: Balancing broadcast vs bucket strategies for different table sizes
2. **Data Distribution**: Ensuring even bucket distribution across 16 partitions
3. **Sort Optimization**: Finding the optimal sort order for minimal data size
4. **Performance Tuning**: Configuring Spark for optimal execution

## Files
- `spark_analysis.py` - Main Spark job with all optimizations and queries
- `README.md` - This explanation 