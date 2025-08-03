"""
Integration Tests for ETL Pipeline
================================

End-to-end integration tests for the complete ETL pipeline.
"""

import pytest
import pandas as pd
from unittest.mock import patch, Mock
from src.etl import SocialFITETL
from src.database import DatabaseManager
from src.analytics import AnalyticsEngine


class TestPipelineIntegration:
    """Integration tests for complete ETL pipeline"""
    
    @pytest.mark.integration
    def test_complete_pipeline_flow(self, sample_students_df, sample_instagram_df):
        """Test complete pipeline flow with mocked components"""
        # Mock all external dependencies
        with patch('src.etl.pd.read_csv') as mock_read_csv, \
             patch('src.database.DatabaseManager') as mock_db_class, \
             patch('src.analytics.AnalyticsEngine') as mock_analytics_class:
            
            # Setup mocks
            mock_read_csv.side_effect = [sample_students_df, sample_instagram_df]
            
            mock_db = Mock()
            mock_db.test_connection.return_value = True
            mock_db.insert_students.return_value = True
            mock_db.insert_instagram_posts.return_value = True
            mock_db.insert_analytics.return_value = True
            mock_db_class.return_value = mock_db
            
            mock_analytics = Mock()
            mock_analytics.analyze_students.return_value = Mock()
            mock_analytics.analyze_instagram.return_value = Mock()
            mock_analytics.cross_platform_analysis.return_value = Mock()
            mock_analytics.generate_actionable_insights.return_value = Mock()
            mock_analytics_class.return_value = mock_analytics
            
            # Run pipeline
            etl = SocialFITETL()
            success = etl.run_full_pipeline()
            
            # Verify success
            assert success is True
            
            # Verify all components were called
            mock_db.test_connection.assert_called_once()
            mock_db.insert_students.assert_called_once()
            mock_db.insert_instagram_posts.assert_called_once()
            mock_analytics.analyze_students.assert_called_once()
            mock_analytics.analyze_instagram.assert_called_once()
    
    @pytest.mark.integration
    def test_pipeline_with_database_failure(self, sample_students_df, sample_instagram_df):
        """Test pipeline behavior when database operations fail"""
        with patch('src.etl.pd.read_csv') as mock_read_csv, \
             patch('src.database.DatabaseManager') as mock_db_class:
            
            # Setup mocks
            mock_read_csv.side_effect = [sample_students_df, sample_instagram_df]
            
            mock_db = Mock()
            mock_db.test_connection.return_value = False  # Database connection fails
            mock_db_class.return_value = mock_db
            
            # Run pipeline
            etl = SocialFITETL()
            success = etl.run_full_pipeline()
            
            # Verify failure
            assert success is False
    
    @pytest.mark.integration
    def test_pipeline_with_data_validation_failure(self):
        """Test pipeline behavior with invalid data"""
        # Create invalid data
        invalid_students_df = pd.DataFrame({
            'ID': [1, 2],
            'Nome': ['', ''],  # Empty names
            'Gênero': ['X', 'Y'],  # Invalid gender
            'Valor_Mensal_USD': [-100, -200]  # Negative values
        })
        
        with patch('src.etl.pd.read_csv') as mock_read_csv:
            mock_read_csv.return_value = invalid_students_df
            
            # Run pipeline
            etl = SocialFITETL()
            success = etl.run_full_pipeline()
            
            # Should handle invalid data gracefully
            assert success is False
    
    @pytest.mark.integration
    def test_incremental_update_flow(self, sample_students_df, sample_instagram_df):
        """Test incremental update pipeline flow"""
        with patch('src.etl.pd.read_csv') as mock_read_csv, \
             patch('src.database.DatabaseManager') as mock_db_class:
            
            # Setup mocks
            mock_read_csv.side_effect = [sample_students_df, sample_instagram_df]
            
            mock_db = Mock()
            mock_db.test_connection.return_value = True
            mock_db.insert_students.return_value = True
            mock_db.insert_instagram_posts.return_value = True
            mock_db_class.return_value = mock_db
            
            # Run incremental update
            etl = SocialFITETL()
            success = etl.run_incremental_update()
            
            # Verify success
            assert success is True
    
    @pytest.mark.integration
    def test_data_transformation_integration(self, sample_students_df, sample_instagram_df):
        """Test data transformation integration with real data"""
        etl = SocialFITETL()
        
        # Test student transformation
        students = etl.transform_students(sample_students_df)
        assert len(students) == 3
        assert all(hasattr(student, 'id') for student in students)
        assert all(hasattr(student, 'name') for student in students)
        assert all(hasattr(student, 'gender') for student in students)
        
        # Test Instagram transformation
        posts = etl.transform_instagram(sample_instagram_df)
        assert len(posts) == 3
        assert all(hasattr(post, 'date') for post in posts)
        assert all(hasattr(post, 'likes') for post in posts)
        assert all(hasattr(post, 'comments') for post in posts)
    
    @pytest.mark.integration
    def test_analytics_integration(self, sample_students_df, sample_instagram_df):
        """Test analytics integration with real data"""
        analytics = AnalyticsEngine()
        
        # Test student analytics
        student_analytics = analytics.analyze_students(sample_students_df)
        assert student_analytics is not None
        assert hasattr(student_analytics, 'total_students')
        assert hasattr(student_analytics, 'active_students')
        
        # Test Instagram analytics
        instagram_analytics = analytics.analyze_instagram(sample_instagram_df)
        assert instagram_analytics is not None
        assert hasattr(instagram_analytics, 'total_posts')
        assert hasattr(instagram_analytics, 'average_engagement_rate')
        
        # Test cross-platform analytics
        cross_analytics = analytics.cross_platform_analysis(sample_students_df, sample_instagram_df)
        assert cross_analytics is not None
        assert hasattr(cross_analytics, 'correlation_score')
    
    @pytest.mark.integration
    def test_error_handling_integration(self):
        """Test error handling integration"""
        etl = SocialFITETL()
        
        # Test with missing files
        with pytest.raises(FileNotFoundError):
            etl.extract_data()
        
        # Test with invalid data types
        invalid_df = pd.DataFrame({
            'ID': ['invalid', 'invalid'],
            'Nome': [123, 456],  # Numbers instead of strings
            'Gênero': ['M', 'F']
        })
        
        # Should handle gracefully
        try:
            students = etl.transform_students(invalid_df)
            # If it doesn't raise an exception, it should handle the data
            assert isinstance(students, list)
        except Exception:
            # It's also acceptable to raise an exception for invalid data
            pass
    
    @pytest.mark.integration
    def test_performance_integration(self, sample_students_df, sample_instagram_df):
        """Test pipeline performance with larger datasets"""
        # Create larger dataset
        large_students_df = pd.concat([sample_students_df] * 100, ignore_index=True)
        large_instagram_df = pd.concat([sample_instagram_df] * 50, ignore_index=True)
        
        etl = SocialFITETL()
        
        # Test transformation performance
        import time
        start_time = time.time()
        
        students = etl.transform_students(large_students_df)
        posts = etl.transform_instagram(large_instagram_df)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Should process within reasonable time (adjust threshold as needed)
        assert processing_time < 10.0  # 10 seconds threshold
        assert len(students) == 300
        assert len(posts) == 150
    
    @pytest.mark.integration
    def test_memory_usage_integration(self, sample_students_df, sample_instagram_df):
        """Test memory usage during pipeline execution"""
        import psutil
        import os
        
        # Get initial memory usage
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        etl = SocialFITETL()
        
        # Run transformations
        students = etl.transform_students(sample_students_df)
        posts = etl.transform_instagram(sample_instagram_df)
        
        # Get final memory usage
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (adjust threshold as needed)
        assert memory_increase < 100  # 100 MB threshold
        assert len(students) == 3
        assert len(posts) == 3 