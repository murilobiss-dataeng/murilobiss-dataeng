#!/usr/bin/env python3
"""
🏪 E-commerce Analytics Pipeline

A comprehensive data engineering pipeline for e-commerce analytics built on Google Cloud Platform.
This pipeline extracts, transforms, and loads data from various sources to provide
actionable business insights.

Features:
- Multi-source data extraction
- Advanced data transformation and enrichment
- Data quality validation and monitoring
- Real-time pipeline monitoring and alerting
- Integration with BigQuery and Cloud Storage
- Comprehensive logging and error handling

Author: Data Engineering Team
Version: 1.0.0
"""

from .main import main
from .extractors import DataExtractor
from .transformers import DataTransformer
from .loaders import DataLoader
from .utils import (
    Config,
    PipelineLogger,
    PipelineMonitor,
    DataQualityValidator
)

__all__ = [
    'main',
    'DataExtractor',
    'DataTransformer',
    'DataLoader',
    'Config',
    'PipelineLogger',
    'PipelineMonitor',
    'DataQualityValidator'
]

__version__ = "1.0.0"
__author__ = "Data Engineering Team"
__description__ = "E-commerce Analytics Pipeline for Google Cloud Platform"
