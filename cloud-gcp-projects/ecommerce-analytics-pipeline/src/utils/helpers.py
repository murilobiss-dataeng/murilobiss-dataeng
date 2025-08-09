#!/usr/bin/env python3
"""
🛠️ Helpers Module

This module provides common utility functions and helper classes for the e-commerce analytics pipeline.
These are general-purpose utilities that can be used across different pipeline stages.

Author: Data Engineering Team
Version: 1.0.0
"""

import json
import csv
import hashlib
import re
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union
from pathlib import Path
import pandas as pd


class DataHelpers:
    """Helper class for common data operations."""
    
    @staticmethod
    def generate_id(data: Dict[str, Any], fields: List[str]) -> str:
        """
        Generate a unique ID based on specified fields.
        
        Args:
            data: Dictionary containing the data
            fields: List of field names to use for ID generation
            
        Returns:
            str: MD5 hash of the concatenated field values
        """
        id_string = "|".join(str(data.get(field, "")) for field in fields)
        return hashlib.md5(id_string.encode()).hexdigest()
    
    @staticmethod
    def clean_string(value: str) -> str:
        """
        Clean and normalize a string value.
        
        Args:
            value: String to clean
            
        Returns:
            str: Cleaned string
        """
        if not isinstance(value, str):
            return str(value)
        
        # Remove extra whitespace
        cleaned = re.sub(r'\s+', ' ', value.strip())
        # Remove special characters that might cause issues
        cleaned = re.sub(r'[^\w\s\-_.,]', '', cleaned)
        return cleaned
    
    @staticmethod
    def parse_date(date_string: str, formats: Optional[List[str]] = None) -> Optional[datetime]:
        """
        Parse a date string using multiple formats.
        
        Args:
            date_string: String representation of date
            formats: List of date formats to try
            
        Returns:
            datetime: Parsed datetime object or None if parsing fails
        """
        if formats is None:
            formats = [
                '%Y-%m-%d',
                '%Y-%m-%d %H:%M:%S',
                '%d/%m/%Y',
                '%m/%d/%Y',
                '%Y-%m-%dT%H:%M:%S',
                '%Y-%m-%dT%H:%M:%S.%f'
            ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_string, fmt)
            except ValueError:
                continue
        
        return None
    
    @staticmethod
    def format_date(date_obj: datetime, format_string: str = '%Y-%m-%d') -> str:
        """
        Format a datetime object to string.
        
        Args:
            date_obj: Datetime object to format
            format_string: Format string
            
        Returns:
            str: Formatted date string
        """
        return date_obj.strftime(format_string)


class FileHelpers:
    """Helper class for file operations."""
    
    @staticmethod
    def ensure_directory(path: Union[str, Path]) -> Path:
        """
        Ensure a directory exists, create if it doesn't.
        
        Args:
            path: Directory path
            
        Returns:
            Path: Path object for the directory
        """
        path_obj = Path(path)
        path_obj.mkdir(parents=True, exist_ok=True)
        return path_obj
    
    @staticmethod
    def get_file_extension(file_path: Union[str, Path]) -> str:
        """
        Get file extension from path.
        
        Args:
            file_path: Path to the file
            
        Returns:
            str: File extension (without dot)
        """
        return Path(file_path).suffix.lstrip('.')
    
    @staticmethod
    def is_valid_file(file_path: Union[str, Path], required_extensions: Optional[List[str]] = None) -> bool:
        """
        Check if a file is valid and has required extension.
        
        Args:
            file_path: Path to the file
            required_extensions: List of allowed extensions
            
        Returns:
            bool: True if file is valid
        """
        path_obj = Path(file_path)
        
        if not path_obj.exists() or not path_obj.is_file():
            return False
        
        if required_extensions:
            return path_obj.suffix.lstrip('.') in required_extensions
        
        return True


class ValidationHelpers:
    """Helper class for data validation."""
    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """
        Validate email format.
        
        Args:
            email: Email string to validate
            
        Returns:
            bool: True if email is valid
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def is_valid_phone(phone: str) -> bool:
        """
        Validate phone number format.
        
        Args:
            phone: Phone string to validate
            
        Returns:
            bool: True if phone is valid
        """
        # Remove all non-digit characters
        digits_only = re.sub(r'\D', '', phone)
        return len(digits_only) >= 10
    
    @staticmethod
    def is_valid_postal_code(postal_code: str) -> bool:
        """
        Validate postal code format (US format).
        
        Args:
            postal_code: Postal code string to validate
            
        Returns:
            bool: True if postal code is valid
        """
        pattern = r'^\d{5}(-\d{4})?$'
        return bool(re.match(pattern, postal_code))
    
    @staticmethod
    def is_valid_currency(amount: Union[str, float]) -> bool:
        """
        Validate currency amount.
        
        Args:
            amount: Amount to validate
            
        Returns:
            bool: True if amount is valid
        """
        try:
            float_amount = float(amount)
            return float_amount >= 0
        except (ValueError, TypeError):
            return False


class ConversionHelpers:
    """Helper class for data type conversions."""
    
    @staticmethod
    def safe_int(value: Any, default: int = 0) -> int:
        """
        Safely convert value to integer.
        
        Args:
            value: Value to convert
            default: Default value if conversion fails
            
        Returns:
            int: Converted integer or default
        """
        try:
            return int(float(value))
        except (ValueError, TypeError):
            return default
    
    @staticmethod
    def safe_float(value: Any, default: float = 0.0) -> float:
        """
        Safely convert value to float.
        
        Args:
            value: Value to convert
            default: Default value if conversion fails
            
        Returns:
            float: Converted float or default
        """
        try:
            return float(value)
        except (ValueError, TypeError):
            return default
    
    @staticmethod
    def safe_bool(value: Any, default: bool = False) -> bool:
        """
        Safely convert value to boolean.
        
        Args:
            value: Value to convert
            default: Default value if conversion fails
            
        Returns:
            bool: Converted boolean or default
        """
        if isinstance(value, bool):
            return value
        elif isinstance(value, str):
            return value.lower() in ('true', '1', 'yes', 'on')
        elif isinstance(value, (int, float)):
            return value != 0
        else:
            return default


def create_dataframe(data: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Create a pandas DataFrame from a list of dictionaries.
    
    Args:
        data: List of dictionaries
        
    Returns:
        pd.DataFrame: Created DataFrame
    """
    return pd.DataFrame(data)


def save_to_json(data: Any, file_path: Union[str, Path], indent: int = 2) -> bool:
    """
    Save data to JSON file.
    
    Args:
        data: Data to save
        file_path: Path to save the file
        indent: JSON indentation
        
    Returns:
        bool: True if successful
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, default=str)
        return True
    except Exception:
        return False


def load_from_json(file_path: Union[str, Path]) -> Optional[Any]:
    """
    Load data from JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Any: Loaded data or None if failed
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None


def save_to_csv(data: List[Dict[str, Any]], file_path: Union[str, Path]) -> bool:
    """
    Save data to CSV file.
    
    Args:
        data: List of dictionaries to save
        file_path: Path to save the file
        
    Returns:
        bool: True if successful
    """
    try:
        if not data:
            return False
        
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)
        return True
    except Exception:
        return False


def load_from_csv(file_path: Union[str, Path]) -> Optional[pd.DataFrame]:
    """
    Load data from CSV file.
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        pd.DataFrame: Loaded DataFrame or None if failed
    """
    try:
        return pd.read_csv(file_path)
    except Exception:
        return None
