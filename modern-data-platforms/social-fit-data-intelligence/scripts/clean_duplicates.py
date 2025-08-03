#!/usr/bin/env python3
"""
Clean Duplicates Script
=======================

Script to clean duplicate records from the Social FIT database.
"""

import sys
import os
from pathlib import Path
from loguru import logger

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database.database import DatabaseManager
from src.config.config import settings

def clean_duplicate_students():
    """Clean duplicate students based on name and birth_date."""
    try:
        db = DatabaseManager()
        
        # Get all students
        result = db.supabase.table('students').select('*').execute()
        students = result.data
        
        logger.info(f"📊 Found {len(students)} total students")
        
        # Group by name and birth_date
        seen = set()
        duplicates = []
        unique_students = []
        
        for student in students:
            key = (student['name'], student['birth_date'])
            if key in seen:
                duplicates.append(student['id'])
            else:
                seen.add(key)
                unique_students.append(student)
        
        logger.info(f"🔍 Found {len(duplicates)} duplicate students")
        
        if duplicates:
            # Delete duplicates (keep the first occurrence)
            for duplicate_id in duplicates:
                db.supabase.table('students').delete().eq('id', duplicate_id).execute()
                logger.info(f"🗑️  Deleted duplicate student ID: {duplicate_id}")
            
            logger.info(f"✅ Cleaned {len(duplicates)} duplicate students")
        else:
            logger.info("✅ No duplicate students found")
        
        return len(unique_students)
        
    except Exception as e:
        logger.error(f"❌ Error cleaning duplicate students: {e}")
        return 0

def clean_duplicate_instagram_posts():
    """Clean duplicate Instagram posts based on post_date and main_hashtag."""
    try:
        db = DatabaseManager()
        
        # Get all Instagram posts
        result = db.supabase.table('instagram_posts').select('*').execute()
        posts = result.data
        
        logger.info(f"📊 Found {len(posts)} total Instagram posts")
        
        # Group by post_date and main_hashtag
        seen = set()
        duplicates = []
        unique_posts = []
        
        for post in posts:
            key = (post['post_date'], post['main_hashtag'])
            if key in seen:
                duplicates.append(post['id'])
            else:
                seen.add(key)
                unique_posts.append(post)
        
        logger.info(f"🔍 Found {len(duplicates)} duplicate Instagram posts")
        
        if duplicates:
            # Delete duplicates (keep the first occurrence)
            for duplicate_id in duplicates:
                db.supabase.table('instagram_posts').delete().eq('id', duplicate_id).execute()
                logger.info(f"🗑️  Deleted duplicate post ID: {duplicate_id}")
            
            logger.info(f"✅ Cleaned {len(duplicates)} duplicate Instagram posts")
        else:
            logger.info("✅ No duplicate Instagram posts found")
        
        return len(unique_posts)
        
    except Exception as e:
        logger.error(f"❌ Error cleaning duplicate Instagram posts: {e}")
        return 0

def clean_duplicate_analytics():
    """Clean duplicate analytics based on metric_name and date."""
    try:
        db = DatabaseManager()
        
        # Get all analytics
        result = db.supabase.table('analytics').select('*').execute()
        analytics = result.data
        
        logger.info(f"📊 Found {len(analytics)} total analytics records")
        
        # Group by metric_name and date
        seen = set()
        duplicates = []
        unique_analytics = []
        
        for analytic in analytics:
            key = (analytic['metric_name'], analytic['date'])
            if key in seen:
                duplicates.append(analytic['id'])
            else:
                seen.add(key)
                unique_analytics.append(analytic)
        
        logger.info(f"🔍 Found {len(duplicates)} duplicate analytics records")
        
        if duplicates:
            # Delete duplicates (keep the first occurrence)
            for duplicate_id in duplicates:
                db.supabase.table('analytics').delete().eq('id', duplicate_id).execute()
                logger.info(f"🗑️  Deleted duplicate analytics ID: {duplicate_id}")
            
            logger.info(f"✅ Cleaned {len(duplicates)} duplicate analytics records")
        else:
            logger.info("✅ No duplicate analytics records found")
        
        return len(unique_analytics)
        
    except Exception as e:
        logger.error(f"❌ Error cleaning duplicate analytics: {e}")
        return 0

def main():
    """Main function to clean all duplicate records."""
    logger.info("🧹 Starting Duplicate Cleanup Process")
    logger.info("=" * 50)
    
    # Clean duplicates from all tables
    students_count = clean_duplicate_students()
    logger.info("-" * 30)
    
    posts_count = clean_duplicate_instagram_posts()
    logger.info("-" * 30)
    
    analytics_count = clean_duplicate_analytics()
    logger.info("-" * 30)
    
    logger.info("🎉 Duplicate Cleanup Completed!")
    logger.info("=" * 50)
    logger.info(f"📊 Final Counts:")
    logger.info(f"   - Students: {students_count}")
    logger.info(f"   - Instagram Posts: {posts_count}")
    logger.info(f"   - Analytics Records: {analytics_count}")

if __name__ == "__main__":
    main() 