#!/usr/bin/env python3
"""
Supabase Setup Script for Social FIT ETL Pipeline

This script sets up the necessary tables and configurations in Supabase
for the Social FIT data intelligence project.
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import credential_manager
from database import DatabaseManager
from loguru import logger

def setup_supabase_tables():
    """Set up the required tables in Supabase."""
    print("🏗️  Setting up Supabase tables for Social FIT...")
    
    try:
        # Initialize database manager
        db_manager = DatabaseManager()
        
        # Test connection
        if not db_manager.test_connection():
            print("❌ Failed to connect to Supabase")
            return False
        
        # Create tables
        db_manager.create_tables()
        
        print("✅ Supabase setup completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error setting up Supabase: {e}")
        return False

def create_sql_migrations():
    """Create SQL migration files for manual table creation."""
    print("📝 Creating SQL migration files...")
    
    migrations_dir = Path("migrations")
    migrations_dir.mkdir(exist_ok=True)
    
    # Students table migration
    students_migration = """
-- Migration: Create students table
-- Date: 2025-01-01
-- Description: Create students table for Social FIT ETL pipeline

CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    gender VARCHAR(1) NOT NULL,
    birth_date DATE NOT NULL,
    address TEXT NOT NULL,
    neighborhood VARCHAR(100) NOT NULL,
    plan_type VARCHAR(20) NOT NULL,
    gympass BOOLEAN DEFAULT FALSE,
    monthly_value DECIMAL(10,2) NOT NULL,
    total_value DECIMAL(10,2) NOT NULL,
    plan_start_date DATE NOT NULL,
    active_plan BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_students_neighborhood ON students(neighborhood);
CREATE INDEX IF NOT EXISTS idx_students_plan_type ON students(plan_type);
CREATE INDEX IF NOT EXISTS idx_students_active_plan ON students(active_plan);
CREATE INDEX IF NOT EXISTS idx_students_plan_start_date ON students(plan_start_date);

-- Add comments for documentation
COMMENT ON TABLE students IS 'Student enrollment data for Social FIT gym';
COMMENT ON COLUMN students.name IS 'Full name of the student';
COMMENT ON COLUMN students.gender IS 'Gender: M for Male, F for Female';
COMMENT ON COLUMN students.neighborhood IS 'Neighborhood in Curitiba';
COMMENT ON COLUMN students.plan_type IS 'Plan type: Mensal, Trimestral, or Anual';
COMMENT ON COLUMN students.gympass IS 'Whether student has Gympass';
"""
    
    # Instagram posts table migration
    instagram_migration = """
-- Migration: Create instagram_posts table
-- Date: 2025-01-01
-- Description: Create Instagram posts table for Social FIT ETL pipeline

