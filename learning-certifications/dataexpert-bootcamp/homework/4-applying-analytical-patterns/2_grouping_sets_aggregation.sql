-- Week 4: GROUPING SETS Aggregation Query
-- DataExpert Bootcamp - Data Engineering
-- Author: Murilo Biss
-- Date: December 2024

-- Query using GROUPING SETS for efficient aggregations
-- Multi-dimensional analysis of game_details data

SELECT 
    COALESCE(p.player_name, 'ALL PLAYERS') as player_name,
    COALESCE(t.team_name, 'ALL TEAMS') as team_name,
    COALESCE(ps.season, 'ALL SEASONS') as season,
    COUNT(*) as total_games,
    SUM(gd.points) as total_points,
    AVG(gd.points) as avg_points,
    MAX(gd.points) as max_points,
    SUM(gd.rebounds) as total_rebounds,
    SUM(gd.assists) as total_assists
FROM game_details gd
JOIN players p ON gd.player_id = p.player_id
JOIN teams t ON gd.team_id = t.team_id
JOIN player_seasons ps ON gd.player_id = ps.player_id 
    AND gd.season = ps.season
GROUP BY GROUPING SETS (
    (p.player_name, t.team_name),    -- player and team
    (p.player_name, ps.season),      -- player and season
    (t.team_name),                    -- team only
    ()                                -- grand total
)
ORDER BY 
    CASE WHEN p.player_name IS NULL THEN 1 ELSE 0 END,
    p.player_name,
    CASE WHEN t.team_name IS NULL THEN 1 ELSE 0 END,
    t.team_name,
    CASE WHEN ps.season IS NULL THEN 1 ELSE 0 END,
    ps.season; 