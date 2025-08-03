#!/usr/bin/env python3
"""
Social FIT Data Intelligence Platform
====================================

Main entry point for the Social FIT ETL pipeline and analytics platform.
"""

import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.app import main

if __name__ == "__main__":
    main() 