CREATE TABLE IF NOT EXISTS instagram_posts (
    id SERIAL PRIMARY KEY,
    post_date DATE NOT NULL,
    likes INTEGER NOT NULL,
    comments INTEGER NOT NULL,
    saves INTEGER NOT NULL,
    reach INTEGER NOT NULL,
    profile_visits INTEGER NOT NULL,
    new_followers INTEGER NOT NULL,
    main_hashtag VARCHAR(100) NOT NULL,
    engagement_rate DECIMAL(5,4),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_instagram_post_date ON instagram_posts(post_date);
CREATE INDEX IF NOT EXISTS idx_instagram_main_hashtag ON instagram_posts(main_hashtag);
CREATE INDEX IF NOT EXISTS idx_instagram_engagement_rate ON instagram_posts(engagement_rate);

-- Add comments for documentation
COMMENT ON TABLE instagram_posts IS 'Instagram post performance data for Social FIT';
COMMENT ON COLUMN instagram_posts.engagement_rate IS 'Calculated engagement rate (likes + comments + saves) / reach';
COMMENT ON COLUMN instagram_posts.main_hashtag IS 'Primary hashtag used in the post';
"""
    
    # Analytics table migration
    analytics_migration = """
-- Migration: Create analytics table
-- Date: 2025-01-01
-- Description: Create analytics table for Social FIT ETL pipeline

CREATE TABLE IF NOT EXISTS analytics (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    metric_name VARCHAR(100) NOT NULL,
    metric_value JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_analytics_date ON analytics(date);
CREATE INDEX IF NOT EXISTS idx_analytics_metric_name ON analytics(metric_name);
CREATE INDEX IF NOT EXISTS idx_analytics_metric_value ON analytics USING GIN(metric_value);

-- Add comments for documentation
COMMENT ON TABLE analytics IS 'Analytics and insights data for Social FIT';
COMMENT ON COLUMN analytics.metric_name IS 'Name of the metric (e.g., comprehensive_analytics)';
COMMENT ON COLUMN analytics.metric_value IS 'JSON data containing the metric values';
"""
    
    # Write migration files
    with open(migrations_dir / "001_create_students_table.sql", "w") as f:
        f.write(students_migration)
    
    with open(migrations_dir / "002_create_instagram_posts_table.sql", "w") as f:
        f.write(instagram_migration)
    
    with open(migrations_dir / "003_create_analytics_table.sql", "w") as f:
        f.write(analytics_migration)
    
    print("✅ SQL migration files created in migrations/ directory")
    return True

def create_supabase_dashboard_instructions():
    """Create instructions for setting up tables in Supabase dashboard."""
    print("📋 Creating Supabase dashboard setup instructions...")
    
    instructions = """
# Supabase Dashboard Setup Instructions

## 1. Access Your Supabase Project
1. Go to https://supabase.com/dashboard
2. Select your project: rwdydxswgmzgdivriyarq
3. Navigate to the SQL Editor

## 2. Create Tables
Run the following SQL commands in the SQL Editor:

### Students Table
```sql
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    gender VARCHAR(1) NOT NULL,
    birth_date DATE NOT NULL,
    address TEXT NOT NULL,
    neighborhood VARCHAR(100) NOT NULL,
    plan_type VARCHAR(20) NOT NULL,
    gympass BOOLEAN DEFAULT FALSE,
    monthly_value DECIMAL(10,2) NOT NULL,
    total_value DECIMAL(10,2) NOT NULL,
    plan_start_date DATE NOT NULL,
    active_plan BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Instagram Posts Table
```sql
CREATE TABLE instagram_posts (
    id SERIAL PRIMARY KEY,
    post_date DATE NOT NULL,
    likes INTEGER NOT NULL,
    comments INTEGER NOT NULL,
    saves INTEGER NOT NULL,
    reach INTEGER NOT NULL,
    profile_visits INTEGER NOT NULL,
    new_followers INTEGER NOT NULL,
    main_hashtag VARCHAR(100) NOT NULL,
    engagement_rate DECIMAL(5,4),
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Analytics Table
```sql
CREATE TABLE analytics (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    metric_name VARCHAR(100) NOT NULL,
    metric_value JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## 3. Set Up Row Level Security (RLS)
For production use, consider enabling RLS on your tables:

```sql
ALTER TABLE students ENABLE ROW LEVEL SECURITY;
ALTER TABLE instagram_posts ENABLE ROW LEVEL SECURITY;
ALTER TABLE analytics ENABLE ROW LEVEL SECURITY;
```

## 4. Create Policies (Optional)
Create policies to control access to your data:

```sql
-- Example policy for read access
CREATE POLICY "Allow read access" ON students FOR SELECT USING (true);
CREATE POLICY "Allow read access" ON instagram_posts FOR SELECT USING (true);
CREATE POLICY "Allow read access" ON analytics FOR SELECT USING (true);
```

## 5. Verify Setup
After creating the tables, you can verify them in the Table Editor section of your Supabase dashboard.

## 6. Test Connection
Run the ETL pipeline to test the connection:
```bash
python main.py run
```
"""
    
    with open("SUPABASE_SETUP.md", "w") as f:
        f.write(instructions)
    
    print("✅ Supabase setup instructions created: SUPABASE_SETUP.md")
    return True

def main():
    """Main setup function."""
    print("=" * 60)
    print("🚀 SUPABASE SETUP FOR SOCIAL FIT ETL PIPELINE")
    print("=" * 60)
    
    # Validate credentials
    if not credential_manager.validate_credentials():
        print("❌ Invalid Supabase credentials")
        print("Please check your configuration in config.py")
        return False
    
    print("✅ Supabase credentials validated")
    
    # Create migration files
    create_sql_migrations()
    
    # Create setup instructions
    create_supabase_dashboard_instructions()
    
    # Try to set up tables programmatically
    print("\n🔄 Attempting to set up tables programmatically...")
    if setup_supabase_tables():
        print("✅ Tables created successfully!")
    else:
        print("⚠️  Automatic table creation failed")
        print("📝 Please follow the instructions in SUPABASE_SETUP.md")
        print("📝 Or run the SQL files in the migrations/ directory")
    
    print("\n" + "=" * 60)
    print("✅ SUPABASE SETUP COMPLETED!")
    print("=" * 60)
    print("\n📋 Next steps:")
    print("1. Check SUPABASE_SETUP.md for manual setup instructions")
    print("2. Run: python main.py run")
    print("3. View dashboard: python dashboard.py")
    
    return True

if __name__ == "__main__":
    main() 