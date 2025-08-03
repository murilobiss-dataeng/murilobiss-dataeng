#!/usr/bin/env python3
"""
Test Analytics Insertion
========================

Script to test analytics generation and insertion into the database.
"""

import sys
import os
from pathlib import Path
import json
from datetime import datetime

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database import DatabaseManager
from src.analytics import AnalyticsEngine
from src.config import settings
from loguru import logger

def test_analytics_insertion():
    """Test analytics generation and insertion."""
    try:
        logger.info("🧪 Testing analytics insertion...")
        
        # Initialize components
        db = DatabaseManager()
        analytics_engine = AnalyticsEngine()
        
        # Test connection
        if not db.test_connection():
            logger.error("❌ Database connection failed")
            return False
        
        # Get data from database
        students_df = db.get_students()
        instagram_df = db.get_instagram_posts()
        
        logger.info(f"📊 Retrieved {len(students_df)} students and {len(instagram_df)} Instagram posts")
        
        if students_df.empty or instagram_df.empty:
            logger.error("❌ No data available for analytics")
            return False
        
        # Generate analytics
        logger.info("🔍 Generating student analytics...")
        students_analytics = analytics_engine.analyze_students(students_df)
        
        logger.info("📱 Generating Instagram analytics...")
        instagram_analytics = analytics_engine.analyze_instagram(instagram_df)
        
        logger.info("🔗 Generating cross-platform analytics...")
        cross_platform_analytics = analytics_engine.cross_platform_analysis(students_df, instagram_df)
        
        logger.info("💡 Generating actionable insights...")
        insights = analytics_engine.generate_actionable_insights(
            students_analytics, instagram_analytics, cross_platform_analytics
        )
        
        # Test JSON serialization
        logger.info("🔄 Testing JSON serialization...")
        
        # Test individual analytics objects
        try:
            students_json = students_analytics.model_dump()
            logger.info("✅ Student analytics serialized successfully")
        except Exception as e:
            logger.error(f"❌ Error serializing student analytics: {e}")
            return False
        
        try:
            instagram_json = instagram_analytics.model_dump()
            logger.info("✅ Instagram analytics serialized successfully")
        except Exception as e:
            logger.error(f"❌ Error serializing Instagram analytics: {e}")
            return False
        
        try:
            cross_platform_json = cross_platform_analytics.model_dump()
            logger.info("✅ Cross-platform analytics serialized successfully")
        except Exception as e:
            logger.error(f"❌ Error serializing cross-platform analytics: {e}")
            return False
        
        # Prepare analytics data for storage
        analytics_data = {
            'date': datetime.now().date().isoformat(),
            'metric_name': 'comprehensive_analytics',
            'metric_value': {
                'students_analytics': students_json,
                'instagram_analytics': instagram_json,
                'cross_platform_analytics': cross_platform_json,
                'actionable_insights': insights
            }
        }
        
        # Test JSON serialization of complete data
        try:
            json_str = json.dumps(analytics_data['metric_value'])
            logger.info(f"✅ Complete analytics JSON serialized successfully ({len(json_str)} characters)")
        except Exception as e:
            logger.error(f"❌ Error serializing complete analytics: {e}")
            return False
        
        # Insert analytics into database
        logger.info("💾 Inserting analytics into database...")
        success = db.insert_analytics(analytics_data)
        
        if success:
            logger.info("✅ Analytics inserted successfully!")
            
            # Verify insertion
            logger.info("🔍 Verifying analytics insertion...")
            analytics_df = db.get_analytics('comprehensive_analytics')
            
            if not analytics_df.empty:
                logger.info(f"✅ Found {len(analytics_df)} analytics records in database")
                logger.info("📋 Analytics data:")
                for _, row in analytics_df.iterrows():
                    logger.info(f"  - ID: {row['id']}")
                    logger.info(f"  - Date: {row['date']}")
                    logger.info(f"  - Metric: {row['metric_name']}")
                    logger.info(f"  - Value size: {len(str(row['metric_value']))} characters")
            else:
                logger.warning("⚠️  No analytics records found in database")
        else:
            logger.error("❌ Failed to insert analytics")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Test failed with error: {e}")
        return False

def test_simple_analytics():
    """Test simple analytics insertion."""
    try:
        logger.info("🧪 Testing simple analytics insertion...")
        
        db = DatabaseManager()
        
        # Test simple analytics data
        simple_data = {
            'date': datetime.now().date().isoformat(),
            'metric_name': 'test_metric',
            'metric_value': {
                'total_students': 100,
                'active_students': 85,
                'total_revenue': 15000.0,
                'test_string': 'Hello World',
                'test_list': [1, 2, 3, 4, 5],
                'test_dict': {'key1': 'value1', 'key2': 'value2'}
            }
        }
        
        success = db.insert_analytics(simple_data)
        
        if success:
            logger.info("✅ Simple analytics inserted successfully!")
            
            # Verify
            analytics_df = db.get_analytics('test_metric')
            if not analytics_df.empty:
                logger.info(f"✅ Found {len(analytics_df)} test analytics records")
            else:
                logger.warning("⚠️  No test analytics records found")
        else:
            logger.error("❌ Failed to insert simple analytics")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Simple test failed: {e}")
        return False

def main():
    """Main test function."""
    logger.info("🚀 Starting Analytics Insertion Tests")
    logger.info("=" * 50)
    
    # Test simple analytics first
    simple_success = test_simple_analytics()
    
    if simple_success:
        logger.info("✅ Simple analytics test passed")
    else:
        logger.error("❌ Simple analytics test failed")
        return False
    
    logger.info("-" * 50)
    
    # Test comprehensive analytics
    comprehensive_success = test_analytics_insertion()
    
    if comprehensive_success:
        logger.info("✅ Comprehensive analytics test passed")
    else:
        logger.error("❌ Comprehensive analytics test failed")
        return False
    
    logger.info("=" * 50)
    logger.info("🎉 All analytics tests completed successfully!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 