# Week 1 Homework - Dimensional Data Modeling

## What I did

Had to create a dimensional data model for the `actor_films` dataset. Basically needed to build two tables:
- `actors` table to store current actor info with their films
- `actors_history_scd` table to track how actors' quality and status changed over time

## My approach

### 1. Actors Table
Created a table that stores:
- Actor basic info (id, name)
- Films as an array of structs (film name, votes, rating, film id)
- Quality class based on their most recent year's average rating
- Whether they're currently active (made films this year)

The quality classes are:
- **star**: avg rating > 8
- **good**: avg rating 7-8
- **average**: avg rating 6-7  
- **bad**: avg rating ≤ 6

### 2. Populating the Actors Table
Wrote a query that:
- Groups films by actor and year
- Calculates average rating per year
- Determines quality based on the most recent year they appeared
- Sets active status if they made films in the latest year overall

### 3. SCD Table Structure
For tracking historical changes, created a table with:
- All the actor info
- Start and end dates for when each record was valid
- A current flag to mark the active record

### 4. Backfill Query
This was the hardest part - had to create historical records for all actors across all years. Used:
- Window functions to get the next year's start date as the end date
- A far future date (9999-12-31) for current records
- The current flag to identify active records

### 5. Incremental Updates
This handles new data coming in. The logic:
- Compare new data with existing current records
- If something changed (quality class or active status), close the old record and create a new one
- If nothing changed, keep the existing record
- Add completely new actors

## Technical stuff I used

- **ARRAY<STRUCT>** for storing multiple films per actor
- **Window functions** (LEAD, MAX OVER) for temporal logic
- **CTEs** to break down complex queries
- **CASE statements** for quality classification
- **UNION ALL** to combine different record types

## Challenges I faced

The hardest part was definitely the incremental update query. Had to think through:
- How to identify what changed
- How to preserve historical records
- How to handle new actors vs existing ones

Ended up breaking it into several CTEs to make it clearer:
1. Get new data
2. Get existing current records
3. Find changed records
4. Find unchanged records  
5. Find brand new actors
6. Combine everything

The backfill query was also tricky because I had to figure out how to use LEAD() properly to get the end dates.

## Files
- `solution.sql` - All the queries
- `README.md` - This explanation 