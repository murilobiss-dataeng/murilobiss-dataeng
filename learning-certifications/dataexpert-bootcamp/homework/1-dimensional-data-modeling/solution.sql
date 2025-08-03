-- Week 1 Homework - Dimensional Data Modeling
-- working with actor_films dataset
-- need to create actors table and SCD table for history tracking

-- 1. actors table
CREATE TABLE actors (
    actorid INT,
    actor STRING,
    films ARRAY<STRUCT<
        film: STRING,
        votes: INT,
        rating: DECIMAL(3,1),
        filmid: INT
    >>,
    quality_class STRING,
    is_active BOOLEAN
);

-- 2. populate actors table
-- group by actor and year, calculate quality based on most recent year
WITH films_grouped AS (
    SELECT 
        actorid,
        actor,
        year,
        -- collect films for this actor in this year
        -- using COLLECT_LIST to group them
        COLLECT_LIST(
            STRUCT(
                film,
                votes,
                rating,
                filmid
            )
        ) AS films,
        AVG(rating) AS avg_rating,
        -- get latest year for this actor
        -- need this to determine if they're active
        MAX(year) OVER (PARTITION BY actorid) AS max_year
    FROM actor_films
    GROUP BY actorid, actor, year
),
quality_analysis AS (
    SELECT 
        actorid,
        actor,
        films,
        -- quality based on most recent year avg rating
        CASE 
            WHEN avg_rating > 8 THEN 'star'
            WHEN avg_rating > 7 AND avg_rating <= 8 THEN 'good'
            WHEN avg_rating > 6 AND avg_rating <= 7 THEN 'average'
            ELSE 'bad'
        END AS quality_class,
        -- active if they made films in latest year
        (year = max_year) AS is_active
    FROM films_grouped
)
SELECT * FROM quality_analysis;

-- 3. SCD table for history tracking
CREATE TABLE actors_history_scd (
    actorid INT,
    actor STRING,
    quality_class STRING,
    is_active BOOLEAN,
    start_date DATE,
    end_date DATE,
    current_flag BOOLEAN
);

-- 4. backfill SCD table
-- create historical records for all actors
-- this was tricky to figure out
WITH actor_yearly AS (
    SELECT 
        actorid,
        actor,
        year,
        AVG(rating) AS avg_rating
    FROM actor_films
    GROUP BY actorid, actor, year
),
quality_by_year AS (
    SELECT 
        actorid,
        actor,
        year,
        CASE 
            WHEN avg_rating > 8 THEN 'star'
            WHEN avg_rating > 7 AND avg_rating <= 8 THEN 'good'
            WHEN avg_rating > 6 AND avg_rating <= 7 THEN 'average'
            ELSE 'bad'
        END AS quality_class,
        -- check if this is most recent year
        (year = (SELECT MAX(year) FROM actor_films)) AS is_active
    FROM actor_yearly
),
scd_temp AS (
    SELECT 
        actorid,
        actor,
        quality_class,
        is_active,
        CAST(CONCAT(year, '-01-01') AS DATE) AS start_date,
        -- use LEAD to get next year start as end date
        LEAD(CAST(CONCAT(year, '-01-01') AS DATE)) OVER (
            PARTITION BY actorid 
            ORDER BY year
        ) AS end_date
    FROM quality_by_year
)
SELECT 
    actorid,
    actor,
    quality_class,
    is_active,
    start_date,
    -- if no end_date (most recent), use far future
    COALESCE(end_date, CAST('9999-12-31' AS DATE)) AS end_date,
    -- current if no end_date
    (end_date IS NULL) AS current_flag
FROM scd_temp;

-- 5. incremental update for SCD
-- handle new data while keeping history
-- most complex part of the homework
WITH latest_data AS (
    -- get latest year data
    SELECT 
        actorid,
        actor,
        quality_class,
        is_active,
        CURRENT_DATE AS start_date
    FROM actors
    WHERE year = (SELECT MAX(year) FROM actor_films)
),
existing_current AS (
    -- get existing current records and close them
    SELECT 
        actorid,
        actor,
        quality_class,
        is_active,
        start_date,
        -- close current records
        CASE 
            WHEN current_flag = TRUE THEN CURRENT_DATE - 1
            ELSE end_date
        END AS end_date,
        FALSE AS current_flag
    FROM actors_history_scd
    WHERE current_flag = TRUE
),
records_with_changes AS (
    -- records where quality_class or is_active changed
    SELECT 
        ld.actorid,
        ld.actor,
        ld.quality_class,
        ld.is_active,
        ld.start_date,
        CAST('9999-12-31' AS DATE) AS end_date,
        TRUE AS current_flag
    FROM latest_data ld
    INNER JOIN existing_current ec ON ld.actorid = ec.actorid
    WHERE ld.quality_class != ec.quality_class 
       OR ld.is_active != ec.is_active
),
records_no_changes AS (
    -- records that didn't change - keep existing
    SELECT 
        ec.actorid,
        ec.actor,
        ec.quality_class,
        ec.is_active,
        ec.start_date,
        ec.end_date,
        ec.current_flag
    FROM existing_current ec
    INNER JOIN latest_data ld ON ec.actorid = ld.actorid
    WHERE ld.quality_class = ec.quality_class 
      AND ld.is_active = ec.is_active
),
new_actors_only AS (
    -- completely new actors
    SELECT 
        ld.actorid,
        ld.actor,
        ld.quality_class,
        ld.is_active,
        ld.start_date,
        CAST('9999-12-31' AS DATE) AS end_date,
        TRUE AS current_flag
    FROM latest_data ld
    LEFT JOIN existing_current ec ON ld.actorid = ec.actorid
    WHERE ec.actorid IS NULL
)
-- combine all records
SELECT * FROM existing_current WHERE current_flag = FALSE
UNION ALL
SELECT * FROM records_no_changes
UNION ALL
SELECT * FROM records_with_changes
UNION ALL
SELECT * FROM new_actors_only; 