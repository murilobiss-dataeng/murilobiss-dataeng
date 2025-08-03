# Week 3.2 Homework - Spark Fundamentals (PostgreSQL to SparkSQL Conversion)

## What I did

Had to convert 2 queries from the previous weeks (Week 1 - Dimensional Data Modeling and Week 2 - Fact Data Modeling) from PostgreSQL to SparkSQL. Created PySpark jobs with proper testing structure and comprehensive documentation.

## My approach

### 1. Query Selection
Selected two complex queries from previous weeks:
- **Week 1**: SCD (Slowly Changing Dimension) incremental update query
- **Week 2**: Monthly reduced fact table aggregation query

### 2. PostgreSQL to SparkSQL Conversion
Converted the selected queries considering:
- **Data Types**: PostgreSQL types to Spark SQL types
- **Window Functions**: Adapted for Spark SQL syntax
- **Date Functions**: Converted PostgreSQL date functions to Spark equivalents
- **Aggregation Functions**: Maintained logic while adapting to Spark

### 3. PySpark Job Structure
Created modular PySpark jobs in `src/jobs/`:
- **scd_incremental_update.py**: Handles SCD incremental updates
- **monthly_fact_aggregation.py**: Processes monthly fact table aggregations

### 4. Testing Framework
Built comprehensive tests in `src/tests/`:
- **Fake input data**: Generated test datasets
- **Expected output data**: Defined expected results
- **Unit tests**: Test individual functions
- **Integration tests**: Test complete workflows

## Technical Implementation

### Key Conversions Made

#### PostgreSQL to SparkSQL Syntax Changes:
- `DATE_TRUNC('month', date)` → `date_trunc('month', date)`
- `CURRENT_DATE` → `current_date()`
- `COALESCE` → `coalesce`
- `LEAD()` → `lead()` (window functions)
- `ARRAY<DATE>` → `array<date>`

#### Data Type Mappings:
- `BOOLEAN` → `boolean`
- `INT` → `int`
- `STRING` → `string`
- `DATE` → `date`
- `ARRAY<T>` → `array<t>`

### PySpark Job Features
- **Modular Design**: Separate functions for different operations
- **Error Handling**: Comprehensive exception handling
- **Logging**: Detailed logging for debugging
- **Configuration**: Configurable parameters
- **Performance**: Optimized for Spark execution

### Testing Strategy
- **Unit Tests**: Test individual functions with mock data
- **Integration Tests**: Test complete data pipelines
- **Data Validation**: Verify output schema and data quality
- **Performance Tests**: Measure execution time and resource usage

## Files Created

### Source Code
- `src/jobs/scd_incremental_update.py` - SCD incremental update job
- `src/jobs/monthly_fact_aggregation.py` - Monthly fact aggregation job

### Tests
- `src/tests/test_scd_incremental_update.py` - SCD job tests
- `src/tests/test_monthly_fact_aggregation.py` - Monthly aggregation tests
- `src/tests/test_data.py` - Test data generators

### Documentation
- `README.md` - This comprehensive documentation

## Challenges Faced

The main challenges were:
1. **Syntax Differences**: Adapting PostgreSQL-specific syntax to SparkSQL
2. **Data Type Handling**: Converting complex data types between systems
3. **Window Functions**: Ensuring window function behavior is identical
4. **Testing Strategy**: Creating realistic test data and expected outputs
5. **Performance Optimization**: Ensuring Spark jobs are efficient

## Performance Considerations

- **Partitioning**: Used appropriate partitioning strategies
- **Broadcasting**: Applied broadcast joins where beneficial
- **Caching**: Strategic caching of frequently used DataFrames
- **Memory Management**: Optimized memory usage for large datasets 