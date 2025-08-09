#!/usr/bin/env python3
"""
🔧 Utils Package

This package contains utility modules for the e-commerce analytics pipeline:
- config: Configuration management
- logger: Structured logging
- monitoring: Pipeline monitoring and metrics
- data_quality: Data validation and quality checks
- exceptions: Custom exception classes

Author: Data Engineering Team
Version: 1.0.0
"""

from .config import Config
from .logger import PipelineLogger, setup_logger, get_logger
from .monitoring import PipelineMonitor, create_monitor
from .data_quality import DataQualityValidator, create_validator
from .helpers import DataHelpers, FileHelpers, ValidationHelpers, ConversionHelpers
from .database import DatabaseConnection, BigQueryConnection, ConnectionPool, get_db_connection
from .exceptions import (
    PipelineError,
    ConfigurationError,
    DataQualityError,
    ExtractionError,
    TransformationError,
    LoadingError,
    DatabaseError,
    ConnectionError
)

__all__ = [
    'Config',
    'PipelineLogger',
    'setup_logger',
    'get_logger',
    'PipelineMonitor',
    'create_monitor',
    'DataQualityValidator',
    'create_validator',
    'DataHelpers',
    'FileHelpers',
    'ValidationHelpers',
    'ConversionHelpers',
    'DatabaseConnection',
    'BigQueryConnection',
    'ConnectionPool',
    'get_db_connection',
    'PipelineError',
    'ConfigurationError',
    'DataQualityError',
    'ExtractionError',
    'TransformationError',
    'LoadingError',
    'DatabaseError',
    'ConnectionError'
]

__version__ = "1.0.0"
