# Social FIT Data Intelligence Platform - Development Guide

## Development Environment Setup

### Prerequisites

- Python 3.9 or higher
- Git
- Virtual environment tool (venv, conda, etc.)
- Code editor (VS Code, PyCharm, etc.)

### Initial Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/social_fit.git
   cd social_fit
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -e .[dev]
   ```

4. **Configure environment**
   ```bash
   cp env_example.txt .env
   # Edit .env with your development credentials
   ```

5. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

## Project Structure

```
social_fit/
├── src/                    # Main source code
│   ├── __init__.py        # Package initialization
│   ├── etl/               # ETL pipeline components
│   │   ├── __init__.py
│   │   └── etl_pipeline.py
│   ├── analytics/         # Analytics and insights engine
│   │   ├── __init__.py
│   │   └── analytics.py
│   ├── database/          # Database management
│   │   ├── __init__.py
│   │   └── database.py
│   ├── models/            # Data models and schemas
│   │   ├── __init__.py
│   │   └── models.py
│   ├── config/            # Configuration management
│   │   ├── __init__.py
│   │   └── config.py
│   ├── dashboard.py       # Web dashboard
│   └── main.py           # Main application entry point
├── tests/                 # Test suite
│   ├── __init__.py
│   ├── unit/             # Unit tests
│   │   ├── __init__.py
│   │   ├── test_etl.py
│   │   ├── test_analytics.py
│   │   └── test_models.py
│   └── integration/      # Integration tests
│       ├── __init__.py
│       ├── test_database.py
│       └── test_pipeline.py
├── scripts/              # Utility scripts
│   ├── create_tables_public_final.sql
│   └── debug_tables.py
├── docs/                 # Documentation
│   ├── API.md
│   ├── DEVELOPMENT.md
│   └── DEPLOYMENT.md
├── data/                 # Data files
├── logs/                 # Application logs
├── main.py              # CLI entry point
├── setup.py             # Package setup
├── pytest.ini          # Test configuration
├── requirements.txt     # Python dependencies
└── README.md           # Project documentation
```

## Development Workflow

### 1. Feature Development

1. **Create feature branch**
   ```bash
   git checkout -b feature/new-feature
   ```

2. **Implement changes**
   - Follow coding standards
   - Add comprehensive tests
   - Update documentation

3. **Run tests**
   ```bash
   pytest
   pytest --cov=src
   ```

4. **Code quality checks**
   ```bash
   black src/ tests/
   flake8 src/ tests/
   mypy src/
   ```

5. **Commit changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

6. **Push and create PR**
   ```bash
   git push origin feature/new-feature
   # Create pull request on GitHub
   ```

### 2. Testing Strategy

#### Unit Tests
- Test individual functions and classes
- Mock external dependencies
- Focus on business logic

#### Integration Tests
- Test component interactions
- Use test database
- Validate end-to-end workflows

#### Test Structure
```python
# tests/unit/test_etl.py
import pytest
from src.etl import SocialFITETL

class TestSocialFITETL:
    def test_extract_data(self):
        """Test data extraction functionality"""
        etl = SocialFITETL()
        # Test implementation
        
    def test_transform_students(self):
        """Test student data transformation"""
        # Test implementation
        
    @pytest.mark.integration
    def test_full_pipeline(self):
        """Test complete ETL pipeline"""
        # Test implementation
```

### 3. Code Quality Standards

#### Python Style Guide
- Follow PEP 8
- Use type hints
- Add docstrings
- Keep functions small and focused

#### Example Code
```python
from typing import List, Dict, Any
from loguru import logger

def process_student_data(students: List[Dict[str, Any]]) -> List[Student]:
    """
    Process and validate student data.
    
    Args:
        students: List of student dictionaries
        
    Returns:
        List of validated Student objects
        
    Raises:
        ValidationError: If data validation fails
    """
    processed_students = []
    
    for student_data in students:
        try:
            student = Student(**student_data)
            processed_students.append(student)
            logger.debug(f"Processed student: {student.name}")
        except Exception as e:
            logger.error(f"Failed to process student: {e}")
            raise ValidationError(f"Invalid student data: {e}")
    
    return processed_students
```

### 4. Configuration Management

#### Environment Variables
```python
# src/config/config.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Supabase Configuration
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_SERVICE_ROLE_KEY: str
    
    # Application Configuration
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    BATCH_SIZE: int = 100
    
    # Database Configuration
    DATABASE_URL: Optional[str] = None
    
    class Config:
        env_file = ".env"
```

#### Development vs Production
```python
# Development settings
DEBUG=True
LOG_LEVEL=DEBUG
BATCH_SIZE=50

