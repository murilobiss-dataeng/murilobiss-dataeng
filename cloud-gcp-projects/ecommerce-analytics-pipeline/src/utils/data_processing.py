#!/usr/bin/env python3
"""
🔄 Data Processing Utilities Module

This module provides utilities for common data processing operations in the e-commerce analytics pipeline.
It includes data cleaning, transformation, aggregation, and enrichment functions.

Author: Data Engineering Team
Version: 1.0.0
"""

import pandas as pd
import numpy as np
from typing import Any, Dict, List, Optional, Union, Tuple, Callable
from datetime import datetime, timedelta
import logging
from functools import wraps
import time

from .exceptions import TransformationError


class DataProcessor:
    """Main data processing class with common operations."""
    
    def __init__(self):
        """Initialize the data processor."""
        self.logger = logging.getLogger(__name__)
        self.processing_stats = {
            'records_processed': 0,
            'records_failed': 0,
            'processing_time': 0.0
        }
    
    def clean_dataframe(self, df: pd.DataFrame, 
                       remove_duplicates: bool = True,
                       handle_missing: str = 'drop',  # 'drop', 'fill', 'interpolate'
                       fill_value: Any = None,
                       text_columns: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Clean a pandas DataFrame.
        
        Args:
            df: Input DataFrame
            remove_duplicates: Whether to remove duplicate rows
            handle_missing: Strategy for handling missing values
            fill_value: Value to fill missing values with (if handle_missing='fill')
            text_columns: List of text columns to clean
            
        Returns:
            pd.DataFrame: Cleaned DataFrame
        """
        try:
            df_clean = df.copy()
            
            # Remove duplicates
            if remove_duplicates:
                initial_count = len(df_clean)
                df_clean = df_clean.drop_duplicates()
                removed_count = initial_count - len(df_clean)
                self.logger.info(f"Removed {removed_count} duplicate rows")
            
            # Handle missing values
            if handle_missing == 'drop':
                initial_count = len(df_clean)
                df_clean = df_clean.dropna()
                removed_count = initial_count - len(df_clean)
                self.logger.info(f"Removed {removed_count} rows with missing values")
            elif handle_missing == 'fill':
                df_clean = df_clean.fillna(fill_value)
                self.logger.info("Filled missing values")
            elif handle_missing == 'interpolate':
                df_clean = df_clean.interpolate()
                self.logger.info("Interpolated missing values")
            
            # Clean text columns
            if text_columns:
                for col in text_columns:
                    if col in df_clean.columns:
                        df_clean[col] = df_clean[col].astype(str).str.strip()
                        df_clean[col] = df_clean[col].replace('', np.nan)
            
            return df_clean
            
        except Exception as e:
            self.logger.error(f"Data cleaning failed: {e}")
            raise TransformationError(f"Data cleaning failed: {e}")
    
    def standardize_columns(self, df: pd.DataFrame, 
                           column_mapping: Dict[str, str],
                           case: str = 'lower') -> pd.DataFrame:
        """
        Standardize column names.
        
        Args:
            df: Input DataFrame
            column_mapping: Dictionary mapping old names to new names
            case: Case for column names ('lower', 'upper', 'title')
            
        Returns:
            pd.DataFrame: DataFrame with standardized columns
        """
        try:
            df_std = df.copy()
            
            # Apply column mapping
            df_std = df_std.rename(columns=column_mapping)
            
            # Apply case transformation
            if case == 'lower':
                df_std.columns = df_std.columns.str.lower()
            elif case == 'upper':
                df_std.columns = df_std.columns.str.upper()
            elif case == 'title':
                df_std.columns = df_std.columns.str.title()
            
            # Replace spaces and special characters
            df_std.columns = df_std.columns.str.replace(' ', '_')
            df_std.columns = df_std.columns.str.replace('-', '_')
            df_std.columns = df_std.columns.str.replace('.', '_')
            
            self.logger.info(f"Standardized {len(df_std.columns)} columns")
            return df_std
            
        except Exception as e:
            self.logger.error(f"Column standardization failed: {e}")
            raise TransformationError(f"Column standardization failed: {e}")
    
    def convert_data_types(self, df: pd.DataFrame, 
                          type_mapping: Dict[str, str],
                          date_columns: Optional[List[str]] = None,
                          date_format: str = '%Y-%m-%d') -> pd.DataFrame:
        """
        Convert data types of DataFrame columns.
        
        Args:
            df: Input DataFrame
            type_mapping: Dictionary mapping column names to target types
            date_columns: List of columns to convert to datetime
            date_format: Format for date parsing
            
        Returns:
            pd.DataFrame: DataFrame with converted data types
        """
        try:
            df_converted = df.copy()
            
            # Convert date columns
            if date_columns:
                for col in date_columns:
                    if col in df_converted.columns:
                        df_converted[col] = pd.to_datetime(df_converted[col], format=date_format, errors='coerce')
            
            # Apply type conversions
            for col, target_type in type_mapping.items():
                if col in df_converted.columns:
                    try:
                        if target_type == 'int':
                            df_converted[col] = pd.to_numeric(df_converted[col], errors='coerce').astype('Int64')
                        elif target_type == 'float':
                            df_converted[col] = pd.to_numeric(df_converted[col], errors='coerce')
                        elif target_type == 'bool':
                            df_converted[col] = df_converted[col].astype(bool)
                        elif target_type == 'category':
                            df_converted[col] = df_converted[col].astype('category')
                        elif target_type == 'string':
                            df_converted[col] = df_converted[col].astype(str)
                    except Exception as e:
                        self.logger.warning(f"Failed to convert column {col} to {target_type}: {e}")
            
            self.logger.info(f"Converted data types for {len(type_mapping)} columns")
            return df_converted
            
        except Exception as e:
            self.logger.error(f"Data type conversion failed: {e}")
            raise TransformationError(f"Data type conversion failed: {e}")
    
    def aggregate_data(self, df: pd.DataFrame, 
                      group_columns: List[str],
                      agg_functions: Dict[str, List[str]]) -> pd.DataFrame:
        """
        Aggregate data by grouping columns.
        
        Args:
            df: Input DataFrame
            group_columns: Columns to group by
            agg_functions: Dictionary mapping columns to aggregation functions
            
        Returns:
            pd.DataFrame: Aggregated DataFrame
        """
        try:
            # Perform aggregation
            df_agg = df.groupby(group_columns).agg(agg_functions).reset_index()
            
            # Flatten column names if multi-level
            if isinstance(df_agg.columns, pd.MultiIndex):
                df_agg.columns = [f"{col[0]}_{col[1]}" if col[1] else col[0] 
                                for col in df_agg.columns]
            
            self.logger.info(f"Aggregated data by {len(group_columns)} columns")
            return df_agg
            
        except Exception as e:
            self.logger.error(f"Data aggregation failed: {e}")
            raise TransformationError(f"Data aggregation failed: {e}")
    
    def pivot_data(self, df: pd.DataFrame,
                   index: str,
                   columns: str,
                   values: str,
                   fill_value: Any = 0) -> pd.DataFrame:
        """
        Pivot data from long to wide format.
        
        Args:
            df: Input DataFrame
            index: Column to use as index
            columns: Column to use as columns
            values: Column to use as values
            fill_value: Value to fill missing values
            
        Returns:
            pd.DataFrame: Pivoted DataFrame
        """
        try:
            df_pivot = df.pivot_table(
                index=index,
                columns=columns,
                values=values,
                fill_value=fill_value,
                aggfunc='first'
            ).reset_index()
            
            self.logger.info(f"Pivoted data: {index} -> {columns} -> {values}")
            return df_pivot
            
        except Exception as e:
            self.logger.error(f"Data pivoting failed: {e}")
            raise TransformationError(f"Data pivoting failed: {e}")
    
    def merge_dataframes(self, df1: pd.DataFrame,
                        df2: pd.DataFrame,
                        on: Union[str, List[str]],
                        how: str = 'inner',
                        suffixes: Tuple[str, str] = ('_x', '_y')) -> pd.DataFrame:
        """
        Merge two DataFrames.
        
        Args:
            df1: First DataFrame
            df2: Second DataFrame
            on: Column(s) to merge on
            how: Type of merge ('inner', 'left', 'right', 'outer')
            suffixes: Suffixes for duplicate columns
            
        Returns:
            pd.DataFrame: Merged DataFrame
        """
        try:
            df_merged = df1.merge(df2, on=on, how=how, suffixes=suffixes)
            
            self.logger.info(f"Merged DataFrames: {len(df1)} + {len(df2)} -> {len(df_merged)} rows")
            return df_merged
            
        except Exception as e:
            self.logger.error(f"DataFrame merge failed: {e}")
            raise TransformationError(f"DataFrame merge failed: {e}")
    
    def add_calculated_columns(self, df: pd.DataFrame,
                              calculations: Dict[str, str]) -> pd.DataFrame:
        """
        Add calculated columns to DataFrame.
        
        Args:
            df: Input DataFrame
            calculations: Dictionary mapping new column names to calculation expressions
            
        Returns:
            pd.DataFrame: DataFrame with calculated columns
        """
        try:
            df_calc = df.copy()
            
            for col_name, expression in calculations.items():
                try:
                    # Use eval for simple calculations (be careful with user input)
                    df_calc[col_name] = df_calc.eval(expression)
                    self.logger.debug(f"Added calculated column: {col_name} = {expression}")
                except Exception as e:
                    self.logger.warning(f"Failed to calculate column {col_name}: {e}")
            
            self.logger.info(f"Added {len(calculations)} calculated columns")
            return df_calc
            
        except Exception as e:
            self.logger.error(f"Column calculation failed: {e}")
            raise TransformationError(f"Column calculation failed: {e}")
    
    def filter_data(self, df: pd.DataFrame,
                   filters: Dict[str, Any]) -> pd.DataFrame:
        """
        Filter DataFrame based on conditions.
        
        Args:
            df: Input DataFrame
            filters: Dictionary mapping column names to filter values or conditions
            
        Returns:
            pd.DataFrame: Filtered DataFrame
        """
        try:
            df_filtered = df.copy()
            
            for column, condition in filters.items():
                if column in df_filtered.columns:
                    if isinstance(condition, (list, tuple)):
                        df_filtered = df_filtered[df_filtered[column].isin(condition)]
                    elif isinstance(condition, dict):
                        # Handle range conditions like {'min': 0, 'max': 100}
                        if 'min' in condition:
                            df_filtered = df_filtered[df_filtered[column] >= condition['min']]
                        if 'max' in condition:
                            df_filtered = df_filtered[df_filtered[column] <= condition['max']]
                    else:
                        df_filtered = df_filtered[df_filtered[column] == condition]
            
            self.logger.info(f"Filtered data: {len(df)} -> {len(df_filtered)} rows")
            return df_filtered
            
        except Exception as e:
            self.logger.error(f"Data filtering failed: {e}")
            raise TransformationError(f"Data filtering failed: {e}")
    
    def sample_data(self, df: pd.DataFrame,
                   sample_size: Optional[int] = None,
                   sample_fraction: Optional[float] = None,
                   random_state: Optional[int] = None) -> pd.DataFrame:
        """
        Sample data from DataFrame.
        
        Args:
            df: Input DataFrame
            sample_size: Number of rows to sample
            sample_fraction: Fraction of rows to sample
            random_state: Random seed for reproducibility
            
        Returns:
            pd.DataFrame: Sampled DataFrame
        """
        try:
            if sample_size:
                df_sampled = df.sample(n=sample_size, random_state=random_state)
            elif sample_fraction:
                df_sampled = df.sample(frac=sample_fraction, random_state=random_state)
            else:
                raise ValueError("Either sample_size or sample_fraction must be specified")
            
            self.logger.info(f"Sampled data: {len(df)} -> {len(df_sampled)} rows")
            return df_sampled
            
        except Exception as e:
            self.logger.error(f"Data sampling failed: {e}")
            raise TransformationError(f"Data sampling failed: {e}")


def timing_decorator(func: Callable) -> Callable:
    """Decorator to measure function execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logging.info(f"Function {func.__name__} executed in {execution_time:.2f} seconds")
        return result
    return wrapper


def validate_dataframe(df: pd.DataFrame, 
                      required_columns: Optional[List[str]] = None,
                      min_rows: Optional[int] = None,
                      max_rows: Optional[int] = None) -> bool:
    """
    Validate DataFrame structure and content.
    
    Args:
        df: DataFrame to validate
        required_columns: List of required column names
        min_rows: Minimum number of rows required
        max_rows: Maximum number of rows allowed
        
    Returns:
        bool: True if validation passes
    """
    try:
        # Check if DataFrame is empty
        if df.empty:
            raise ValueError("DataFrame is empty")
        
        # Check required columns
        if required_columns:
            missing_columns = set(required_columns) - set(df.columns)
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Check row count
        if min_rows and len(df) < min_rows:
            raise ValueError(f"DataFrame has {len(df)} rows, minimum required: {min_rows}")
        
        if max_rows and len(df) > max_rows:
            raise ValueError(f"DataFrame has {len(df)} rows, maximum allowed: {max_rows}")
        
        return True
        
    except Exception as e:
        logging.error(f"DataFrame validation failed: {e}")
        return False


def create_summary_stats(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Create summary statistics for a DataFrame.
    
    Args:
        df: Input DataFrame
        
    Returns:
        Dict[str, Any]: Summary statistics
    """
    try:
        summary = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024 / 1024,
            'column_types': df.dtypes.to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'numeric_columns': df.select_dtypes(include=[np.number]).columns.tolist(),
            'categorical_columns': df.select_dtypes(include=['object', 'category']).columns.tolist(),
            'date_columns': df.select_dtypes(include=['datetime64']).columns.tolist()
        }
        
        # Add basic statistics for numeric columns
        if summary['numeric_columns']:
            summary['numeric_stats'] = df[summary['numeric_columns']].describe().to_dict()
        
        return summary
        
    except Exception as e:
        logging.error(f"Failed to create summary stats: {e}")
        return {}


def split_dataframe(df: pd.DataFrame, 
                   split_ratio: float = 0.8,
                   random_state: Optional[int] = None) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split DataFrame into training and testing sets.
    
    Args:
        df: Input DataFrame
        split_ratio: Ratio for training set (0.0 to 1.0)
        random_state: Random seed for reproducibility
        
    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: Training and testing DataFrames
    """
    try:
        if not 0 < split_ratio < 1:
            raise ValueError("split_ratio must be between 0 and 1")
        
        # Calculate split point
        split_point = int(len(df) * split_ratio)
        
        # Split the DataFrame
        train_df = df.iloc[:split_point]
        test_df = df.iloc[split_point:]
        
        logging.info(f"Split DataFrame: {len(train_df)} training, {len(test_df)} testing")
        return train_df, test_df
        
    except Exception as e:
        logging.error(f"DataFrame splitting failed: {e}")
        raise TransformationError(f"DataFrame splitting failed: {e}")
