import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Dict, Any
from loguru import logger
import os

from src.config import settings
from src.models import Student, InstagramPost
from src.database import DatabaseManager
from src.analytics import AnalyticsEngine

class SocialFITETL:
    """Main ETL pipeline for Social FIT data integration."""
    
    def __init__(self):
        """Initialize ETL pipeline."""
        self.db_manager = DatabaseManager()
        self.analytics_engine = AnalyticsEngine()
        
        # Configure logging
        logger.add("logs/etl_{time}.log", rotation="1 day", retention="7 days", level=settings.LOG_LEVEL)
        
    def extract_data(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Extract data from CSV files."""
        try:
            # Read students data
            students_file = os.path.join(settings.DATA_DIR, settings.STUDENTS_FILE)
            students_df = pd.read_csv(students_file)
            logger.info(f"Extracted {len(students_df)} student records")
            
            # Read Instagram data
            instagram_file = os.path.join(settings.DATA_DIR, settings.INSTAGRAM_FILE)
            instagram_df = pd.read_csv(instagram_file)
            logger.info(f"Extracted {len(instagram_df)} Instagram posts")
            
            return students_df, instagram_df
            
        except Exception as e:
            logger.error(f"Error extracting data: {e}")
            raise
    
    def transform_students(self, students_df: pd.DataFrame) -> List[Student]:
        """Transform students data into Pydantic models."""
        try:
            students = []
            
            # Clean and transform data
            students_df['Data de Nascimento'] = pd.to_datetime(students_df['Data de Nascimento'])
            students_df['Data Início Plano'] = pd.to_datetime(students_df['Data Início Plano'])
            
            # Convert boolean columns
            students_df['Gympass'] = students_df['Gympass'].apply(lambda x: str(x).strip().lower() == 'true')
            students_df['Plano Ativo'] = students_df['Plano Ativo'].apply(lambda x: str(x).strip().lower() == 'true')
            
            # Convert to Pydantic models
            for _, row in students_df.iterrows():
                try:
                    student = Student(**row.to_dict())
                    students.append(student)
                except Exception as e:
                    logger.warning(f"Error processing student row: {e}")
                    continue
            
            logger.info(f"Transformed {len(students)} student records")
            return students
            
        except Exception as e:
            logger.error(f"Error transforming students data: {e}")
            raise
    
    def transform_instagram(self, instagram_df: pd.DataFrame) -> List[InstagramPost]:
        """Transform Instagram data into Pydantic models."""
        try:
            posts = []
            
            # Clean and transform data
            instagram_df['Data'] = pd.to_datetime(instagram_df['Data'])
            
            # Convert numeric columns
            numeric_columns = ['Likes', 'Comentários', 'Salvamentos', 'Alcance', 'Visitas ao Perfil', 'Novos Seguidores']
            for col in numeric_columns:
                instagram_df[col] = pd.to_numeric(instagram_df[col], errors='coerce')
                instagram_df[col] = instagram_df[col].fillna(0).astype(int)
            
            # Convert to Pydantic models
            for _, row in instagram_df.iterrows():
                try:
                    post = InstagramPost(**row.to_dict())
                    posts.append(post)
                except Exception as e:
                    logger.warning(f"Error processing Instagram post row: {e}")
                    continue
            
            logger.info(f"Transformed {len(posts)} Instagram posts")
            return posts
            
        except Exception as e:
            logger.error(f"Error transforming Instagram data: {e}")
            raise
    
    def load_data(self, students: List[Student], posts: List[InstagramPost]) -> bool:
        """Load transformed data into database."""
        try:
            # Create tables if they don't exist
            self.db_manager.create_tables()
            
            # Load students data
            students_success = self.db_manager.insert_students(students)
            
            # Load Instagram posts data
            posts_success = self.db_manager.insert_instagram_posts(posts)
            
            return students_success and posts_success
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return False
    
    def generate_analytics(self) -> Dict[str, Any]:
        """Generate comprehensive analytics."""
        try:
            # Retrieve data from database
            students_df = self.db_manager.get_students()
            instagram_df = self.db_manager.get_instagram_posts()
            
            if students_df.empty or instagram_df.empty:
                logger.warning("No data available for analytics")
                return {}
            
            # Generate analytics
            students_analytics = self.analytics_engine.analyze_students(students_df)
            instagram_analytics = self.analytics_engine.analyze_instagram(instagram_df)
            cross_platform_analytics = self.analytics_engine.cross_platform_analysis(students_df, instagram_df)
            
            # Generate actionable insights
            insights = self.analytics_engine.generate_actionable_insights(
                students_analytics, instagram_analytics, cross_platform_analytics
            )
            
            # Prepare analytics data for storage
            analytics_data = {
                'students_analytics': students_analytics.dict(),
                'instagram_analytics': instagram_analytics.dict(),
                'cross_platform_analytics': cross_platform_analytics.dict(),
                'actionable_insights': insights
            }
            
            # Store analytics in database
            self.db_manager.insert_analytics({
                'date': datetime.now().date(),
                'metric_name': 'comprehensive_analytics',
                'metric_value': analytics_data
            })
            
            logger.info("Analytics generated and stored successfully")
            return analytics_data
            
        except Exception as e:
            logger.error(f"Error generating analytics: {e}")
            return {}
    
    def run_full_pipeline(self) -> bool:
        """Run the complete ETL pipeline."""
        try:
            logger.info("Starting Social FIT ETL pipeline")
            
            # Extract
            students_df, instagram_df = self.extract_data()
            
            # Transform
            students = self.transform_students(students_df)
            posts = self.transform_instagram(instagram_df)
            
            # Load
            load_success = self.load_data(students, posts)
            
            if load_success:
                # Generate analytics
                analytics = self.generate_analytics()
                logger.info("ETL pipeline completed successfully")
                return True
            else:
                logger.error("ETL pipeline failed at loading stage")
                return False
                
        except Exception as e:
            logger.error(f"ETL pipeline failed: {e}")
            return False
    
    def run_incremental_update(self) -> bool:
        """Run incremental update of the pipeline."""
        try:
            logger.info("Starting incremental update")
            
            # Extract new data
            students_df, instagram_df = self.extract_data()
            
            # Get existing data to identify new records
            existing_students = self.db_manager.get_students()
            existing_posts = self.db_manager.get_instagram_posts()
            
            # Filter new records (simplified logic - in production would use timestamps)
            if not existing_students.empty:
                students_df = students_df[~students_df['ID'].isin(existing_students['id'])]
            
            if not existing_posts.empty:
                instagram_df = instagram_df[~instagram_df['Data'].isin(existing_posts['post_date'])]
            
            if students_df.empty and instagram_df.empty:
                logger.info("No new data to process")
                return True
            
            # Transform and load new data
            if not students_df.empty:
                new_students = self.transform_students(students_df)
                self.db_manager.insert_students(new_students)
            
            if not instagram_df.empty:
                new_posts = self.transform_instagram(instagram_df)
                self.db_manager.insert_instagram_posts(new_posts)
            
            # Regenerate analytics
            self.generate_analytics()
            
            logger.info("Incremental update completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Incremental update failed: {e}")
            return False 