# Production settings
DEBUG=False
LOG_LEVEL=WARNING
BATCH_SIZE=1000
```

## Database Development

### Local Development Database

1. **Setup local PostgreSQL**
   ```bash
   # Using Docker
   docker run --name social-fit-db \
     -e POSTGRES_PASSWORD=password \
     -e POSTGRES_DB=social_fit \
     -p 5432:5432 \
     -d postgres:13
   ```

2. **Create tables**
   ```bash
   psql -h localhost -U postgres -d social_fit -f scripts/create_tables_public_final.sql
   ```

3. **Update .env**
   ```env
   DATABASE_URL=postgresql://postgres:password@localhost:5432/social_fit
   ```

### Supabase Development

1. **Create development project**
   - Create new Supabase project
   - Use development credentials

2. **Setup schema**
   ```sql
   -- Run in Supabase SQL editor
   \i scripts/create_tables_public_final.sql
   ```

3. **Configure RLS**
   ```sql
   -- Enable RLS
   ALTER TABLE students ENABLE ROW LEVEL SECURITY;
   ALTER TABLE instagram_posts ENABLE ROW LEVEL SECURITY;
   ALTER TABLE analytics ENABLE ROW LEVEL SECURITY;
   
   -- Create policies
   CREATE POLICY "Enable read access for all users" ON students FOR SELECT USING (true);
   CREATE POLICY "Enable insert access for authenticated users" ON students FOR INSERT WITH CHECK (true);
   ```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test categories
pytest tests/unit/
pytest tests/integration/

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test
pytest tests/unit/test_etl.py::TestSocialFITETL::test_extract_data

# Run with markers
pytest -m "not slow"
pytest -m integration
```

### Test Data

Create test data fixtures:

```python
# tests/conftest.py
import pytest
import pandas as pd
from datetime import datetime

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
```

## Debugging

### Logging Configuration

```python
# Development logging
import logging
from loguru import logger

# Configure detailed logging for development
logger.add(
    "logs/debug.log",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
    rotation="1 day"
)
```

### Debug Tools

1. **Python Debugger**
   ```python
   import pdb; pdb.set_trace()
   ```

2. **Loguru Debug**
   ```python
   logger.debug(f"Variable value: {variable}")
   ```

3. **Data Validation**
   ```python
   from src.models import Student
   
   try:
       student = Student(**data)
       print(f"Valid student: {student}")
   except Exception as e:
       print(f"Validation error: {e}")
   ```

## Performance Optimization

### Database Optimization

1. **Indexes**
   ```sql
   CREATE INDEX idx_students_neighborhood ON students(neighborhood);
   CREATE INDEX idx_instagram_date ON instagram_posts(post_date);
   CREATE INDEX idx_analytics_date ON analytics(date);
   ```

2. **Batch Processing**
   ```python
   # Process data in batches
   batch_size = settings.BATCH_SIZE
   for i in range(0, len(data), batch_size):
       batch = data[i:i + batch_size]
       process_batch(batch)
   ```

3. **Connection Pooling**
   ```python
   # Use connection pooling for database connections
   from sqlalchemy import create_engine
   
   engine = create_engine(
       DATABASE_URL,
       pool_size=10,
       max_overflow=20,
       pool_pre_ping=True
   )
   ```

### Memory Optimization

1. **Generator Functions**
   ```python
   def process_large_dataset(file_path):
       """Process large datasets using generators"""
       for chunk in pd.read_csv(file_path, chunksize=1000):
           yield process_chunk(chunk)
   ```

2. **Data Types**
   ```python
   # Use appropriate data types
   df['gender'] = df['gender'].astype('category')
   df['plan_type'] = df['plan_type'].astype('category')
   ```

## Deployment Preparation

### Environment Configuration

1. **Production Settings**
   ```env
   DEBUG=False
   LOG_LEVEL=WARNING
   BATCH_SIZE=1000
   ```

2. **Security**
   ```python
   # Validate all environment variables
   settings = Settings()
   assert settings.SUPABASE_URL, "SUPABASE_URL is required"
   assert settings.SUPABASE_SERVICE_ROLE_KEY, "SUPABASE_SERVICE_ROLE_KEY is required"
   ```

### Health Checks

```python
def health_check():
    """Application health check"""
    try:
        # Test database connection
        db = DatabaseManager()
        if not db.test_connection():
            return False, "Database connection failed"
        
        # Test basic functionality
        etl = SocialFITETL()
        if not etl.extract_data():
            return False, "Data extraction failed"
        
        return True, "Application healthy"
    except Exception as e:
        return False, f"Health check failed: {e}"
```

## Contributing Guidelines

### Code Review Process

1. **Pull Request Requirements**
   - All tests must pass
   - Code coverage > 80%
   - No linting errors
   - Documentation updated

2. **Review Checklist**
   - [ ] Code follows style guide
   - [ ] Tests are comprehensive
   - [ ] Documentation is updated
   - [ ] No security vulnerabilities
   - [ ] Performance impact considered

### Commit Message Format

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Maintenance tasks

Examples:
```
feat(etl): add incremental update functionality
fix(database): resolve connection timeout issue
docs(api): update API documentation
test(analytics): add unit tests for correlation analysis
```

## Support and Resources

### Documentation
- [Python Documentation](https://docs.python.org/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
- [Supabase Documentation](https://supabase.com/docs)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

### Tools
- [Black Code Formatter](https://black.readthedocs.io/)
- [Flake8 Linter](https://flake8.pycqa.org/)
- [MyPy Type Checker](https://mypy.readthedocs.io/)
- [Pytest Testing Framework](https://docs.pytest.org/)

### Community
- [Python Discord](https://discord.gg/python)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/python)
- [GitHub Issues](https://github.com/your-username/social_fit/issues) 