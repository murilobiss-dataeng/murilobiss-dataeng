"""
Test Configuration and Fixtures
==============================

Shared test configuration, fixtures, and utilities for the test suite.
"""

import pytest
import pandas as pd
from datetime import datetime
from pathlib import Path
import sys

# Add src to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

@pytest.fixture
def sample_students_df():
    """Sample student data for testing"""
    return pd.DataFrame({
        'ID': [1, 2, 3],
        'Nome': ['João Silva', 'Maria Santos', 'Pedro Costa'],
        'Gênero': ['M', 'F', 'M'],
        'Data_Nascimento': ['1990-01-01', '1985-05-15', '1995-12-20'],
        'Endereço': ['Rua A, 123', 'Rua B, 456', 'Rua C, 789'],
        'Bairro': ['Centro', 'Vila Nova', 'Jardim'],
        'Tipo_Plano': ['Mensal', 'Trimestral', 'Anual'],
        'Gympass': [True, False, True],
        'Valor_Mensal_USD': [89.90, 79.90, 69.90],
        'Valor_Total_USD': [89.90, 239.70, 838.80],
        'Data_Início_Plano': ['2024-01-01', '2024-01-15', '2024-02-01'],
        'Plano_Ativo': [True, True, False]
    })

@pytest.fixture
def sample_instagram_df():
    """Sample Instagram data for testing"""
    return pd.DataFrame({
        'Data': ['2024-01-01', '2024-01-02', '2024-01-03'],
        'Curtidas': [150, 200, 180],
        'Comentários': [25, 30, 28],
        'Salvos': [10, 15, 12],
        'Alcance': [1000, 1200, 1100],
        'Visitas_Perfil': [50, 60, 55],
        'Novos_Seguidores': [15, 20, 18],
        'Hashtag_Principal': ['#socialfit', '#fitness', '#workout']
    })

@pytest.fixture
def mock_supabase_config():
    """Mock Supabase configuration for testing"""
    return {
        'url': 'https://test-project.supabase.co',
        'anon_key': 'test-anon-key',
        'service_role_key': 'test-service-role-key'
    }

@pytest.fixture
def test_data_dir():
    """Test data directory"""
    return Path(__file__).parent.parent / "data"

@pytest.fixture
def sample_student_dict():
    """Sample student dictionary for model testing"""
    return {
        'id': 1,
        'name': 'João Silva',
        'gender': 'M',
        'birth_date': datetime(1990, 1, 1),
        'address': 'Rua A, 123',
        'neighborhood': 'Centro',
        'plan_type': 'Mensal',
        'gympass': True,
        'monthly_value': 89.90,
        'total_value': 89.90,
        'plan_start_date': datetime(2024, 1, 1),
        'active_plan': True
    }

@pytest.fixture
def sample_instagram_post_dict():
    """Sample Instagram post dictionary for model testing"""
    return {
        'date': datetime(2024, 1, 1),
        'likes': 150,
        'comments': 25,
        'saves': 10,
        'reach': 1000,
        'profile_visits': 50,
        'new_followers': 15,
        'main_hashtag': '#socialfit'
    } 