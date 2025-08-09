#!/usr/bin/env python3
"""
📤 Loaders Package

This package contains data loading modules for the e-commerce analytics pipeline.
Each loader is responsible for writing transformed data to specific destinations
like BigQuery, Cloud Storage, or other data warehouses.

Author: Data Engineering Team
Version: 1.0.0
"""

from .data_loader import DataLoader

__all__ = ['DataLoader']
__version__ = "1.0.0"
