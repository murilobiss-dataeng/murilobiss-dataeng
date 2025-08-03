#!/usr/bin/env python3
"""
Test script for Social FIT ETL Pipeline

This script tests the ETL pipeline components to ensure they work correctly
before running the full pipeline.
"""

import sys
import os
import pandas as pd
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import settings
from models import Student, InstagramPost, Gender, PlanType
from analytics import AnalyticsEngine

def test_data_loading():
    """Test data loading from CSV files."""
    print("🧪 Testing data loading...")
    
    try:
        # Test students data loading
        students_file = os.path.join(settings.DATA_DIR, settings.STUDENTS_FILE)
        students_df = pd.read_csv(students_file)
        print(f"✅ Students data loaded: {len(students_df)} records")
        
        # Test Instagram data loading
        instagram_file = os.path.join(settings.DATA_DIR, settings.INSTAGRAM_FILE)
        instagram_df = pd.read_csv(instagram_file)
        print(f"✅ Instagram data loaded: {len(instagram_df)} records")
        
        return students_df, instagram_df
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None, None

def test_data_transformation(students_df, instagram_df):
    """Test data transformation to Pydantic models."""
    print("\n🧪 Testing data transformation...")
    
    try:
        # Test student transformation
        students_df['Data de Nascimento'] = pd.to_datetime(students_df['Data de Nascimento'])
        students_df['Data Início Plano'] = pd.to_datetime(students_df['Data Início Plano'])
        students_df['Gympass'] = students_df['Gympass'].map({'True': True, 'False': False})
        students_df['Plano Ativo'] = students_df['Plano Ativo'].map({'True': True, 'False': False})
        
        students = []
        for _, row in students_df.head(5).iterrows():  # Test with first 5 records
            try:
                student = Student(**row.to_dict())
                students.append(student)
            except Exception as e:
                print(f"⚠️  Error processing student: {e}")
        
        print(f"✅ Student transformation: {len(students)} models created")
        
        # Test Instagram transformation
        instagram_df['Data'] = pd.to_datetime(instagram_df['Data'])
        numeric_columns = ['Likes', 'Comentários', 'Salvamentos', 'Alcance', 'Visitas ao Perfil', 'Novos Seguidores']
        for col in numeric_columns:
            instagram_df[col] = pd.to_numeric(instagram_df[col], errors='coerce').fillna(0).astype(int)
        
        posts = []
        for _, row in instagram_df.head(5).iterrows():  # Test with first 5 records
            try:
                post = InstagramPost(**row.to_dict())
                posts.append(post)
            except Exception as e:
                print(f"⚠️  Error processing Instagram post: {e}")
        
        print(f"✅ Instagram transformation: {len(posts)} models created")
        
        return students, posts
        
    except Exception as e:
        print(f"❌ Error in data transformation: {e}")
        return [], []

def test_analytics(students_df, instagram_df):
    """Test analytics engine."""
    print("\n🧪 Testing analytics engine...")
    
    try:
        engine = AnalyticsEngine()
        
        # Test student analytics
        students_analytics = engine.analyze_students(students_df)
        print(f"✅ Student analytics generated:")
        print(f"   - Total students: {students_analytics.total_students}")
        print(f"   - Active students: {students_analytics.active_students}")
        print(f"   - Average monthly value: R$ {students_analytics.average_monthly_value}")
        
        # Test Instagram analytics
        instagram_analytics = engine.analyze_instagram(instagram_df)
        print(f"✅ Instagram analytics generated:")
        print(f"   - Total posts: {instagram_analytics.total_posts}")
        print(f"   - Total likes: {instagram_analytics.total_likes:,}")
        print(f"   - Average engagement rate: {instagram_analytics.average_engagement_rate:.2%}")
        
        # Test cross-platform analytics
        cross_platform_analytics = engine.cross_platform_analysis(students_df, instagram_df)
        print(f"✅ Cross-platform analytics generated:")
        print(f"   - Correlation score: {cross_platform_analytics.correlation_score:.2%}")
        print(f"   - Revenue impact: R$ {cross_platform_analytics.revenue_impact:,.2f}")
        
        # Test insights generation
        insights = engine.generate_actionable_insights(
            students_analytics, instagram_analytics, cross_platform_analytics
        )
        print(f"✅ Generated {len(insights)} actionable insights")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in analytics: {e}")
        return False

def test_configuration():
    """Test configuration loading."""
    print("\n🧪 Testing configuration...")
    
    try:
        print(f"✅ Data directory: {settings.DATA_DIR}")
        print(f"✅ Students file: {settings.STUDENTS_FILE}")
        print(f"✅ Instagram file: {settings.INSTAGRAM_FILE}")
        print(f"✅ Gym name: {settings.GYM_NAME}")
        print(f"✅ Gym CNPJ: {settings.GYM_CNPJ}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in configuration: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("🧪 SOCIAL FIT ETL PIPELINE TEST SUITE")
    print("=" * 60)
    
    # Test configuration
    config_ok = test_configuration()
    
    # Test data loading
    students_df, instagram_df = test_data_loading()
    
    if students_df is not None and instagram_df is not None:
        # Test data transformation
        students, posts = test_data_transformation(students_df, instagram_df)
        
        # Test analytics
        analytics_ok = test_analytics(students_df, instagram_df)
        
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 60)
        
        if config_ok and len(students) > 0 and len(posts) > 0 and analytics_ok:
            print("✅ ALL TESTS PASSED!")
            print("🚀 ETL pipeline is ready to run")
        else:
            print("❌ SOME TESTS FAILED")
            print("🔧 Please check the errors above and fix them")
    else:
        print("❌ CRITICAL ERROR: Could not load data files")
        print("🔧 Please ensure data files exist in the data/ directory")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main() 