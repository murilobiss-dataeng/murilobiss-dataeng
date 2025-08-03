-- Week 2 Homework - Fact Data Modeling
-- Working with devices and events datasets
-- Building cumulative and aggregated fact tables

-- 1. Deduplicate game_details from Day 1
WITH deduplicated AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (
            PARTITION BY game_id, team_id, player_id
            ORDER BY event_time
        ) AS rn
    FROM game_details
    WHERE DATE(event_time) = '2024-01-01'  -- Day 1
)
SELECT 
    user_id,
    event_type,
    event_time,
    game_id,
    score,
    level
FROM deduplicated
WHERE rn = 1;

-- 2. DDL for user_devices_cumulated table
CREATE TABLE user_devices_cumulated (
    user_id INT,
    browser_type STRING,
    device_activity_datelist ARRAY<DATE>,
    date DATE
);

-- 3. Cumulative query to generate device_activity_datelist from events
WITH daily_activity AS (
    SELECT 
        user_id,
        browser_type,
        DATE(event_time) AS activity_date
    FROM events e
    JOIN devices d ON e.device_id = d.device_id
    WHERE DATE(event_time) = CURRENT_DATE  -- Today's data
),
existing_activity AS (
    SELECT 
        user_id,
        browser_type,
        device_activity_datelist
    FROM user_devices_cumulated
    WHERE date = CURRENT_DATE - 1  -- Previous day's data
)
SELECT 
    COALESCE(da.user_id, ea.user_id) AS user_id,
    COALESCE(da.browser_type, ea.browser_type) AS browser_type,
    CASE 
        WHEN ea.device_activity_datelist IS NULL THEN ARRAY[da.activity_date]
        WHEN da.activity_date IS NULL THEN ea.device_activity_datelist
        WHEN NOT ARRAY_CONTAINS(ea.device_activity_datelist, da.activity_date) 
            THEN ARRAY_CONCAT(ea.device_activity_datelist, ARRAY[da.activity_date])
        ELSE ea.device_activity_datelist
    END AS device_activity_datelist,
    CURRENT_DATE AS date
FROM daily_activity da
FULL OUTER JOIN existing_activity ea 
    ON da.user_id = ea.user_id 
    AND da.browser_type = ea.browser_type;

-- 4. Convert device_activity_datelist to datelist_int
SELECT 
    user_id,
    browser_type,
    device_activity_datelist,
    ARRAY(
        SELECT CAST(DATEDIFF(activity_date, '1970-01-01') AS INT)
        FROM UNNEST(device_activity_datelist) AS activity_date
    ) AS datelist_int,
    date
FROM user_devices_cumulated
WHERE date = CURRENT_DATE;

-- 5. DDL for hosts_cumulated table
CREATE TABLE hosts_cumulated (
    host STRING,
    host_activity_datelist ARRAY<DATE>,
    date DATE
);

-- 6. Incremental query to generate host_activity_datelist
WITH daily_host_activity AS (
    SELECT 
        host,
        DATE(event_time) AS activity_date
    FROM events
    WHERE DATE(event_time) = CURRENT_DATE  -- Today's data
    GROUP BY host, DATE(event_time)
),
existing_host_activity AS (
    SELECT 
        host,
        host_activity_datelist
    FROM hosts_cumulated
    WHERE date = CURRENT_DATE - 1  -- Previous day's data
)
SELECT 
    COALESCE(dha.host, eha.host) AS host,
    CASE 
        WHEN eha.host_activity_datelist IS NULL THEN ARRAY[dha.activity_date]
        WHEN dha.activity_date IS NULL THEN eha.host_activity_datelist
        WHEN NOT ARRAY_CONTAINS(eha.host_activity_datelist, dha.activity_date) 
            THEN ARRAY_CONCAT(eha.host_activity_datelist, ARRAY[dha.activity_date])
        ELSE eha.host_activity_datelist
    END AS host_activity_datelist,
    CURRENT_DATE AS date
FROM daily_host_activity dha
FULL OUTER JOIN existing_host_activity eha ON dha.host = eha.host;

-- 7. DDL for monthly reduced fact table host_activity_reduced
CREATE TABLE host_activity_reduced (
    month DATE,
    host STRING,
    hit_array ARRAY<INT>,
    unique_visitors_array ARRAY<INT>
);

-- 8. Incremental query to load host_activity_reduced day by day
WITH daily_metrics AS (
    SELECT 
        DATE_TRUNC('month', DATE(event_time)) AS month,
        host,
        DATE(event_time) AS activity_date,
        COUNT(*) AS daily_hits,
        COUNT(DISTINCT user_id) AS daily_unique_visitors
    FROM events
    WHERE DATE(event_time) = CURRENT_DATE  -- Today's data
    GROUP BY DATE_TRUNC('month', DATE(event_time)), host, DATE(event_time)
),
existing_monthly_data AS (
    SELECT 
        month,
        host,
        hit_array,
        unique_visitors_array
    FROM host_activity_reduced
    WHERE month = DATE_TRUNC('month', CURRENT_DATE)
),
day_of_month AS (
    SELECT 
        dm.*,
        DAY(dm.activity_date) AS day_number
    FROM daily_metrics dm
)
SELECT 
    dm.month,
    dm.host,
    CASE 
        WHEN emd.hit_array IS NULL THEN ARRAY[dm.daily_hits]
        ELSE ARRAY_CONCAT(
            SLICE(emd.hit_array, 1, dm.day_number - 1),
            ARRAY[dm.daily_hits],
            SLICE(emd.hit_array, dm.day_number + 1, ARRAY_LENGTH(emd.hit_array))
        )
    END AS hit_array,
    CASE 
        WHEN emd.unique_visitors_array IS NULL THEN ARRAY[dm.daily_unique_visitors]
        ELSE ARRAY_CONCAT(
            SLICE(emd.unique_visitors_array, 1, dm.day_number - 1),
            ARRAY[dm.daily_unique_visitors],
            SLICE(emd.unique_visitors_array, dm.day_number + 1, ARRAY_LENGTH(emd.unique_visitors_array))
        )
    END AS unique_visitors_array
FROM day_of_month dm
LEFT JOIN existing_monthly_data emd 
    ON dm.month = emd.month 
    AND dm.host = emd.host; 