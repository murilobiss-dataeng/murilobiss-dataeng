"""
Integration Tests for Database Operations
=======================================

Integration tests for database connectivity and operations.
"""

import pytest
from unittest.mock import patch, Mock, MagicMock
from src.database import DatabaseManager
from src.models import Student, InstagramPost


class TestDatabaseIntegration:
    """Integration tests for database operations"""
    
    @pytest.mark.integration
    def test_database_connection(self):
        """Test database connection with mocked Supabase"""
        with patch('src.database.create_client') as mock_create_client:
            # Mock successful connection
            mock_client = Mock()
            mock_client.table().select().execute.return_value = Mock(data=[])
            mock_create_client.return_value = mock_client
            
            db = DatabaseManager()
            success = db.test_connection()
            
            assert success is True
            mock_create_client.assert_called_once()
    
    @pytest.mark.integration
    def test_database_connection_failure(self):
        """Test database connection failure"""
        with patch('src.database.create_client') as mock_create_client:
            # Mock connection failure
            mock_create_client.side_effect = Exception("Connection failed")
            
            db = DatabaseManager()
            success = db.test_connection()
            
            assert success is False
    
    @pytest.mark.integration
    def test_insert_students_success(self, sample_student_dict):
        """Test successful student data insertion"""
        with patch('src.database.create_client') as mock_create_client:
            # Mock successful insertion
            mock_client = Mock()
            mock_client.table().insert().execute.return_value = Mock(data=[sample_student_dict])
            mock_create_client.return_value = mock_client
            
            db = DatabaseManager()
            students = [Student(**sample_student_dict)]
            success = db.insert_students(students)
            
            assert success is True
            mock_client.table().insert().execute.assert_called_once()
    
    @pytest.mark.integration
    def test_insert_instagram_posts_success(self, sample_instagram_post_dict):
        """Test successful Instagram post insertion"""
        with patch('src.database.create_client') as mock_create_client:
            # Mock successful insertion
            mock_client = Mock()
            mock_client.table().insert().execute.return_value = Mock(data=[sample_instagram_post_dict])
            mock_create_client.return_value = mock_client
            
            db = DatabaseManager()
            posts = [InstagramPost(**sample_instagram_post_dict)]
            success = db.insert_instagram_posts(posts)
            
            assert success is True
            mock_client.table().insert().execute.assert_called_once()
    
    @pytest.mark.integration
    def test_insert_analytics_success(self):
        """Test successful analytics insertion"""
        with patch('src.database.create_client') as mock_create_client:
            # Mock successful insertion
            mock_client = Mock()
            mock_client.table().insert().execute.return_value = Mock(data=[{'id': 1}])
            mock_create_client.return_value = mock_client
            
            db = DatabaseManager()
            analytics_data = {
                'date': '2024-01-01',
                'metric_name': 'student_count',
                'metric_value': {'total_students': 100}
            }
            success = db.insert_analytics([analytics_data])
            
            assert success is True
            mock_client.table().insert().execute.assert_called_once()
    
    @pytest.mark.integration
    def test_get_students_success(self, sample_student_dict):
        """Test successful student data retrieval"""
        with patch('src.database.create_client') as mock_create_client:
            # Mock successful retrieval
            mock_client = Mock()
            mock_client.table().select().execute.return_value = Mock(data=[sample_student_dict])
            mock_create_client.return_value = mock_client
            
            db = DatabaseManager()
            students_df = db.get_students()
            
            assert students_df is not None
            assert len(students_df) == 1
            mock_client.table().select().execute.assert_called_once()
    
    @pytest.mark.integration
    def test_get_instagram_posts_success(self, sample_instagram_post_dict):
        """Test successful Instagram posts retrieval"""
        with patch('src.database.create_client') as mock_create_client:
            # Mock successful retrieval
            mock_client = Mock()
            mock_client.table().select().execute.return_value = Mock(data=[sample_instagram_post_dict])
            mock_create_client.return_value = mock_client
            
            db = DatabaseManager()
            posts_df = db.get_instagram_posts()
            
            assert posts_df is not None
            assert len(posts_df) == 1
            mock_client.table().select().execute.assert_called_once()
    
    @pytest.mark.integration
    def test_get_analytics_success(self):
        """Test successful analytics retrieval"""
        with patch('src.database.create_client') as mock_create_client:
            # Mock successful retrieval
            mock_client = Mock()
            mock_client.table().select().execute.return_value = Mock(data=[
                {'id': 1, 'metric_name': 'student_count', 'metric_value': {'total': 100}}
            ])
            mock_create_client.return_value = mock_client
            
            db = DatabaseManager()
            analytics_df = db.get_analytics()
            
            assert analytics_df is not None
            assert len(analytics_df) == 1
            mock_client.table().select().execute.assert_called_once()
    
    @pytest.mark.integration
    def test_batch_insertion(self, sample_student_dict):
        """Test batch insertion of data"""
        with patch('src.database.create_client') as mock_create_client:
            # Mock successful batch insertion
            mock_client = Mock()
            mock_client.table().insert().execute.return_value = Mock(data=[sample_student_dict])
            mock_create_client.return_value = mock_client
            
            db = DatabaseManager()
            
            # Create multiple students
            students = [Student(**sample_student_dict) for _ in range(10)]
            success = db.insert_students(students)
            
            assert success is True
            # Should handle batch insertion
            mock_client.table().insert().execute.assert_called_once()
    
    @pytest.mark.integration
    def test_data_validation_before_insertion(self, sample_student_dict):
        """Test data validation before database insertion"""
        with patch('src.database.create_client') as mock_create_client:
            mock_client = Mock()
            mock_create_client.return_value = mock_client
            
            db = DatabaseManager()
            
            # Test with valid data
            valid_student = Student(**sample_student_dict)
            success = db.insert_students([valid_student])
            
            # Should validate data before insertion
            assert success is True
            
            # Test with invalid data
            invalid_data = sample_student_dict.copy()
            invalid_data['id'] = 'invalid_id'  # Invalid ID type
            
            with pytest.raises(Exception):
                invalid_student = Student(**invalid_data)
    
    @pytest.mark.integration
    def test_error_handling_during_insertion(self, sample_student_dict):
        """Test error handling during data insertion"""
        with patch('src.database.create_client') as mock_create_client:
            # Mock insertion failure
            mock_client = Mock()
            mock_client.table().insert().execute.side_effect = Exception("Insertion failed")
            mock_create_client.return_value = mock_client
            
            db = DatabaseManager()
            students = [Student(**sample_student_dict)]
            success = db.insert_students(students)
            
            assert success is False
    
    @pytest.mark.integration
    def test_connection_pooling(self):
        """Test database connection pooling"""
        with patch('src.database.create_client') as mock_create_client:
            mock_client = Mock()
            mock_create_client.return_value = mock_client
            
            db = DatabaseManager()
            
            # Test multiple operations with same connection
            success1 = db.test_connection()
            success2 = db.test_connection()
            
            # Should reuse connection
            assert success1 is True
            assert success2 is True
            # Should create client only once
            assert mock_create_client.call_count == 1
    
    @pytest.mark.integration
    def test_data_serialization(self, sample_student_dict):
        """Test data serialization for database storage"""
        with patch('src.database.create_client') as mock_create_client:
            mock_client = Mock()
            mock_client.table().insert().execute.return_value = Mock(data=[sample_student_dict])
            mock_create_client.return_value = mock_client
            
            db = DatabaseManager()
            student = Student(**sample_student_dict)
            
            # Test that data is properly serialized
            success = db.insert_students([student])
            
            assert success is True
            
            # Verify that the data was serialized correctly
            call_args = mock_client.table().insert().execute.call_args
            inserted_data = call_args[0][0]  # Get the data that was inserted
            
            # Check that datetime objects are properly handled
            assert 'birth_date' in inserted_data[0]
            assert 'plan_start_date' in inserted_data[0]
    
    @pytest.mark.integration
    def test_transaction_handling(self, sample_student_dict, sample_instagram_post_dict):
        """Test transaction handling for multiple operations"""
        with patch('src.database.create_client') as mock_create_client:
            mock_client = Mock()
            mock_create_client.return_value = mock_client
            
            db = DatabaseManager()
            
            # Test multiple insertions
            student = Student(**sample_student_dict)
            post = InstagramPost(**sample_instagram_post_dict)
            
            success1 = db.insert_students([student])
            success2 = db.insert_instagram_posts([post])
            
            # Both operations should succeed
            assert success1 is True
            assert success2 is True
    
    @pytest.mark.integration
    def test_data_consistency(self, sample_student_dict):
        """Test data consistency between insert and retrieve operations"""
        with patch('src.database.create_client') as mock_create_client:
            mock_client = Mock()
            
            # Mock insertion
            mock_client.table().insert().execute.return_value = Mock(data=[sample_student_dict])
            # Mock retrieval
            mock_client.table().select().execute.return_value = Mock(data=[sample_student_dict])
            
            mock_create_client.return_value = mock_client
            
            db = DatabaseManager()
            student = Student(**sample_student_dict)
            
            # Insert data
            insert_success = db.insert_students([student])
            assert insert_success is True
            
            # Retrieve data
            retrieved_df = db.get_students()
            assert retrieved_df is not None
            assert len(retrieved_df) == 1
            
            # Verify data consistency
            retrieved_data = retrieved_df.iloc[0].to_dict()
            assert retrieved_data['id'] == sample_student_dict['id']
            assert retrieved_data['name'] == sample_student_dict['name'] 