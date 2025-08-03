# Social FIT Data Intelligence Platform - API Documentation

## Overview

This document describes the API and usage patterns for the Social FIT Data Intelligence Platform.

## Core Modules

### ETL Pipeline (`src.etl`)

The ETL pipeline is responsible for extracting, transforming, and loading data from various sources.

#### SocialFITETL Class

```python
from src.etl import SocialFITETL

# Initialize ETL pipeline
etl = SocialFITETL()

# Run complete pipeline
success = etl.run_full_pipeline()

# Run incremental update
success = etl.run_incremental_update()
```

**Methods:**

- `extract_data()` - Extract data from CSV files
- `transform_students(df)` - Transform student data
- `transform_instagram(df)` - Transform Instagram data
- `load_data(students, posts)` - Load data to database
- `generate_analytics()` - Generate analytics and insights
- `run_full_pipeline()` - Run complete ETL process
- `run_incremental_update()` - Run incremental update

### Database Management (`src.database`)

Database operations and management for Supabase integration.

#### DatabaseManager Class

```python
from src.database import DatabaseManager

# Initialize database manager
db = DatabaseManager()

# Test connection
success = db.test_connection()

# Create tables
db.create_tables()

# Insert data
success = db.insert_students(students_list)
success = db.insert_instagram_posts(posts_list)

# Query data
students_df = db.get_students()
posts_df = db.get_instagram_posts()
analytics_df = db.get_analytics()
```

**Methods:**

- `test_connection()` - Test database connectivity
- `create_tables()` - Create database tables
- `insert_students(students)` - Insert student data
- `insert_instagram_posts(posts)` - Insert Instagram data
- `insert_analytics(data)` - Insert analytics data
- `get_students()` - Retrieve student data
- `get_instagram_posts()` - Retrieve Instagram data
- `get_analytics()` - Retrieve analytics data
- `clear_tables()` - Clear table data

### Analytics Engine (`src.analytics`)

Business intelligence and analytics generation.

#### AnalyticsEngine Class

```python
from src.analytics import AnalyticsEngine

# Initialize analytics engine
analytics = AnalyticsEngine()

# Analyze student data
student_analytics = analytics.analyze_students(students_df)

# Analyze Instagram data
instagram_analytics = analytics.analyze_instagram(instagram_df)

# Cross-platform analysis
cross_analytics = analytics.cross_platform_analysis(students_df, instagram_df)

# Generate insights
insights = analytics.generate_actionable_insights(
    student_analytics, 
    instagram_analytics, 
    cross_analytics
)
```

**Methods:**

- `analyze_students(df)` - Analyze student data
- `analyze_instagram(df)` - Analyze Instagram data
- `cross_platform_analysis(students_df, instagram_df)` - Cross-platform correlation
- `generate_actionable_insights(...)` - Generate business insights

### Data Models (`src.models`)

Pydantic models for data validation and structure.

#### Student Model

```python
from src.models import Student

student = Student(
    id=1,
    name="João Silva",
    gender="M",
    birth_date=datetime(1990, 1, 1),
    address="Rua das Flores, 123",
    neighborhood="Centro",
    plan_type="Mensal",
    gympass=True,
    monthly_value=89.90,
    total_value=89.90,
    plan_start_date=datetime(2024, 1, 1),
    active_plan=True
)
```

#### Instagram Post Model

```python
from src.models import InstagramPost

post = InstagramPost(
    date=datetime(2024, 1, 1),
    likes=150,
    comments=25,
    saves=10,
    reach=1000,
    profile_visits=50,
    new_followers=15,
    main_hashtag="#socialfit"
)
```

#### ColumnMapper

Automatic column mapping for CSV files.

```python
from src.models import ColumnMapper

# Create column mapping
mapping = ColumnMapper.create_column_mapping(df)

# Transform dataframe
transformed_df = ColumnMapper.transform_dataframe(df, mapping)
```

### Configuration (`src.config`)

Configuration management and credential handling.

```python
from src.config import settings, credential_manager

# Access settings
supabase_url = settings.SUPABASE_URL
batch_size = settings.BATCH_SIZE

# Validate credentials
is_valid = credential_manager.validate_credentials()

# Get Supabase config
config = credential_manager.get_supabase_config()
```

