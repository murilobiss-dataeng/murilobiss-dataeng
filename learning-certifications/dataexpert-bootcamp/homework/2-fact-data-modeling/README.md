# Week 2 Homework - Fact Data Modeling

## What I did

Had to create a comprehensive fact data modeling solution using the `devices` and `events` datasets. The goal was to build cumulative and aggregated fact tables that track user device activity and host activity over time.

## My approach

### 1. Deduplication Query
Created a query to remove duplicates from `game_details` for Day 1 using window functions to identify and filter out duplicate records.

### 2. User Devices Cumulated Table DDL
Designed a table structure to track user device activity by browser type:
- `user_id` - identifies the user
- `browser_type` - the browser being used
- `device_activity_datelist` - array of dates when user was active with that browser
- `date` - current date for incremental processing

### 3. Cumulative Device Activity Query
Built a query that:
- Groups events by user and browser type
- Collects all activity dates into arrays
- Handles incremental updates by merging new dates with existing ones
- Uses window functions to track activity over time

### 4. Datelist Integer Conversion
Created a query to convert date arrays to integer representation:
- Converts each date to a day number (days since epoch)
- Stores as array of integers for more efficient storage
- Useful for date range queries and analytics

### 5. Hosts Cumulated Table DDL
Designed table to track host activity:
- `host` - identifies the host/server
- `host_activity_datelist` - array of dates when host had activity
- `date` - current date for incremental processing

### 6. Incremental Host Activity Query
Built query to:
- Extract host information from events
- Group by host and collect activity dates
- Handle incremental updates properly
- Merge new activity dates with existing ones

### 7. Monthly Reduced Fact Table DDL
Created aggregated monthly fact table:
- `month` - month of activity
- `host` - host identifier
- `hit_array` - array of daily hit counts for the month
- `unique_visitors_array` - array of daily unique visitor counts

### 8. Incremental Monthly Loading Query
Built query to:
- Aggregate daily data into monthly arrays
- Calculate hit counts and unique visitors per day
- Handle incremental loading day by day
- Maintain historical arrays for trend analysis

## Technical Implementation

### Key SQL Features Used
- **Window Functions**: ROW_NUMBER() for deduplication, LEAD/LAG for comparisons
- **Array Functions**: COLLECT_LIST, ARRAY_CONCAT for date aggregation
- **Date Functions**: DATE_TRUNC, DATE_ADD for time-based operations
- **Aggregation Functions**: COUNT, COUNT DISTINCT for metrics
- **CTEs**: For complex multi-step operations

### Data Modeling Patterns
- **Cumulative Fact Tables**: Track activity over time with date arrays
- **Incremental Processing**: Handle day-by-day updates efficiently
- **Array-based Storage**: Store time series data as arrays for performance
- **Reduced Fact Tables**: Pre-aggregated monthly summaries

### Performance Considerations
- Used arrays to avoid row explosion
- Implemented proper incremental logic
- Leveraged window functions for efficient processing
- Designed for scalable day-by-day loading

## Challenges Faced

The main challenges were:
1. **Array Manipulation**: Learning to work with ARRAY<DATE> and ARRAY<INT> data types
2. **Incremental Logic**: Figuring out how to merge new dates with existing arrays
3. **Date Conversions**: Converting between dates and integers efficiently
4. **Monthly Aggregation**: Building arrays of daily metrics within monthly buckets

## Files
- `solution.sql` - All the queries and DDL statements
- `README.md` - This explanation 