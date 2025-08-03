-- Query using window functions for advanced analytics
-- 1. Most games won in a 90-game stretch
-- 2. LeBron James consecutive games with 10+ points


-- Query 1: Most games won in a 90-game stretch
WITH team_win_streaks AS (
    SELECT 
        t.team_name,
        g.season,
        g.game_date,
        CASE WHEN g.home_team_id = t.team_id 
             THEN CASE WHEN g.home_score > g.away_score THEN 1 ELSE 0 END
             ELSE CASE WHEN g.away_score > g.home_score THEN 1 ELSE 0 END
        END as is_win,
        SUM(CASE WHEN g.home_team_id = t.team_id 
                 THEN CASE WHEN g.home_score > g.away_score THEN 1 ELSE 0 END
                 ELSE CASE WHEN g.away_score > g.home_score THEN 1 ELSE 0 END
            END) OVER (
            PARTITION BY t.team_id 
            ORDER BY g.game_date 
            ROWS BETWEEN 89 PRECEDING AND CURRENT ROW
        ) as wins_in_90_game_stretch
    FROM games g
    JOIN teams t ON (g.home_team_id = t.team_id OR g.away_team_id = t.team_id)
    ORDER BY t.team_id, g.game_date
),
max_wins_90_stretch AS (
    SELECT 
        team_name,
        season,
        game_date,
        wins_in_90_game_stretch,
        ROW_NUMBER() OVER (
            PARTITION BY team_name 
            ORDER BY wins_in_90_game_stretch DESC
        ) as rn
    FROM team_win_streaks
),

-- Query 2: LeBron James consecutive games with 10+ points
lebron_consecutive_games AS (
    SELECT 
        p.player_name,
        gd.game_date,
        gd.points,
        CASE WHEN gd.points >= 10 THEN 1 ELSE 0 END as scored_10_plus,
        SUM(CASE WHEN gd.points >= 10 THEN 1 ELSE 0 END) OVER (
            PARTITION BY p.player_id 
            ORDER BY gd.game_date 
            ROWS UNBOUNDED PRECEDING
        ) as running_total_10_plus,
        ROW_NUMBER() OVER (
            PARTITION BY p.player_id 
            ORDER BY gd.game_date
        ) as game_number,
        ROW_NUMBER() OVER (
            PARTITION BY p.player_id, 
            CASE WHEN gd.points >= 10 THEN 1 ELSE 0 END
            ORDER BY gd.game_date
        ) as consecutive_count
    FROM game_details gd
    JOIN players p ON gd.player_id = p.player_id
    WHERE p.player_name = 'LeBron James'
    ORDER BY gd.game_date
)

-- Final results combining both analyses
SELECT 
    'Max Wins in 90-Game Stretch' as analysis_type,
    team_name,
    season,
    game_date,
    wins_in_90_game_stretch as metric_value
FROM max_wins_90_stretch 
WHERE rn = 1

UNION ALL

SELECT 
    'LeBron James Consecutive 10+ Point Games' as analysis_type,
    player_name as team_name,
    '' as season,
    game_date,
    consecutive_count as metric_value
FROM lebron_consecutive_games
WHERE scored_10_plus = 1
ORDER BY analysis_type, metric_value DESC; 