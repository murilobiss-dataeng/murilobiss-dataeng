-- Query for state change tracking of players
-- Tracks player career transitions using window functions

WITH player_state_changes AS (
    SELECT 
        p.player_id,
        p.player_name,
        psc.season,
        psc.team_id,
        psc.is_active,
        LAG(psc.is_active) OVER (
            PARTITION BY p.player_id 
            ORDER BY psc.season
        ) as prev_is_active,
        CASE 
            WHEN LAG(psc.is_active) OVER (
                PARTITION BY p.player_id 
                ORDER BY psc.season
            ) IS NULL AND psc.is_active = 1 
            THEN 'New'
            WHEN LAG(psc.is_active) OVER (
                PARTITION BY p.player_id 
                ORDER BY psc.season
            ) = 1 AND psc.is_active = 0 
            THEN 'Retired'
            WHEN LAG(psc.is_active) OVER (
                PARTITION BY p.player_id 
                ORDER BY psc.season
            ) = 1 AND psc.is_active = 1 
            THEN 'Continued Playing'
            WHEN LAG(psc.is_active) OVER (
                PARTITION BY p.player_id 
                ORDER BY psc.season
            ) = 0 AND psc.is_active = 1 
            THEN 'Returned from Retirement'
            WHEN LAG(psc.is_active) OVER (
                PARTITION BY p.player_id 
                ORDER BY psc.season
            ) = 0 AND psc.is_active = 0 
            THEN 'Stayed Retired'
            ELSE 'Unknown'
        END as state_change
    FROM players p
    JOIN players_scd psc ON p.player_id = psc.player_id
    ORDER BY p.player_id, psc.season
)
SELECT 
    player_id,
    player_name,
    season,
    team_id,
    state_change
FROM player_state_changes
WHERE state_change != 'Unknown'
ORDER BY player_id, season; 