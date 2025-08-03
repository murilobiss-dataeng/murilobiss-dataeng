#!/usr/bin/env python3
"""
Social FIT Data Intelligence Platform - Main Application
=======================================================

Main application entry point for the Social FIT ETL pipeline and analytics platform.
"""

import sys
import os
import schedule
import time
from datetime import datetime
from pathlib import Path
from loguru import logger

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent))

from src.etl import SocialFITETL
from src.config import settings

def setup_logging():
    """Setup logging configuration."""
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # Configure logger
    logger.remove()  # Remove default handler
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=settings.LOG_LEVEL
    )
    logger.add(
        "logs/social_fit_etl.log",
        rotation="1 day",
        retention="30 days",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=settings.LOG_LEVEL
    )

def run_etl_pipeline():
    """Run the ETL pipeline."""
    try:
        logger.info("=" * 60)
        logger.info("SOCIAL FIT ETL PIPELINE STARTED")
        logger.info("=" * 60)
        
        # Initialize ETL pipeline
        etl = SocialFITETL()
        
        # Run full pipeline
        success = etl.run_full_pipeline()
        
        if success:
            logger.info("✅ ETL Pipeline completed successfully!")
            logger.info("📊 Analytics generated and stored in Supabase")
            logger.info("🎯 Actionable insights ready for Social FIT team")
        else:
            logger.error("❌ ETL Pipeline failed!")
            return False
        
        logger.info("=" * 60)
        return True
        
    except Exception as e:
        logger.error(f"❌ Critical error in ETL pipeline: {e}")
        return False

def run_incremental_update():
    """Run incremental update."""
    try:
        logger.info("🔄 Running incremental update...")
        
        etl = SocialFITETL()
        success = etl.run_incremental_update()
        
        if success:
            logger.info("✅ Incremental update completed successfully!")
        else:
            logger.error("❌ Incremental update failed!")
        
        return success
        
    except Exception as e:
        logger.error(f"❌ Error in incremental update: {e}")
        return False

def schedule_daily_update():
    """Schedule daily incremental updates."""
    schedule.every().day.at("06:00").do(run_incremental_update)
    schedule.every().day.at("18:00").do(run_incremental_update)
    
    logger.info("📅 Scheduled daily updates at 06:00 and 18:00")
    
    while True:
        schedule.run_pending()
        time.sleep(60)

def main():
    """Main execution function."""
    # Setup logging
    setup_logging()
    
    # Check command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "run":
            # Run full pipeline once
            run_etl_pipeline()
            
        elif command == "incremental":
            # Run incremental update
            run_incremental_update()
            
        elif command == "schedule":
            # Run with scheduling
            logger.info("🚀 Starting scheduled ETL pipeline...")
            run_etl_pipeline()  # Run initial pipeline
            schedule_daily_update()
            
        elif command == "test":
            # Test mode - run with limited data
            logger.info("🧪 Running in test mode...")
            # Add test-specific logic here
            run_etl_pipeline()
            
        else:
            print("Usage: python app.py [run|incremental|schedule|test]")
            print("  run        - Run full ETL pipeline once")
            print("  incremental - Run incremental update")
            print("  schedule   - Run with daily scheduling")
            print("  test       - Run in test mode")
            sys.exit(1)
    else:
        # Default: run full pipeline
        run_etl_pipeline()

if __name__ == "__main__":
    main() 