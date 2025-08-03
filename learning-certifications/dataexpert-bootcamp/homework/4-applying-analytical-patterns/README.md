# Week 4: Applying Analytical Patterns

## 📋 Overview

This exercise demonstrates three key analytical patterns using NBA data with pure SQL implementations:

1. **State Change Tracking** - Tracking player career transitions
2. **GROUPING SETS Aggregations** - Efficient multi-dimensional analysis
3. **Window Functions** - Advanced time-series and ranking analytics

## 🎯 Objectives

### 1. State Change Tracking (`1_state_change_tracking.sql`)
Track player career state changes using window functions:
- **New**: Player entering the league
- **Retired**: Player leaving the league
- **Continued Playing**: Player staying active
- **Returned from Retirement**: Player coming back
- **Stayed Retired**: Player remaining inactive

### 2. GROUPING SETS Aggregations (`2_grouping_sets_aggregation.sql`)
Efficient multi-dimensional aggregations:
- **Player and Team**: Who scored most points for one team?
- **Player and Season**: Who scored most points in one season?
- **Team Only**: Which team won most games?

### 3. Window Functions Analytics (`3_window_functions.sql`)
Advanced analytics using window functions:
- **90-Game Win Streaks**: Most games won in 90-game stretch
- **Consecutive Scoring**: LeBron James consecutive 10+ point games

## 📁 Files Structure

```
4-applying-analytical-patterns/
├── README.md                           # This file
├── homework.md                         # Original homework description
├── 1_state_change_tracking.sql         # State change tracking query
├── 2_grouping_sets_aggregation.sql     # GROUPING SETS aggregation query
└── 3_window_functions.sql              # Window functions query
```

## 🛠️ SQL Implementation Details

### State Change Tracking Query
**Key Features:**
- Uses `LAG()` window function to compare current vs previous state
- `CASE` statements to categorize state transitions
- Tracks player lifecycle from rookie to retirement

**Key SQL Patterns:**
```sql
LAG(psc.is_active) OVER (
    PARTITION BY p.player_id 
    ORDER BY psc.season
) as prev_is_active
```

### GROUPING SETS Aggregation Query
**Key Features:**
- Efficient multi-dimensional aggregations
- `COALESCE()` for handling NULL values in grouped results
- Multiple aggregation levels in single query

**Key SQL Patterns:**
```sql
GROUP BY GROUPING SETS (
    (p.player_name, t.team_name),    -- player and team
    (p.player_name, ps.season),      -- player and season
    (t.team_name),                    -- team only
    ()                                -- grand total
)
```

### Window Functions Query
**Key Features:**
- Sliding window analysis (90-game stretches)
- Consecutive counting with `ROW_NUMBER()`
- Running totals with `SUM() OVER()`

**Key SQL Patterns:**
```sql
-- Sliding window
SUM(...) OVER (
    PARTITION BY t.team_id 
    ORDER BY g.game_date 
    ROWS BETWEEN 89 PRECEDING AND CURRENT ROW
)

-- Consecutive counting
ROW_NUMBER() OVER (
    PARTITION BY p.player_id, 
    CASE WHEN gd.points >= 10 THEN 1 ELSE 0 END
    ORDER BY gd.game_date
)
```

## 🚀 Usage

### Running the Queries
```bash
# Execute state change tracking
sqlite3 nba_data.db < 1_state_change_tracking.sql

# Execute GROUPING SETS aggregation
sqlite3 nba_data.db < 2_grouping_sets_aggregation.sql

# Execute window functions
sqlite3 nba_data.db < 3_window_functions.sql
```

### Expected Results

#### State Change Tracking
- Shows player career transitions over time
- Identifies new players, retirements, and comebacks
- Tracks career longevity patterns

#### GROUPING SETS Aggregation
- Multi-level aggregations (player-team, player-season, team-only)
- Performance metrics at different granularities
- Efficient single-query analysis

#### Window Functions
- Team performance in 90-game windows
- LeBron James scoring consistency analysis
- Time-based performance patterns

## 📊 Analytical Insights

### State Change Patterns
- **Career Transitions**: Track player lifecycle from rookie to retirement
- **Comeback Stories**: Identify players who returned from retirement
- **Career Longevity**: Analyze players who continued vs. retired

### Aggregation Insights
- **Player Performance**: Top scorers by team and season
- **Team Analysis**: Overall team performance metrics
- **Seasonal Trends**: Performance patterns across seasons

### Window Function Analytics
- **Win Streaks**: Teams with best 90-game performance
- **Scoring Consistency**: Players with longest scoring streaks
- **Performance Trends**: Time-based performance analysis

## 🔧 Technical Implementation

### Key SQL Patterns
1. **LAG() Window Function**: Track previous state
2. **GROUPING SETS**: Multi-dimensional aggregations
3. **ROW_NUMBER()**: Ranking and consecutive counting
4. **SUM() OVER()**: Running totals and sliding windows
5. **CASE Statements**: Complex conditional logic

### Performance Considerations
- **Window Functions**: Efficient for time-series analysis
- **GROUPING SETS**: Single query for multiple aggregation levels
- **CTEs**: Complex query organization and readability

## 📈 Business Value

### Data Engineering Applications
- **ETL Pipeline Design**: State change tracking for data quality
- **Data Warehouse Optimization**: Efficient aggregations with GROUPING SETS
- **Real-time Analytics**: Window functions for streaming data

### Analytics Use Cases
- **Player Career Analytics**: Track career progression and transitions
- **Performance Metrics**: Multi-dimensional performance analysis
- **Trend Analysis**: Time-series analysis for predictive insights

## 🎓 Learning Outcomes

### SQL Advanced Patterns
- **Window Functions**: LAG(), ROW_NUMBER(), SUM() OVER()
- **GROUPING SETS**: Efficient multi-dimensional aggregations
- **CTEs (Common Table Expressions)**: Complex query organization

### Data Engineering Skills
- **State Management**: Tracking entity state changes over time
- **Performance Optimization**: Efficient query patterns
- **Analytical Thinking**: Breaking down complex business questions

### Business Intelligence
- **Multi-dimensional Analysis**: Different levels of aggregation
- **Time-series Analytics**: Trend analysis and patterns
- **Data Storytelling**: Presenting insights clearly

---

**Author**: Murilo Biss  
**Date**: December 2024  
**Course**: DataExpert Bootcamp - Data Engineering 