## Usage Examples

### Complete ETL Pipeline

```python
#!/usr/bin/env python3
"""
Complete ETL pipeline example
"""

import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.etl import SocialFITETL
from loguru import logger

def main():
    # Initialize ETL pipeline
    etl = SocialFITETL()
    
    # Run complete pipeline
    success = etl.run_full_pipeline()
    
    if success:
        logger.info("✅ ETL pipeline completed successfully!")
    else:
        logger.error("❌ ETL pipeline failed!")
        return False
    
    return True

if __name__ == "__main__":
    main()
```

### Custom Analytics

```python
#!/usr/bin/env python3
"""
Custom analytics example
"""

from src.analytics import AnalyticsEngine
from src.database import DatabaseManager
import pandas as pd

def custom_analytics():
    # Initialize components
    db = DatabaseManager()
    analytics = AnalyticsEngine()
    
    # Get data
    students_df = db.get_students()
    instagram_df = db.get_instagram_posts()
    
    # Generate custom analytics
    student_analytics = analytics.analyze_students(students_df)
    instagram_analytics = analytics.analyze_instagram(instagram_df)
    
    # Print results
    print(f"Total students: {student_analytics.total_students}")
    print(f"Active students: {student_analytics.active_students}")
    print(f"Total Instagram posts: {instagram_analytics.total_posts}")
    print(f"Average engagement rate: {instagram_analytics.average_engagement_rate:.2%}")

if __name__ == "__main__":
    custom_analytics()
```

### Data Validation

```python
#!/usr/bin/env python3
"""
Data validation example
"""

from src.models import Student, InstagramPost, ColumnMapper
import pandas as pd

def validate_data():
    # Load data
    students_df = pd.read_csv("data/social_fit_alunos.csv")
    
    # Create column mapping
    mapping = ColumnMapper.create_column_mapping(students_df)
    
    # Transform data
    transformed_df = ColumnMapper.transform_dataframe(students_df, mapping)
    
    # Validate with Pydantic models
    students = []
    for _, row in transformed_df.iterrows():
        try:
            student = Student(**row.to_dict())
            students.append(student)
            print(f"✅ Validated student: {student.name}")
        except Exception as e:
            print(f"❌ Validation error: {e}")
    
    print(f"Successfully validated {len(students)} students")

if __name__ == "__main__":
    validate_data()
```

## Error Handling

The platform includes comprehensive error handling:

```python
from src.database import DatabaseManager
from loguru import logger

try:
    db = DatabaseManager()
    success = db.test_connection()
    
    if success:
        logger.info("✅ Database connection successful")
    else:
        logger.error("❌ Database connection failed")
        
except Exception as e:
    logger.error(f"❌ Critical error: {e}")
```

## Configuration

### Environment Variables

Required environment variables:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# Application Configuration
DEBUG=True
LOG_LEVEL=INFO
BATCH_SIZE=100
```

### Database Schema

The platform uses the following database schema:

```sql
-- Students table
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

-- Instagram posts table
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

-- Analytics table
CREATE TABLE analytics (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    metric_name VARCHAR(100) NOT NULL,
    metric_value JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## Best Practices

1. **Error Handling**: Always wrap API calls in try-catch blocks
2. **Logging**: Use the provided logging configuration
3. **Data Validation**: Validate data before processing
4. **Batch Processing**: Use batch processing for large datasets
5. **Configuration**: Use environment variables for sensitive data
6. **Testing**: Write comprehensive tests for all components

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Check Supabase credentials in `.env`
   - Verify network connectivity
   - Ensure tables exist in database

2. **Data Validation Errors**
   - Check CSV file format
   - Verify column names match expected schema
   - Review data types and constraints

3. **Memory Issues**
   - Reduce batch size in configuration
   - Process data in smaller chunks
   - Monitor system resources

### Debug Mode

Enable debug mode for detailed logging:

```python
import os
os.environ["DEBUG"] = "True"
os.environ["LOG_LEVEL"] = "DEBUG"
```

## Support

For additional support:

- Check the main README.md file
- Review test files for usage examples
- Create an issue in the GitHub repository
- Contact the development team 