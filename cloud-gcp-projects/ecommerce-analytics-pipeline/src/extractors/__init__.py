#!/usr/bin/env python3
"""
📥 Extractors Package

This package contains data extraction modules for the e-commerce analytics pipeline.
Each extractor is responsible for pulling data from specific sources and
preparing it for transformation.

Author: Data Engineering Team
Version: 1.0.0
"""

from .data_extractor import DataExtractor

__all__ = ['DataExtractor']
__version__ = "1.0.0"
