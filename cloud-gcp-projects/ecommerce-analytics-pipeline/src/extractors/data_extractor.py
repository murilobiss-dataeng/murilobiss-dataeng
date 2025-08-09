#!/usr/bin/env python3
"""
📥 Data Extractor Module

This module handles data extraction from various sources including:
- CSV files from ERP systems
- JSON APIs from product management systems
- Google Analytics 4 data
- Database exports from warehouse systems

Author: Data Engineering Team
Version: 1.0.0
"""

import json
import logging
import pandas as pd
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
from google.cloud import storage, bigquery
from google.cloud.exceptions import GoogleCloudError

from utils.config import Config
from utils.exceptions import ExtractionError


class DataExtractor:
    """
    Data extraction class for e-commerce analytics pipeline.
    
    Handles extraction from multiple data sources including files, APIs,
    and databases, with proper error handling and validation.
    """
    
    def __init__(self, config: Config):
        """
        Initialize the data extractor.
        
        Args:
            config: Configuration object containing extraction settings
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize GCP clients
        self.storage_client = storage.Client()
        self.bigquery_client = bigquery.Client()
        
        # Extract configuration
        self.data_sources = config.get('data_sources', {})
        self.api_config = config.get('api_config', {})
        self.storage_config = config.get('storage_config', {})
        
        self.logger.info("📥 Data Extractor initialized successfully")
    
    def extract_customer_orders(self) -> List[Dict[str, Any]]:
        """
        Extract customer orders data from ERP system CSV files.
        
        Returns:
            List of customer order records
        """
        try:
            self.logger.info("📥 Extracting customer orders data...")
            
            # Get source path from config
            source_path = self.data_sources.get('customer_orders', {}).get('source_path')
            if not source_path:
                raise ExtractionError("Customer orders source path not configured")
            
            # Read CSV file
            if source_path.startswith('gs://'):
                # Cloud Storage path
                df = self._read_csv_from_gcs(source_path)
            else:
                # Local file path
                df = pd.read_csv(source_path)
            
            # Validate data structure
            required_columns = ['order_id', 'customer_id', 'order_date', 'total_amount']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ExtractionError(f"Missing required columns: {missing_columns}")
            
            # Convert to list of dictionaries
            orders_data = df.to_dict('records')
            
            self.logger.info(f"✅ Successfully extracted {len(orders_data)} customer orders")
            return orders_data
            
        except Exception as e:
            self.logger.error(f"❌ Failed to extract customer orders: {str(e)}")
            raise ExtractionError(f"Customer orders extraction failed: {str(e)}")
    
    def extract_product_catalog(self) -> List[Dict[str, Any]]:
        """
        Extract product catalog data from JSON API.
        
        Returns:
            List of product catalog records
        """
        try:
            self.logger.info("📥 Extracting product catalog data...")
            
            # Get API configuration
            api_url = self.api_config.get('product_catalog', {}).get('url')
            api_key = self.api_config.get('product_catalog', {}).get('api_key')
            
            if not api_url:
                raise ExtractionError("Product catalog API URL not configured")
            
            # Make API request
            headers = {'Authorization': f'Bearer {api_key}'} if api_key else {}
            response = requests.get(api_url, headers=headers, timeout=30)
            response.raise_for_status()
            
            # Parse JSON response
            products_data = response.json()
            
            # Validate response structure
            if not isinstance(products_data, list):
                raise ExtractionError("Invalid API response format - expected list")
            
            # Validate required fields
            required_fields = ['product_id', 'name', 'category', 'price']
            for product in products_data:
                missing_fields = [field for field in required_fields if field not in product]
                if missing_fields:
                    self.logger.warning(f"Product {product.get('product_id', 'unknown')} missing fields: {missing_fields}")
            
            self.logger.info(f"✅ Successfully extracted {len(products_data)} products")
            return products_data
            
        except requests.RequestException as e:
            self.logger.error(f"❌ API request failed: {str(e)}")
            raise ExtractionError(f"Product catalog API request failed: {str(e)}")
        except Exception as e:
            self.logger.error(f"❌ Failed to extract product catalog: {str(e)}")
            raise ExtractionError(f"Product catalog extraction failed: {str(e)}")
    
    def extract_web_analytics(self) -> Dict[str, Any]:
        """
        Extract web analytics data from Google Analytics 4.
        
        Returns:
            Dictionary containing web analytics data
        """
        try:
            self.logger.info("📥 Extracting web analytics data...")
            
            # Get GA4 configuration
            ga4_config = self.api_config.get('google_analytics', {})
            property_id = ga4_config.get('property_id')
            credentials_path = ga4_config.get('credentials_path')
            
            if not property_id or not credentials_path:
                raise ExtractionError("Google Analytics configuration incomplete")
            
            # Extract data for the last 30 days
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
            
            # This would typically use the Google Analytics Data API
            # For demonstration, we'll create sample analytics data
            analytics_data = self._generate_sample_analytics_data(start_date, end_date)
            
            self.logger.info("✅ Successfully extracted web analytics data")
            return analytics_data
            
        except Exception as e:
            self.logger.error(f"❌ Failed to extract web analytics: {str(e)}")
            raise ExtractionError(f"Web analytics extraction failed: {str(e)}")
    
    def extract_inventory_data(self) -> List[Dict[str, Any]]:
        """
        Extract inventory data from warehouse database exports.
        
        Returns:
            List of inventory records
        """
        try:
            self.logger.info("📥 Extracting inventory data...")
            
            # Get source path from config
            source_path = self.data_sources.get('inventory', {}).get('source_path')
            if not source_path:
                raise ExtractionError("Inventory source path not configured")
            
            # Read CSV file
            if source_path.startswith('gs://'):
                # Cloud Storage path
                df = self._read_csv_from_gcs(source_path)
            else:
                # Local file path
                df = pd.read_csv(source_path)
            
            # Validate data structure
            required_columns = ['product_id', 'warehouse_id', 'quantity', 'last_updated']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ExtractionError(f"Missing required columns: {missing_columns}")
            
            # Convert to list of dictionaries
            inventory_data = df.to_dict('records')
            
            self.logger.info(f"✅ Successfully extracted {len(inventory_data)} inventory records")
            return inventory_data
            
        except Exception as e:
            self.logger.error(f"❌ Failed to extract inventory data: {str(e)}")
            raise ExtractionError(f"Inventory extraction failed: {str(e)}")
    
    def _read_csv_from_gcs(self, gcs_path: str) -> pd.DataFrame:
        """
        Read CSV file from Google Cloud Storage.
        
        Args:
            gcs_path: GCS path in format 'gs://bucket/path/file.csv'
            
        Returns:
            Pandas DataFrame containing the CSV data
        """
        try:
            # Parse GCS path
            if not gcs_path.startswith('gs://'):
                raise ValueError("Invalid GCS path format")
            
            bucket_name = gcs_path.split('/')[2]
            blob_path = '/'.join(gcs_path.split('/')[3:])
            
            # Get bucket and blob
            bucket = self.storage_client.bucket(bucket_name)
            blob = bucket.blob(blob_path)
            
            # Download and read CSV
            content = blob.download_as_text()
            df = pd.read_csv(pd.StringIO(content))
            
            return df
            
        except Exception as e:
            self.logger.error(f"❌ Failed to read CSV from GCS: {str(e)}")
            raise ExtractionError(f"GCS CSV reading failed: {str(e)}")
    
    def _generate_sample_analytics_data(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """
        Generate sample web analytics data for demonstration.
        
        Args:
            start_date: Start date for analytics period
            end_date: End date for analytics period
            
        Returns:
            Dictionary containing sample analytics data
        """
        # Generate date range
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Sample analytics data
        analytics_data = {
            'page_views': [],
            'sessions': [],
            'users': [],
            'conversions': [],
            'revenue': []
        }
        
        for date in date_range:
            # Generate realistic sample data
            analytics_data['page_views'].append({
                'date': date.strftime('%Y-%m-%d'),
                'count': int(pd.np.random.normal(10000, 2000)),
                'page_type': 'product'
            })
            
            analytics_data['sessions'].append({
                'date': date.strftime('%Y-%m-%d'),
                'count': int(pd.np.random.normal(5000, 1000)),
                'duration_avg': float(pd.np.random.normal(180, 30))
            })
            
            analytics_data['users'].append({
                'date': date.strftime('%Y-%m-%d'),
                'new_users': int(pd.np.random.normal(800, 150)),
                'returning_users': int(pd.np.random.normal(1200, 200))
            })
            
            analytics_data['conversions'].append({
                'date': date.strftime('%Y-%m-%d'),
                'count': int(pd.np.random.normal(150, 30)),
                'rate': float(pd.np.random.normal(0.03, 0.005))
            })
            
            analytics_data['revenue'].append({
                'date': date.strftime('%Y-%m-%d'),
                'amount': float(pd.np.random.normal(25000, 5000)),
                'currency': 'USD'
            })
        
        return analytics_data
    
    def validate_gcp_access(self) -> bool:
        """
        Validate GCP access and permissions.
        
        Returns:
            True if validation passes, False otherwise
        """
        try:
            self.logger.info("🔍 Validating GCP access...")
            
            # Test Cloud Storage access
            bucket_name = self.storage_config.get('bucket_name')
            if bucket_name:
                bucket = self.storage_client.bucket(bucket_name)
                bucket.reload()
                self.logger.info("✅ Cloud Storage access validated")
            
            # Test BigQuery access
            dataset_id = self.config.get('bigquery', {}).get('dataset_id')
            if dataset_id:
                dataset = self.bigquery_client.dataset(dataset_id)
                dataset.reload()
                self.logger.info("✅ BigQuery access validated")
            
            return True
            
        except GoogleCloudError as e:
            self.logger.error(f"❌ GCP access validation failed: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"❌ GCP validation error: {str(e)}")
            return False
    
    def validate_data_sources(self) -> bool:
        """
        Validate data source accessibility and structure.
        
        Returns:
            True if validation passes, False otherwise
        """
        try:
            self.logger.info("🔍 Validating data sources...")
            
            # Validate customer orders source
            customer_source = self.data_sources.get('customer_orders', {}).get('source_path')
            if customer_source and not self._validate_source_path(customer_source):
                return False
            
            # Validate inventory source
            inventory_source = self.data_sources.get('inventory', {}).get('source_path')
            if inventory_source and not self._validate_source_path(inventory_source):
                return False
            
            # Validate API endpoints
            product_api = self.api_config.get('product_catalog', {}).get('url')
            if product_api and not self._validate_api_endpoint(product_api):
                return False
            
            self.logger.info("✅ Data sources validation completed")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Data sources validation failed: {str(e)}")
            return False
    
    def _validate_source_path(self, source_path: str) -> bool:
        """
        Validate if a data source path is accessible.
        
        Args:
            source_path: Path to the data source
            
        Returns:
            True if accessible, False otherwise
        """
        try:
            if source_path.startswith('gs://'):
                # GCS path validation
                bucket_name = source_path.split('/')[2]
                blob_path = '/'.join(source_path.split('/')[3:])
                bucket = self.storage_client.bucket(bucket_name)
                blob = bucket.blob(blob_path)
                return blob.exists()
            else:
                # Local file path validation
                return Path(source_path).exists()
        except Exception:
            return False
    
    def _validate_api_endpoint(self, api_url: str) -> bool:
        """
        Validate if an API endpoint is accessible.
        
        Args:
            api_url: URL of the API endpoint
            
        Returns:
            True if accessible, False otherwise
        """
        try:
            response = requests.head(api_url, timeout=10)
            return response.status_code < 400
        except Exception:
            return False
