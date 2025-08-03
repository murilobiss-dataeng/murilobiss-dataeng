from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum
import pandas as pd
import re
import numpy as np

class Gender(str, Enum):
    MALE = "M"
    FEMALE = "F"

class PlanType(str, Enum):
    MONTHLY = "Mensal"
    QUARTERLY = "Trimestral"
    ANNUAL = "Anual"

class ColumnMapper:
    """Automatic column mapping utility for CSV files."""
    
    @staticmethod
    def detect_column_type(column_name: str, sample_values: list) -> str:
        """Detect the type of a column based on name and sample values."""
        column_lower = column_name.lower()
        
        # Student-related patterns
        if any(word in column_lower for word in ['id', 'codigo', 'numero']):
            return 'id'
        elif any(word in column_lower for word in ['nome', 'name', 'aluno', 'student']):
            return 'name'
        elif any(word in column_lower for word in ['genero', 'sexo', 'gender']):
            return 'gender'
        elif any(word in column_lower for word in ['nascimento', 'birth', 'data_nasc']):
            return 'birth_date'
        elif any(word in column_lower for word in ['endereco', 'address', 'rua']):
            return 'address'
        elif any(word in column_lower for word in ['bairro', 'neighborhood', 'bairro']):
            return 'neighborhood'
        elif any(word in column_lower for word in ['plano', 'plan', 'tipo']):
            return 'plan_type'
        elif any(word in column_lower for word in ['gympass']):
            return 'gympass'
        elif any(word in column_lower for word in ['valor', 'price', 'mensal']):
            return 'monthly_value'
        elif any(word in column_lower for word in ['total', 'valor_total']):
            return 'total_value'
        elif any(word in column_lower for word in ['inicio', 'start', 'data_inicio']):
            return 'plan_start_date'
        elif any(word in column_lower for word in ['ativo', 'active', 'status']):
            return 'active_plan'
        
        # Instagram-related patterns
        elif any(word in column_lower for word in ['data', 'date', 'post_date']):
            return 'date'
        elif any(word in column_lower for word in ['like', 'curtida']):
            return 'likes'
        elif any(word in column_lower for word in ['comentario', 'comment']):
            return 'comments'
        elif any(word in column_lower for word in ['salvamento', 'save', 'bookmark']):
            return 'saves'
        elif any(word in column_lower for word in ['alcance', 'reach', 'impression']):
            return 'reach'
        elif any(word in column_lower for word in ['visita', 'visit', 'perfil']):
            return 'profile_visits'
        elif any(word in column_lower for word in ['seguidor', 'follower', 'novo']):
            return 'new_followers'
        elif any(word in column_lower for word in ['hashtag', 'tag']):
            return 'main_hashtag'
        
        return 'unknown'
    
    @staticmethod
    def create_column_mapping(df: pd.DataFrame) -> Dict[str, str]:
        """Create automatic column mapping for a DataFrame."""
        mapping = {}
        
        for column in df.columns:
            # Get sample values (first 10 non-null values)
            sample_values = df[column].dropna().head(10).tolist()
            detected_type = ColumnMapper.detect_column_type(column, sample_values)
            
            if detected_type != 'unknown':
                mapping[column] = detected_type
        
        return mapping
    
    @staticmethod
    def transform_dataframe(df: pd.DataFrame, mapping: Dict[str, str]) -> pd.DataFrame:
        """Transform DataFrame using the column mapping."""
        transformed_df = df.copy()
        
        for column, field_type in mapping.items():
            if column not in transformed_df.columns:
                continue
                
            try:
                if field_type == 'id':
                    transformed_df[column] = pd.to_numeric(transformed_df[column], errors='coerce')
                elif field_type in ['birth_date', 'date', 'plan_start_date']:
                    transformed_df[column] = pd.to_datetime(transformed_df[column], errors='coerce')
                elif field_type in ['likes', 'comments', 'saves', 'reach', 'profile_visits', 'new_followers']:
                    # Convert to numeric and handle NaN values
                    numeric_data = pd.to_numeric(transformed_df[column], errors='coerce')
                    numeric_data = numeric_data.replace([np.nan, None], 0)
                    transformed_df[column] = numeric_data.astype(int)
                elif field_type in ['monthly_value', 'total_value']:
                    transformed_df[column] = pd.to_numeric(transformed_df[column], errors='coerce')
                elif field_type in ['gympass', 'active_plan']:
                    transformed_df[column] = transformed_df[column].apply(
                        lambda x: str(x).strip().lower() in ['true', 'sim', 'yes', '1', 'ativo']
                    )
                elif field_type == 'gender':
                    transformed_df[column] = transformed_df[column].apply(
                        lambda x: 'M' if str(x).strip().upper() in ['M', 'MASCULINO', 'MALE'] else 'F'
                    )
            except Exception as e:
                print(f"Warning: Could not transform column {column}: {e}")
        
        return transformed_df

class Student(BaseModel):
    """Student data model for Social FIT."""
    id: int = Field(alias="ID")
    name: str = Field(alias="Nome")
    gender: Gender = Field(alias="Gênero")
    birth_date: datetime = Field(alias="Data de Nascimento")
    address: str = Field(alias="Endereço")
    neighborhood: str = Field(alias="Bairro")
    plan_type: PlanType = Field(alias="Tipo_Plano")
    gympass: bool = Field(alias="Gympass")
    monthly_value: float = Field(alias="Valor_Plano_Mensal (R$)")
    total_value: float = Field(alias="Valor_Plano_Total (R$)")
    plan_start_date: datetime = Field(alias="Data Início Plano")
    active_plan: bool = Field(alias="Plano Ativo")
    
    class Config:
        allow_population_by_field_name = True

class InstagramPost(BaseModel):
    """Instagram post data model for Social FIT."""
    date: datetime = Field(alias="Data")
    likes: int = Field(alias="Likes")
    comments: int = Field(alias="Comentários")
    saves: int = Field(alias="Salvamentos")
    reach: int = Field(alias="Alcance")
    profile_visits: int = Field(alias="Visitas ao Perfil")
    new_followers: int = Field(alias="Novos Seguidores")
    main_hashtag: str = Field(alias="Hashtag Principal")
    
    class Config:
        allow_population_by_field_name = True

class StudentAnalytics(BaseModel):
    """Analytics model for student data."""
    total_students: int
    active_students: int
    inactive_students: int
    plan_distribution: dict
    neighborhood_distribution: dict
    gender_distribution: dict
    gympass_users: int
    average_monthly_value: float
    total_monthly_revenue: float

class InstagramAnalytics(BaseModel):
    """Analytics model for Instagram data."""
    total_posts: int
    total_likes: int
    total_comments: int
    total_saves: int
    total_reach: int
    total_profile_visits: int
    total_new_followers: int
    average_engagement_rate: float
    hashtag_performance: dict
    daily_performance: dict

class CrossPlatformAnalytics(BaseModel):
    """Cross-platform analytics model."""
    correlation_score: float
    engagement_to_enrollment_rate: float
    top_performing_content_types: list
    optimal_posting_times: dict
    geographic_insights: dict
    revenue_impact: float 