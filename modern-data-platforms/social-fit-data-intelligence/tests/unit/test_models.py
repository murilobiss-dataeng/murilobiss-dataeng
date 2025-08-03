"""
Unit Tests for Data Models
=========================

Test cases for Pydantic models and data validation.
"""

import pytest
from datetime import datetime
from src.models import Student, InstagramPost, ColumnMapper
from src.models import StudentAnalytics, InstagramAnalytics, CrossPlatformAnalytics


class TestStudentModel:
    """Test cases for Student model"""
    
    def test_valid_student_creation(self, sample_student_dict):
        """Test creating a valid Student instance"""
        student = Student(**sample_student_dict)
        
        assert student.id == 1
        assert student.name == "João Silva"
        assert student.gender == "M"
        assert student.plan_type == "Mensal"
        assert student.gympass is True
        assert student.active_plan is True
    
    def test_student_validation_errors(self):
        """Test Student model validation errors"""
        invalid_data = {
            'id': 'invalid_id',  # Should be int
            'name': '',  # Should not be empty
            'gender': 'X',  # Invalid gender
            'birth_date': 'invalid_date',
            'monthly_value': -100,  # Negative value
        }
        
        with pytest.raises(Exception):
            Student(**invalid_data)
    
    def test_student_serialization(self, sample_student_dict):
        """Test Student model serialization"""
        student = Student(**sample_student_dict)
        student_dict = student.model_dump()
        
        assert isinstance(student_dict, dict)
        assert student_dict['id'] == 1
        assert student_dict['name'] == "João Silva"


class TestInstagramPostModel:
    """Test cases for InstagramPost model"""
    
    def test_valid_instagram_post_creation(self, sample_instagram_post_dict):
        """Test creating a valid InstagramPost instance"""
        post = InstagramPost(**sample_instagram_post_dict)
        
        assert post.date == datetime(2024, 1, 1)
        assert post.likes == 150
        assert post.comments == 25
        assert post.reach == 1000
        assert post.main_hashtag == "#socialfit"
    
    def test_instagram_post_validation_errors(self):
        """Test InstagramPost model validation errors"""
        invalid_data = {
            'date': 'invalid_date',
            'likes': -10,  # Negative likes
            'comments': 'invalid',  # Should be int
            'reach': 0,  # Zero reach
        }
        
        with pytest.raises(Exception):
            InstagramPost(**invalid_data)
    
    def test_instagram_post_serialization(self, sample_instagram_post_dict):
        """Test InstagramPost model serialization"""
        post = InstagramPost(**sample_instagram_post_dict)
        post_dict = post.model_dump()
        
        assert isinstance(post_dict, dict)
        assert post_dict['likes'] == 150
        assert post_dict['main_hashtag'] == "#socialfit"


class TestColumnMapper:
    """Test cases for ColumnMapper utility"""
    
    def test_create_column_mapping_students(self, sample_students_df):
        """Test column mapping for student data"""
        mapping = ColumnMapper.create_column_mapping(sample_students_df)
        
        assert 'ID' in mapping
        assert 'Nome' in mapping
        assert 'Gênero' in mapping
        assert mapping['ID'] == 'id'
        assert mapping['Nome'] == 'name'
        assert mapping['Gênero'] == 'gender'
    
    def test_create_column_mapping_instagram(self, sample_instagram_df):
        """Test column mapping for Instagram data"""
        mapping = ColumnMapper.create_column_mapping(sample_instagram_df)
        
        assert 'Data' in mapping
        assert 'Curtidas' in mapping
        assert 'Comentários' in mapping
        assert mapping['Data'] == 'date'
        assert mapping['Curtidas'] == 'likes'
        assert mapping['Comentários'] == 'comments'
    
    def test_transform_dataframe(self, sample_students_df):
        """Test dataframe transformation"""
        mapping = ColumnMapper.create_column_mapping(sample_students_df)
        transformed_df = ColumnMapper.transform_dataframe(sample_students_df, mapping)
        
        # Check if columns were renamed
        assert 'id' in transformed_df.columns
        assert 'name' in transformed_df.columns
        assert 'gender' in transformed_df.columns
        
        # Check if data is preserved
        assert transformed_df['id'].iloc[0] == 1
        assert transformed_df['name'].iloc[0] == "João Silva"
    
    def test_handle_missing_columns(self):
        """Test handling of missing columns"""
        df_with_missing = pd.DataFrame({
            'ID': [1, 2],
            'Nome': ['João', 'Maria'],
            'Unknown_Column': ['value1', 'value2']
        })
        
        mapping = ColumnMapper.create_column_mapping(df_with_missing)
        
        # Should handle unknown columns gracefully
        assert 'ID' in mapping
        assert 'Nome' in mapping
        assert 'Unknown_Column' not in mapping


class TestAnalyticsModels:
    """Test cases for analytics models"""
    
    def test_student_analytics_creation(self):
        """Test StudentAnalytics model creation"""
        analytics = StudentAnalytics(
            total_students=100,
            active_students=85,
            total_revenue=15000.0,
            average_monthly_value=150.0,
            plan_distribution={'Mensal': 60, 'Trimestral': 30, 'Anual': 10},
            gender_distribution={'M': 55, 'F': 45},
            neighborhood_distribution={'Centro': 40, 'Vila Nova': 35, 'Jardim': 25}
        )
        
        assert analytics.total_students == 100
        assert analytics.active_students == 85
        assert analytics.total_revenue == 15000.0
        assert analytics.average_monthly_value == 150.0
    
    def test_instagram_analytics_creation(self):
        """Test InstagramAnalytics model creation"""
        analytics = InstagramAnalytics(
            total_posts=50,
            total_likes=5000,
            total_comments=500,
            total_reach=100000,
            average_engagement_rate=0.05,
            best_performing_hashtag="#socialfit",
            follower_growth_rate=0.02,
            optimal_posting_times={'Monday': '18:00', 'Wednesday': '19:00'}
        )
        
        assert analytics.total_posts == 50
        assert analytics.total_likes == 5000
        assert analytics.average_engagement_rate == 0.05
        assert analytics.best_performing_hashtag == "#socialfit"
    
    def test_cross_platform_analytics_creation(self):
        """Test CrossPlatformAnalytics model creation"""
        analytics = CrossPlatformAnalytics(
            correlation_score=0.75,
            social_media_impact_score=0.8,
            revenue_correlation=0.6,
            optimal_content_strategy={
                'best_hashtags': ['#socialfit', '#fitness'],
                'best_posting_days': ['Monday', 'Wednesday'],
                'best_posting_times': ['18:00', '19:00']
            },
            actionable_insights=[
                "Increase posting frequency on Mondays",
                "Focus on fitness-related content",
                "Engage more with followers during peak hours"
            ]
        )
        
        assert analytics.correlation_score == 0.75
        assert analytics.social_media_impact_score == 0.8
        assert len(analytics.actionable_insights) == 3 