import pandas as pd
from supabase import create_client, Client
from sqlalchemy import create_engine, text
from loguru import logger
from typing import List, Dict, Any
import json

from ..config.config import settings, credential_manager
from ..models.models import Student, InstagramPost

class DatabaseManager:
    """Manages database connections and operations for Social FIT ETL."""
    
    def __init__(self):
        """Initialize database connections with professional credential management."""
        # Validate credentials before initializing
        if not credential_manager.validate_credentials():
            raise ValueError("Invalid Supabase credentials. Please check your configuration.")
        
        # Initialize Supabase client with validated credentials
        supabase_config = credential_manager.get_supabase_config()
        self.supabase: Client = create_client(supabase_config['url'], supabase_config['key'])
        
        # Initialize SQLAlchemy engine only if DATABASE_URL is provided and valid
        self.engine = None
        if settings.DATABASE_URL and settings.DATABASE_URL.strip():
            try:
                self.engine = create_engine(settings.DATABASE_URL)
                logger.info("SQLAlchemy engine initialized for direct database access")
            except Exception as e:
                logger.warning(f"Could not initialize SQLAlchemy engine: {e}")
                self.engine = None
        
        logger.info("Database manager initialized successfully")
        
    def test_connection(self) -> bool:
        """Test database connectivity."""
        try:
            # Test Supabase connection by trying to access a simple table
            result = self.supabase.table('students').select('id').limit(1).execute()
            logger.info("✅ Database connection successful")
            return True
        except Exception as e:
            logger.error(f"❌ Database connection failed: {e}")
            return False
        
    def create_tables(self):
        """Create necessary tables em Supabase schema 'social_fit' (apenas via SQLAlchemy se DATABASE_URL válido)."""
        try:
            schema_name = settings.DATABASE_SCHEMA
            # Só tenta criar via engine se DATABASE_URL estiver preenchido
            if settings.DATABASE_URL and self.engine:
                # Create schema if it doesn't exist
                create_schema_sql = f"""
                CREATE SCHEMA IF NOT EXISTS {schema_name};
                """
                # Create students table in social_fit schema
                students_table_sql = f"""
                CREATE TABLE IF NOT EXISTS {schema_name}.students (
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
                """
                # Create Instagram posts table in social_fit schema
                instagram_table_sql = f"""
                CREATE TABLE IF NOT EXISTS {schema_name}.instagram_posts (
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
                """
                # Create analytics table in social_fit schema
                analytics_table_sql = f"""
                CREATE TABLE IF NOT EXISTS {schema_name}.analytics (
                    id SERIAL PRIMARY KEY,
                    date DATE NOT NULL,
                    metric_name VARCHAR(100) NOT NULL,
                    metric_value JSONB NOT NULL,
                    created_at TIMESTAMP DEFAULT NOW()
                );
                """
                with self.engine.connect() as conn:
                    conn.execute(text(create_schema_sql))
                    conn.execute(text(students_table_sql))
                    conn.execute(text(instagram_table_sql))
                    conn.execute(text(analytics_table_sql))
                    conn.commit()
                logger.info(f"✅ Tables created in schema '{schema_name}'")
            else:
                logger.info(f"⚠️  Skipping direct database table creation (no valid DATABASE_URL)")
            # Test if tables exist
            self._ensure_tables_exist()
        except Exception as e:
            logger.error(f"Error creating tables: {e}")
            raise
    
    def _ensure_tables_exist(self):
        """Ensure required tables exist in the Supabase database (API: sem schema)."""
        required_tables = ['students', 'instagram_posts', 'analytics']
        for table in required_tables:
            try:
                self.supabase.table(table).select('*').limit(1).execute()
                logger.info(f"✅ Table '{table}' exists")
            except Exception as e:
                logger.warning(f"⚠️  Table '{table}' may not exist: {e}")
                logger.info(f"Please create table '{table}' in your Supabase dashboard (schema: social_fit)")
    
    def check_student_exists(self, student: Student) -> bool:
        """Check if a student already exists in the database."""
        try:
            result = self.supabase.table('students').select('id').eq('name', student.name).eq('birth_date', student.birth_date.date().isoformat()).execute()
            return len(result.data) > 0
        except Exception as e:
            logger.error(f"❌ Error checking student existence: {e}")
            return False
    
    def check_instagram_post_exists(self, post: InstagramPost) -> bool:
        """Check if an Instagram post already exists in the database."""
        try:
            result = self.supabase.table('instagram_posts').select('id').eq('post_date', post.date.date().isoformat()).eq('main_hashtag', post.main_hashtag).execute()
            return len(result.data) > 0
        except Exception as e:
            logger.error(f"❌ Error checking Instagram post existence: {e}")
            return False
    
    def check_analytics_exists(self, metric_name: str, date: str) -> bool:
        """Check if analytics for a specific metric and date already exists."""
        try:
            result = self.supabase.table('analytics').select('id').eq('metric_name', metric_name).eq('date', date).execute()
            return len(result.data) > 0
        except Exception as e:
            logger.error(f"❌ Error checking analytics existence: {e}")
            return False
    
    def insert_students(self, students: List[Student]) -> bool:
        """Insert students data into database with deduplication."""
        try:
            # Filter out existing students
            new_students = []
            for student in students:
                if not self.check_student_exists(student):
                    new_students.append(student)
                else:
                    logger.debug(f"⏭️  Skipping existing student: {student.name}")
            
            if not new_students:
                logger.info("ℹ️  No new students to insert (all already exist)")
                return True
            
            students_data = []
            for student in new_students:
                students_data.append({
                    'name': str(student.name),
                    'gender': str(student.gender.value),
                    'birth_date': student.birth_date.date().isoformat(),
                    'address': str(student.address),
                    'neighborhood': str(student.neighborhood),
                    'plan_type': str(student.plan_type.value),
                    'gympass': bool(student.gympass),
                    'monthly_value': float(student.monthly_value),
                    'total_value': float(student.total_value),
                    'plan_start_date': student.plan_start_date.date().isoformat(),
                    'active_plan': bool(student.active_plan)
                })
            
            batch_size = settings.BATCH_SIZE
            
            for i in range(0, len(students_data), batch_size):
                batch = students_data[i:i + batch_size]
                result = self.supabase.table('students').insert(batch).execute()
                logger.info(f"Inserted batch {i//batch_size + 1} of new students")
            
            logger.info(f"✅ Inserted {len(new_students)} new students (skipped {len(students) - len(new_students)} existing)")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error inserting students: {e}")
            return False
    
    def insert_instagram_posts(self, posts: List[InstagramPost]) -> bool:
        """Insert Instagram posts data into database with deduplication."""
        try:
            # Filter out existing posts
            new_posts = []
            for post in posts:
                if not self.check_instagram_post_exists(post):
                    new_posts.append(post)
                else:
                    logger.debug(f"⏭️  Skipping existing post: {post.date.date()} - {post.main_hashtag}")
            
            if not new_posts:
                logger.info("ℹ️  No new Instagram posts to insert (all already exist)")
                return True
            
            posts_data = []
            for post in new_posts:
                engagement_rate = (post.likes + post.comments + post.saves) / post.reach if post.reach > 0 else 0
                posts_data.append({
                    'post_date': post.date.date().isoformat(),
                    'likes': int(post.likes),
                    'comments': int(post.comments),
                    'saves': int(post.saves),
                    'reach': int(post.reach),
                    'profile_visits': int(post.profile_visits),
                    'new_followers': int(post.new_followers),
                    'main_hashtag': str(post.main_hashtag),
                    'engagement_rate': float(engagement_rate)
                })
            
            batch_size = settings.BATCH_SIZE
            
            for i in range(0, len(posts_data), batch_size):
                batch = posts_data[i:i + batch_size]
                result = self.supabase.table('instagram_posts').insert(batch).execute()
                logger.info(f"Inserted batch {i//batch_size + 1} of new Instagram posts")
            
            logger.info(f"✅ Inserted {len(new_posts)} new Instagram posts (skipped {len(posts) - len(new_posts)} existing)")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error inserting Instagram posts: {e}")
            return False
    
    def insert_analytics(self, analytics_data: Dict[str, Any]) -> bool:
        """Insert analytics data into database with deduplication."""
        try:
            # Convert date to string if it's a date object
            date_value = analytics_data.get('date')
            if hasattr(date_value, 'isoformat'):
                date_value = date_value.isoformat()
            
            metric_name = analytics_data.get('metric_name')
            
            # Check if analytics for this metric and date already exists
            if self.check_analytics_exists(metric_name, date_value):
                logger.info(f"ℹ️  Analytics for {metric_name} on {date_value} already exists, skipping")
                return True
            
            analytics_record = {
                'date': date_value,
                'metric_name': metric_name,
                'metric_value': json.dumps(analytics_data.get('metric_value'), default=str)
            }
            
            result = self.supabase.table('analytics').insert(analytics_record).execute()
            logger.info(f"✅ Inserted analytics data: {metric_name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error inserting analytics: {e}")
            return False
    
    def get_students(self) -> pd.DataFrame:
        """Retrieve students data from database."""
        try:
            result = self.supabase.table('students').select('*').execute()
            df = pd.DataFrame(result.data)
            logger.info(f"✅ Retrieved {len(df)} students from database")
            return df
        except Exception as e:
            logger.error(f"❌ Error retrieving students: {e}")
            return pd.DataFrame()
    
    def get_instagram_posts(self) -> pd.DataFrame:
        """Retrieve Instagram posts data from database."""
        try:
            result = self.supabase.table('instagram_posts').select('*').execute()
            df = pd.DataFrame(result.data)
            logger.info(f"✅ Retrieved {len(df)} Instagram posts from database")
            return df
        except Exception as e:
            logger.error(f"❌ Error retrieving Instagram posts: {e}")
            return pd.DataFrame()
    
    def get_analytics(self, metric_name: str = None) -> pd.DataFrame:
        """Retrieve analytics data from database."""
        try:
            query = self.supabase.table('analytics').select('*')
            if metric_name:
                query = query.eq('metric_name', metric_name)
            result = query.execute()
            df = pd.DataFrame(result.data)
            logger.info(f"✅ Retrieved {len(df)} analytics records from database")
            return df
        except Exception as e:
            logger.error(f"❌ Error retrieving analytics: {e}")
            return pd.DataFrame()
    
    def clear_tables(self, table_names: List[str] = None):
        """Clear data from specified tables (use with caution)."""
        if table_names is None:
            table_names = ['students', 'instagram_posts', 'analytics']
        for table in table_names:
            try:
                self.supabase.table(table).delete().neq('id', 0).execute()
                logger.info(f"✅ Cleared table: {table}")
            except Exception as e:
                logger.error(f"❌ Error clearing table {table}: {e}") 