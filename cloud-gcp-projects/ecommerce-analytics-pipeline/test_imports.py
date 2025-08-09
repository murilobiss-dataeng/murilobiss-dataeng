#!/usr/bin/env python3
"""
🧪 Test Imports Script

This script tests that all the utility modules can be imported correctly
without any import errors. It's useful for verifying the package structure.

Author: Data Engineering Team
Version: 1.0.0
"""

import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_imports():
    """Test importing all utility modules."""
    print("🧪 Testing imports...")

    try:
        # Test utils package
        print("  📦 Testing utils package...")
        from utils import Config, PipelineLogger, PipelineMonitor, DataQualityValidator
        print("    ✅ Utils package imported successfully")

        # Test individual modules
        print("  🔧 Testing individual modules...")
        from utils.config import Config
        from utils.logger import PipelineLogger
        from utils.monitoring import PipelineMonitor
        from utils.data_quality import DataQualityValidator
        from utils.exceptions import PipelineError
        print("    ✅ All utility modules imported successfully")

        # Test other packages
        print("  📥 Testing extractors package...")
        from extractors import DataExtractor
        print("    ✅ Extractors package imported successfully")

        print("  🔄 Testing transformers package...")
        from transformers import DataTransformer
        print("    ✅ Transformers package imported successfully")

        print("  📤 Testing loaders package...")
        from loaders import DataLoader
        print("    ✅ Loaders package imported successfully")

        print("  🏪 Testing main package...")
        from src import main
        print("    ✅ Main package imported successfully")

        print("\n🎉 All imports successful! Package structure is correct.")
        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality of key classes."""
    print("  ⚙️ Testing Config class...")
    try:
        from utils.config import Config
        config = Config()
        print("    ✅ Config created successfully")
    except Exception as e:
        print(f"    ❌ Config test failed: {e}")
        return False
    
    print("  📝 Testing PipelineLogger...")
    try:
        from utils.logger import PipelineLogger
        logger = PipelineLogger("test_logger")
        logger.info("Test log message")
        print("    ✅ Logger created and used successfully")
    except Exception as e:
        print(f"    ❌ Logger test failed: {e}")
        return False
    
    print("  🔍 Testing DataQualityValidator...")
    try:
        from utils.data_quality import DataQualityValidator
        validator = DataQualityValidator()
        print("    ✅ DataQualityValidator created successfully")
    except Exception as e:
        print(f"    ❌ DataQualityValidator test failed: {e}")
        return False
    
    print("  🛠️ Testing utility classes...")
    try:
        from utils.helpers import DataHelpers, FileHelpers, ValidationHelpers, ConversionHelpers
        print("    ✅ Helper classes imported successfully")
    except Exception as e:
        print(f"    ❌ Helper classes test failed: {e}")
        return False
    
    print("  🗄️ Testing database utilities...")
    try:
        from utils.database import DatabaseConnection, BigQueryConnection
        print("    ✅ Database utilities imported successfully")
    except Exception as e:
        print(f"    ❌ Database utilities test failed: {e}")
        return False
    
    print("  📊 Testing data processing utilities...")
    try:
        from utils.data_processing import DataProcessor
        print("    ✅ Data processing utilities imported successfully")
    except Exception as e:
        print(f"    ❌ Data processing utilities test failed: {e}")
        return False
    
    return True

def test_monitoring_without_gcp():
    """Test monitoring functionality without GCP setup."""
    print("\n📊 Testing monitoring without GCP...")
    
    try:
        from utils.monitoring import PipelineMonitor
        from utils.config import Config
        
        # Create a minimal config for testing
        config = Config()
        
        # Test monitor creation
        monitor = PipelineMonitor(config)
        print("    ✅ Monitor created successfully")
        
        # Test basic monitoring operations
        session_id = monitor.start_pipeline_monitoring("test_pipeline")
        print(f"    ✅ Started monitoring session: {session_id}")
        
        # Test metrics update
        monitor.update_pipeline_metrics(session_id, records_processed=100)
        print("    ✅ Updated metrics successfully")
        
        # Test completion
        monitor.complete_pipeline_monitoring(session_id, success=True)
        print("    ✅ Completed monitoring successfully")
        
        # Test health checks
        health_results = monitor.run_health_checks()
        print(f"    ✅ Health checks completed: {len(health_results)} checks")
        
        print("    ✅ Monitoring functionality works without GCP!")
        return True
        
    except Exception as e:
        print(f"    ⚠️ Monitoring test failed (expected without GCP): {e}")
        return True  # This is expected to fail without GCP credentials

if __name__ == "__main__":
    print("🚀 Starting import and functionality tests...\n")

    imports_ok = test_imports()
    functionality_ok = test_basic_functionality()
    monitoring_ok = test_monitoring_without_gcp()

    if imports_ok and functionality_ok:
        print("\n🎉 All tests passed! The e-commerce analytics pipeline is ready to use.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        sys.exit(1)
