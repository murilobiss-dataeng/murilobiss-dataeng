#!/usr/bin/env python3
"""
📤 Data Loader Module

This module handles data loading to various destinations in the e-commerce analytics pipeline.
It supports loading to BigQuery, Cloud Storage, and other GCP services with proper
error handling and validation.

Author: Data Engineering Team
Version: 1.0.0
"""

import logging
import json
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from pathlib import Path

from google.cloud import bigquery, storage
from google.cloud.exceptions import GoogleCloudError
from google.api_core import retry

from utils.config import Config
from utils.exceptions import LoadingError


class DataLoader:
    """
    Data loading class for e-commerce analytics pipeline.
    
    Supports loading data to:
    - BigQuery (tables, views, materialized views)
    - Cloud Storage (parquet, avro, json)
    - Cloud SQL (if needed)
    """

    def __init__(self, config: Config):
        """
        Initialize the data loader.
        
        Args:
            config: Configuration object with GCP settings
        """
        self.config = config
        self.logger = logging.getLogger(__name__)

        # Initialize GCP clients
        self.bigquery_client = bigquery.Client()
        self.storage_client = storage.Client()

        # Extract configuration
        self.bigquery_config = config.get('bigquery', {})
        self.storage_config = config.get('storage_config', {})
        self.loading_config = config.get('loading', {})

        # Get dataset and table configurations
        self.dataset_id = self.bigquery_config.get('dataset_id', 'ecommerce_analytics')
        self.project_id = self.bigquery_config.get('project_id')
        
        if not self.project_id:
            self.project_id = self.bigquery_client.project

        self.logger.info("📤 Data Loader initialized successfully")

    def load_to_bigquery(
        self, 
        data: Union[pd.DataFrame, List[Dict[str, Any]]], 
        table_name: str,
        write_disposition: str = 'WRITE_TRUNCATE',
        schema: Optional[List[bigquery.SchemaField]] = None
    ) -> bool:
        """
        Load data to BigQuery table.
        
        Args:
            data: Data to load (DataFrame or list of dictionaries)
            table_name: Name of the target table
            write_disposition: How to handle existing data
            schema: Optional schema definition
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Convert list of dicts to DataFrame if needed
            if isinstance(data, list):
                df = pd.DataFrame(data)
            else:
                df = data.copy()

            # Prepare table reference
            table_id = f"{self.project_id}.{self.dataset_id}.{table_name}"
            table_ref = bigquery.TableReference.from_string(table_id)

            # Create dataset if it doesn't exist
            self._ensure_dataset_exists()

            # Load data to BigQuery
            job_config = bigquery.LoadJobConfig(
                write_disposition=write_disposition,
                schema=schema,
                autodetect=True if schema is None else False
            )

            # Convert DataFrame to BigQuery format
            if isinstance(df, pd.DataFrame):
                job = self.bigquery_client.load_table_from_dataframe(
                    df, table_ref, job_config=job_config
                )
            else:
                # Handle list of dictionaries
                job = self.bigquery_client.load_table_from_json(
                    data, table_ref, job_config=job_config
                )

            # Wait for job completion
            job.result()
            
            # Get table info
            table = self.bigquery_client.get_table(table_ref)
            
            self.logger.info(
                f"✅ Successfully loaded {len(df) if isinstance(df, pd.DataFrame) else len(data)} "
                f"records to {table_id}"
            )
            
            return True

        except Exception as e:
            self.logger.error(f"❌ Error loading data to BigQuery: {str(e)}")
            raise LoadingError(f"Failed to load data to BigQuery: {str(e)}")

    def load_to_cloud_storage(
        self,
        data: Union[pd.DataFrame, List[Dict[str, Any]]],
        bucket_name: str,
        blob_path: str,
        format: str = 'parquet',
        compression: Optional[str] = None
    ) -> bool:
        """
        Load data to Cloud Storage in various formats.
        
        Args:
            data: Data to load
            bucket_name: Target bucket name
            blob_path: Path within the bucket
            format: Output format (parquet, csv, json, avro)
            compression: Compression type (gzip, snappy, etc.)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Convert list of dicts to DataFrame if needed
            if isinstance(data, list):
                df = pd.DataFrame(data)
            else:
                df = data.copy()

            # Get bucket
            bucket = self.storage_client.bucket(bucket_name)
            blob = bucket.blob(blob_path)

            # Convert DataFrame to bytes based on format
            if format.lower() == 'parquet':
                buffer = df.to_parquet(compression=compression)
            elif format.lower() == 'csv':
                buffer = df.to_csv(index=False, compression=compression).encode('utf-8')
            elif format.lower() == 'json':
                buffer = df.to_json(orient='records', date_format='iso').encode('utf-8')
            elif format.lower() == 'avro':
                buffer = df.to_parquet(compression=compression)  # Using parquet as fallback
            else:
                raise ValueError(f"Unsupported format: {format}")

            # Upload to Cloud Storage
            blob.upload_from_string(buffer, content_type=self._get_content_type(format))
            
            self.logger.info(
                f"✅ Successfully uploaded {len(df)} records to "
                f"gs://{bucket_name}/{blob_path} in {format} format"
            )
            
            return True

        except Exception as e:
            self.logger.error(f"❌ Error loading data to Cloud Storage: {str(e)}")
            raise LoadingError(f"Failed to load data to Cloud Storage: {str(e)}")

    def create_bigquery_view(
        self,
        view_name: str,
        query: str,
        description: Optional[str] = None
    ) -> bool:
        """
        Create a BigQuery view.
        
        Args:
            view_name: Name of the view
            query: SQL query for the view
            description: Optional description
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            view_id = f"{self.project_id}.{self.dataset_id}.{view_name}"
            
            # Create view configuration
            view = bigquery.Table(view_id)
            view.view_query = query
            view.description = description or f"View for {view_name}"
            
            # Create the view
            self.bigquery_client.create_table(view, exists_ok=True)
            
            self.logger.info(f"✅ Successfully created BigQuery view: {view_id}")
            return True

        except Exception as e:
            self.logger.error(f"❌ Error creating BigQuery view: {str(e)}")
            raise LoadingError(f"Failed to create BigQuery view: {str(e)}")

    def create_materialized_view(
        self,
        view_name: str,
        query: str,
        description: Optional[str] = None,
        refresh_interval_ms: int = 1800000  # 30 minutes default
    ) -> bool:
        """
        Create a BigQuery materialized view.
        
        Args:
            view_name: Name of the materialized view
            query: SQL query for the view
            description: Optional description
            refresh_interval_ms: Refresh interval in milliseconds
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            view_id = f"{self.project_id}.{self.dataset_id}.{view_name}"
            
            # Create materialized view configuration
            view = bigquery.Table(view_id)
            view.materialized_view = bigquery.MaterializedViewDefinition(
                query=query,
                refresh_interval_ms=refresh_interval_ms
            )
            view.description = description or f"Materialized view for {view_name}"
            
            # Create the materialized view
            self.bigquery_client.create_table(view, exists_ok=True)
            
            self.logger.info(f"✅ Successfully created materialized view: {view_id}")
            return True

        except Exception as e:
            self.logger.error(f"❌ Error creating materialized view: {str(e)}")
            raise LoadingError(f"Failed to create materialized view: {str(e)}")

    def load_ecommerce_analytics(self, transformed_data: Dict[str, Any]) -> Dict[str, bool]:
        """
        Load all e-commerce analytics data to their respective destinations.
        
        Args:
            transformed_data: Dictionary containing all transformed data
            
        Returns:
            Dict[str, bool]: Status of each loading operation
        """
        results = {}
        
        try:
            # Load customer analytics
            if 'customer_analytics' in transformed_data:
                results['customer_analytics'] = self.load_to_bigquery(
                    transformed_data['customer_analytics'],
                    'customer_analytics',
                    write_disposition='WRITE_TRUNCATE'
                )

            # Load product analytics
            if 'product_analytics' in transformed_data:
                results['product_analytics'] = self.load_to_bigquery(
                    transformed_data['product_analytics'],
                    'product_analytics',
                    write_disposition='WRITE_TRUNCATE'
                )

            # Load revenue analytics
            if 'revenue_analytics' in transformed_data:
                results['revenue_analytics'] = self.load_to_bigquery(
                    transformed_data['revenue_analytics'],
                    'revenue_analytics',
                    write_disposition='WRITE_TRUNCATE'
                )

            # Load web analytics
            if 'web_analytics' in transformed_data:
                results['web_analytics'] = self.load_to_bigquery(
                    transformed_data['web_analytics'],
                    'web_analytics',
                    write_disposition='WRITE_TRUNCATE'
                )

            # Load business metrics
            if 'business_metrics' in transformed_data:
                results['business_metrics'] = self.load_to_bigquery(
                    transformed_data['business_metrics'],
                    'business_metrics',
                    write_disposition='WRITE_TRUNCATE'
                )

            # Also save to Cloud Storage as backup
            for key, data in transformed_data.items():
                if key in results and results[key]:
                    backup_path = f"processed/{key}/{datetime.now().strftime('%Y%m%d_%H%M%S')}.parquet"
                    results[f"{key}_backup"] = self.load_to_cloud_storage(
                        data, 
                        self.storage_config.get('processed_bucket', 'ecommerce-processed'),
                        backup_path,
                        format='parquet'
                    )

            self.logger.info("✅ All e-commerce analytics data loaded successfully")
            return results

        except Exception as e:
            self.logger.error(f"❌ Error in bulk loading: {str(e)}")
            raise LoadingError(f"Failed to load e-commerce analytics data: {str(e)}")

    def _ensure_dataset_exists(self) -> None:
        """Ensure the BigQuery dataset exists."""
        try:
            dataset_ref = bigquery.DatasetReference(self.project_id, self.dataset_id)
            dataset = bigquery.Dataset(dataset_ref)
            
            # Create dataset if it doesn't exist
            self.bigquery_client.create_dataset(dataset, exists_ok=True)
            
        except Exception as e:
            self.logger.error(f"❌ Error ensuring dataset exists: {str(e)}")
            raise LoadingError(f"Failed to ensure dataset exists: {str(e)}")

    def _get_content_type(self, format: str) -> str:
        """Get the appropriate content type for the format."""
        content_types = {
            'parquet': 'application/octet-stream',
            'csv': 'text/csv',
            'json': 'application/json',
            'avro': 'application/octet-stream'
        }
        return content_types.get(format.lower(), 'application/octet-stream')

    def cleanup_old_data(self, days_to_keep: int = 30) -> bool:
        """
        Clean up old data files from Cloud Storage.
        
        Args:
            days_to_keep: Number of days to keep data
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            
            for bucket_name in self.storage_config.get('buckets', []):
                bucket = self.storage_client.bucket(bucket_name)
                
                for blob in bucket.list_blobs():
                    if blob.time_created < cutoff_date:
                        blob.delete()
                        self.logger.info(f"🗑️ Deleted old file: {blob.name}")
            
            return True

        except Exception as e:
            self.logger.error(f"❌ Error cleaning up old data: {str(e)}")
            return False
