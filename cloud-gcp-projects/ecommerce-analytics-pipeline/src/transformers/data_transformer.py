#!/usr/bin/env python3
"""
🔄 Data Transformer Module

This module handles data transformation and cleaning for the e-commerce analytics pipeline.
It includes data quality checks, enrichment, aggregation, and business logic implementation.

Author: Data Engineering Team
Version: 1.0.0
"""

import logging
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from utils.config import Config
from utils.exceptions import TransformationError


@dataclass
class DataQualityMetrics:
    """Data structure for data quality metrics."""
    total_records: int
    valid_records: int
    invalid_records: int
    quality_score: float
    missing_values: Dict[str, int]
    duplicate_records: int
    data_type_errors: int


class DataTransformer:
    """
    Data transformation class for e-commerce analytics pipeline.
    
    Handles data cleaning, enrichment, aggregation, and business logic
    implementation with comprehensive data quality monitoring.
    """
    
    def __init__(self, config: Config):
        """
        Initialize the data transformer.
        
        Args:
            config: Configuration object containing transformation settings
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Extract configuration
        self.quality_config = config.get('data_quality', {})
        self.business_rules = config.get('business_rules', {})
        self.aggregation_config = config.get('aggregation', {})
        
        self.logger.info("🔄 Data Transformer initialized successfully")
    
    def transform_customer_orders(self, orders_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Transform and clean customer orders data.
        
        Args:
            orders_data: Raw customer orders data
            
        Returns:
            Transformed and cleaned customer orders data
        """
        try:
            self.logger.info("🔄 Transforming customer orders data...")
            
            # Convert to DataFrame for easier manipulation
            df = pd.DataFrame(orders_data)
            
            # Data cleaning
            df = self._clean_customer_orders(df)
            
            # Data enrichment
            df = self._enrich_customer_orders(df)
            
            # Data validation
            quality_metrics = self._validate_data_quality(df, 'customer_orders')
            self.logger.info(f"📊 Data quality score: {quality_metrics.quality_score:.2f}")
            
            # Convert back to list of dictionaries
            transformed_orders = df.to_dict('records')
            
            self.logger.info(f"✅ Successfully transformed {len(transformed_orders)} customer orders")
            return transformed_orders
            
        except Exception as e:
            self.logger.error(f"❌ Failed to transform customer orders: {str(e)}")
            raise TransformationError(f"Customer orders transformation failed: {str(e)}")
    
    def transform_product_catalog(self, products_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Transform and clean product catalog data.
        
        Args:
            products_data: Raw product catalog data
            
        Returns:
            Transformed and cleaned product catalog data
        """
        try:
            self.logger.info("🔄 Transforming product catalog data...")
            
            # Convert to DataFrame
            df = pd.DataFrame(products_data)
            
            # Data cleaning
            df = self._clean_product_catalog(df)
            
            # Data enrichment
            df = self._enrich_product_catalog(df)
            
            # Data validation
            quality_metrics = self._validate_data_quality(df, 'product_catalog')
            self.logger.info(f"📊 Data quality score: {quality_metrics.quality_score:.2f}")
            
            # Convert back to list of dictionaries
            transformed_products = df.to_dict('records')
            
            self.logger.info(f"✅ Successfully transformed {len(transformed_products)} products")
            return transformed_products
            
        except Exception as e:
            self.logger.error(f"❌ Failed to transform product catalog: {str(e)}")
            raise TransformationError(f"Product catalog transformation failed: {str(e)}")
    
    def transform_web_analytics(self, analytics_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform and clean web analytics data.
        
        Args:
            analytics_data: Raw web analytics data
            
        Returns:
            Transformed and cleaned web analytics data
        """
        try:
            self.logger.info("🔄 Transforming web analytics data...")
            
            transformed_analytics = {}
            
            # Transform each analytics metric
            for metric_name, metric_data in analytics_data.items():
                if isinstance(metric_data, list):
                    # Convert to DataFrame for transformation
                    df = pd.DataFrame(metric_data)
                    
                    # Clean and enrich
                    df = self._clean_analytics_data(df, metric_name)
                    df = self._enrich_analytics_data(df, metric_name)
                    
                    # Convert back to list
                    transformed_analytics[metric_name] = df.to_dict('records')
                else:
                    transformed_analytics[metric_name] = metric_data
            
            self.logger.info("✅ Successfully transformed web analytics data")
            return transformed_analytics
            
        except Exception as e:
            self.logger.error(f"❌ Failed to transform web analytics: {str(e)}")
            raise TransformationError(f"Web analytics transformation failed: {str(e)}")
    
    def transform_inventory_data(self, inventory_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Transform and clean inventory data.
        
        Args:
            inventory_data: Raw inventory data
            
        Returns:
            Transformed and cleaned inventory data
        """
        try:
            self.logger.info("🔄 Transforming inventory data...")
            
            # Convert to DataFrame
            df = pd.DataFrame(inventory_data)
            
            # Data cleaning
            df = self._clean_inventory_data(df)
            
            # Data enrichment
            df = self._enrich_inventory_data(df)
            
            # Data validation
            quality_metrics = self._validate_data_quality(df, 'inventory')
            self.logger.info(f"📊 Data quality score: {quality_metrics.quality_score:.2f}")
            
            # Convert back to list of dictionaries
            transformed_inventory = df.to_dict('records')
            
            self.logger.info(f"✅ Successfully transformed {len(transformed_inventory)} inventory records")
            return transformed_inventory
            
        except Exception as e:
            self.logger.error(f"❌ Failed to transform inventory data: {str(e)}")
            raise TransformationError(f"Inventory transformation failed: {str(e)}")
    
    def create_business_metrics(self, orders: List[Dict[str, Any]], 
                               products: List[Dict[str, Any]], 
                               inventory: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create business metrics and aggregations from transformed data.
        
        Args:
            orders: Transformed customer orders
            products: Transformed product catalog
            inventory: Transformed inventory data
            
        Returns:
            Dictionary containing business metrics and aggregations
        """
        try:
            self.logger.info("📊 Creating business metrics and aggregations...")
            
            # Convert to DataFrames
            orders_df = pd.DataFrame(orders)
            products_df = pd.DataFrame(products)
            inventory_df = pd.DataFrame(inventory)
            
            # Revenue metrics
            revenue_metrics = self._calculate_revenue_metrics(orders_df, products_df)
            
            # Customer metrics
            customer_metrics = self._calculate_customer_metrics(orders_df)
            
            # Product metrics
            product_metrics = self._calculate_product_metrics(orders_df, products_df, inventory_df)
            
            # Inventory metrics
            inventory_metrics = self._calculate_inventory_metrics(inventory_df)
            
            # Time-based aggregations
            time_metrics = self._calculate_time_metrics(orders_df)
            
            business_metrics = {
                'revenue': revenue_metrics,
                'customers': customer_metrics,
                'products': product_metrics,
                'inventory': inventory_metrics,
                'time_series': time_metrics,
                'generated_at': datetime.now().isoformat()
            }
            
            self.logger.info("✅ Successfully created business metrics")
            return business_metrics
            
        except Exception as e:
            self.logger.error(f"❌ Failed to create business metrics: {str(e)}")
            raise TransformationError(f"Business metrics creation failed: {str(e)}")
    
    def _clean_customer_orders(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean customer orders data."""
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Handle missing values
        df['customer_id'] = df['customer_id'].fillna('UNKNOWN')
        df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
        df = df.dropna(subset=['order_date'])
        
        # Clean monetary values
        df['total_amount'] = pd.to_numeric(df['total_amount'], errors='coerce')
        df = df.dropna(subset=['total_amount'])
        
        # Remove invalid amounts
        df = df[df['total_amount'] > 0]
        
        # Add order ID if missing
        if 'order_id' not in df.columns:
            df['order_id'] = range(1, len(df) + 1)
        
        return df
    
    def _enrich_customer_orders(self, df: pd.DataFrame) -> pd.DataFrame:
        """Enrich customer orders data with calculated fields."""
        # Extract date components
        df['order_year'] = df['order_date'].dt.year
        df['order_month'] = df['order_date'].dt.month
        df['order_day'] = df['order_date'].dt.day
        df['order_weekday'] = df['order_date'].dt.day_name()
        
        # Add order value categories
        df['order_value_category'] = pd.cut(
            df['total_amount'],
            bins=[0, 50, 100, 200, 500, float('inf')],
            labels=['Low', 'Medium', 'High', 'Premium', 'Luxury']
        )
        
        # Add customer segment based on order frequency
        customer_order_counts = df.groupby('customer_id').size()
        df['customer_segment'] = df['customer_id'].map(
            lambda x: 'High Value' if customer_order_counts.get(x, 0) > 5 else 'Regular'
        )
        
        return df
    
    def _clean_product_catalog(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean product catalog data."""
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Handle missing values
        df['name'] = df['name'].fillna('Unknown Product')
        df['category'] = df['category'].fillna('Uncategorized')
        
        # Clean price data
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df = df.dropna(subset=['price'])
        df = df[df['price'] >= 0]
        
        # Standardize category names
        df['category'] = df['category'].str.title()
        
        return df
    
    def _enrich_product_catalog(self, df: pd.DataFrame) -> pd.DataFrame:
        """Enrich product catalog data with calculated fields."""
        # Add price categories
        df['price_category'] = pd.cut(
            df['price'],
            bins=[0, 25, 50, 100, 200, float('inf')],
            labels=['Budget', 'Economy', 'Mid-Range', 'Premium', 'Luxury']
        )
        
        # Add product age (if created_date exists)
        if 'created_date' in df.columns:
            df['created_date'] = pd.to_datetime(df['created_date'], errors='coerce')
            df['product_age_days'] = (datetime.now() - df['created_date']).dt.days
        
        return df
    
    def _clean_analytics_data(self, df: pd.DataFrame, metric_name: str) -> pd.DataFrame:
        """Clean analytics data based on metric type."""
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Handle missing values
        df = df.fillna(0)
        
        # Clean numeric fields
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        return df
    
    def _enrich_analytics_data(self, df: pd.DataFrame, metric_name: str) -> pd.DataFrame:
        """Enrich analytics data with calculated fields."""
        # Add date components if date column exists
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            df['day_of_week'] = df['date'].dt.day_name()
            df['is_weekend'] = df['date'].dt.dayofweek.isin([5, 6])
        
        # Add rolling averages for time series data
        if 'date' in df.columns and len(df) > 7:
            df = df.sort_values('date')
            numeric_columns = df.select_dtypes(include=[np.number]).columns
            for col in numeric_columns:
                if col != 'date':
                    df[f'{col}_7d_avg'] = df[col].rolling(window=7, min_periods=1).mean()
        
        return df
    
    def _clean_inventory_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean inventory data."""
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Handle missing values
        df['quantity'] = df['quantity'].fillna(0)
        df['last_updated'] = pd.to_datetime(df['last_updated'], errors='coerce')
        
        # Clean quantity data
        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
        df = df.dropna(subset=['quantity'])
        df = df[df['quantity'] >= 0]
        
        return df
    
    def _enrich_inventory_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Enrich inventory data with calculated fields."""
        # Add inventory status
        df['inventory_status'] = pd.cut(
            df['quantity'],
            bins=[0, 10, 50, 100, float('inf')],
            labels=['Out of Stock', 'Low Stock', 'Medium Stock', 'Well Stocked']
        )
        
        # Add days since last update
        df['days_since_update'] = (datetime.now() - df['last_updated']).dt.days
        
        return df
    
    def _calculate_revenue_metrics(self, orders_df: pd.DataFrame, 
                                 products_df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate revenue-related metrics."""
        # Total revenue
        total_revenue = orders_df['total_amount'].sum()
        
        # Average order value
        avg_order_value = orders_df['total_amount'].mean()
        
        # Revenue by category
        if 'product_id' in orders_df.columns and 'category' in products_df.columns:
            # Merge orders with products to get category information
            merged = orders_df.merge(products_df[['product_id', 'category']], 
                                   on='product_id', how='left')
            revenue_by_category = merged.groupby('category')['total_amount'].sum().to_dict()
        else:
            revenue_by_category = {}
        
        # Revenue by customer segment
        revenue_by_segment = orders_df.groupby('customer_segment')['total_amount'].sum().to_dict()
        
        return {
            'total_revenue': total_revenue,
            'avg_order_value': avg_order_value,
            'revenue_by_category': revenue_by_category,
            'revenue_by_segment': revenue_by_segment
        }
    
    def _calculate_customer_metrics(self, orders_df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate customer-related metrics."""
        # Total customers
        total_customers = orders_df['customer_id'].nunique()
        
        # Customer order frequency
        customer_frequency = orders_df.groupby('customer_id').size()
        avg_orders_per_customer = customer_frequency.mean()
        
        # Customer segments distribution
        segment_distribution = orders_df['customer_segment'].value_counts().to_dict()
        
        # Customer lifetime value (total spent per customer)
        customer_lifetime_value = orders_df.groupby('customer_id')['total_amount'].sum()
        avg_lifetime_value = customer_lifetime_value.mean()
        
        return {
            'total_customers': total_customers,
            'avg_orders_per_customer': avg_orders_per_customer,
            'segment_distribution': segment_distribution,
            'avg_lifetime_value': avg_lifetime_value
        }
    
    def _calculate_product_metrics(self, orders_df: pd.DataFrame, 
                                 products_df: pd.DataFrame, 
                                 inventory_df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate product-related metrics."""
        # Product performance (if product_id exists in orders)
        if 'product_id' in orders_df.columns:
            product_sales = orders_df.groupby('product_id')['total_amount'].sum()
            top_products = product_sales.nlargest(10).to_dict()
        else:
            top_products = {}
        
        # Category distribution
        category_distribution = products_df['category'].value_counts().to_dict()
        
        # Price distribution
        price_stats = {
            'min_price': products_df['price'].min(),
            'max_price': products_df['price'].max(),
            'avg_price': products_df['price'].mean(),
            'median_price': products_df['price'].median()
        }
        
        return {
            'top_products': top_products,
            'category_distribution': category_distribution,
            'price_statistics': price_stats
        }
    
    def _calculate_inventory_metrics(self, inventory_df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate inventory-related metrics."""
        # Total inventory value
        total_quantity = inventory_df['quantity'].sum()
        
        # Stock levels by status
        stock_by_status = inventory_df['inventory_status'].value_counts().to_dict()
        
        # Low stock alerts
        low_stock_items = inventory_df[inventory_df['inventory_status'] == 'Low Stock'].shape[0]
        
        # Out of stock items
        out_of_stock_items = inventory_df[inventory_df['inventory_status'] == 'Out of Stock'].shape[0]
        
        return {
            'total_quantity': total_quantity,
            'stock_by_status': stock_by_status,
            'low_stock_alerts': low_stock_items,
            'out_of_stock_items': out_of_stock_items
        }
    
    def _calculate_time_metrics(self, orders_df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate time-based metrics."""
        # Daily revenue
        daily_revenue = orders_df.groupby('order_date')['total_amount'].sum()
        
        # Monthly revenue
        monthly_revenue = orders_df.groupby([orders_df['order_date'].dt.year, 
                                          orders_df['order_date'].dt.month])['total_amount'].sum()
        
        # Revenue by day of week
        revenue_by_weekday = orders_df.groupby('order_weekday')['total_amount'].sum().to_dict()
        
        return {
            'daily_revenue': daily_revenue.to_dict(),
            'monthly_revenue': monthly_revenue.to_dict(),
            'revenue_by_weekday': revenue_by_weekday
        }
    
    def _validate_data_quality(self, df: pd.DataFrame, data_type: str) -> DataQualityMetrics:
        """Validate data quality and return metrics."""
        total_records = len(df)
        
        # Check for missing values
        missing_values = df.isnull().sum().to_dict()
        total_missing = sum(missing_values.values())
        
        # Check for duplicates
        duplicate_records = df.duplicated().sum()
        
        # Check data types
        data_type_errors = 0
        for column in df.columns:
            try:
                # Basic type validation
                if df[column].dtype == 'object':
                    # Check if numeric columns are actually numeric
                    if column in ['price', 'quantity', 'total_amount']:
                        pd.to_numeric(df[column], errors='raise')
            except:
                data_type_errors += 1
        
        # Calculate quality score
        valid_records = total_records - total_missing - duplicate_records
        quality_score = valid_records / total_records if total_records > 0 else 0
        
        return DataQualityMetrics(
            total_records=total_records,
            valid_records=valid_records,
            invalid_records=total_records - valid_records,
            quality_score=quality_score,
            missing_values=missing_values,
            duplicate_records=duplicate_records,
            data_type_errors=data_type_errors
        )
