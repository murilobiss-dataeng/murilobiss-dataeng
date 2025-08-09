#!/usr/bin/env python3
"""
⚙️ Configuration Module

This module manages configuration for the e-commerce analytics pipeline.
It supports multiple environments (dev, staging, prod) and provides
a centralized way to manage all pipeline settings.

Author: Data Engineering Team
Version: 1.0.0
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass, field

from .exceptions import ConfigurationError


@dataclass
class GCPConfig:
    """GCP-specific configuration."""
    project_id: str
    region: str = "us-central1"
    zone: str = "us-central1-a"
    
    # Service account settings
    service_account_key_path: Optional[str] = None
    service_account_email: Optional[str] = None
    
    # Default credentials
    use_default_credentials: bool = True


@dataclass
class BigQueryConfig:
    """BigQuery configuration."""
    dataset_id: str = "ecommerce_analytics"
    project_id: Optional[str] = None
    
    # Table configurations
    customer_analytics_table: str = "customer_analytics"
    product_analytics_table: str = "product_analytics"
    revenue_analytics_table: str = "revenue_analytics"
    web_analytics_table: str = "web_analytics"
    business_metrics_table: str = "business_metrics"
    
    # Performance settings
    max_bytes_billed: Optional[int] = None
    use_legacy_sql: bool = False


@dataclass
class StorageConfig:
    """Cloud Storage configuration."""
    raw_bucket: str = "ecommerce-raw-data"
    processed_bucket: str = "ecommerce-processed"
    curated_bucket: str = "ecommerce-curated"
    
    # Backup settings
    backup_enabled: bool = True
    backup_retention_days: int = 30
    
    # Data lifecycle
    raw_data_retention_days: int = 90
    processed_data_retention_days: int = 60


@dataclass
class DataQualityConfig:
    """Data quality configuration."""
    # Validation rules
    min_quality_score: float = 0.8
    required_fields: Dict[str, list] = field(default_factory=dict)
    
    # Data type validation
    strict_type_checking: bool = True
    
    # Business rules
    business_rules: Dict[str, Any] = field(default_factory=dict)
    
    # Alerting
    alert_on_quality_failure: bool = True
    quality_thresholds: Dict[str, float] = field(default_factory=dict)


@dataclass
class PipelineConfig:
    """Pipeline execution configuration."""
    # Execution settings
    max_retries: int = 3
    retry_delay_seconds: int = 60
    timeout_seconds: int = 3600
    
    # Parallel processing
    max_workers: int = 4
    chunk_size: int = 10000
    
    # Monitoring
    enable_monitoring: bool = True
    log_level: str = "INFO"
    
    # Notifications
    slack_webhook_url: Optional[str] = None
    email_notifications: bool = False


class Config:
    """
    Main configuration class for the e-commerce analytics pipeline.
    
    Supports loading configuration from:
    - Environment variables
    - Configuration files (YAML/JSON)
    - Default values
    """
    
    def __init__(self, environment: str = "dev", config_path: Optional[str] = None):
        """
        Initialize configuration.
        
        Args:
            environment: Environment name (dev, staging, prod)
            config_path: Path to configuration file
        """
        self.environment = environment.lower()
        self.config_path = config_path
        
        # Initialize configuration sections
        self.gcp = GCPConfig()
        self.bigquery = BigQueryConfig()
        self.storage = StorageConfig()
        self.data_quality = DataQualityConfig()
        self.pipeline = PipelineConfig()
        
        # Load configuration
        self._load_config()
        self._load_environment_variables()
        self._validate_config()
        
    def _load_config(self) -> None:
        """Load configuration from file if specified."""
        if not self.config_path:
            return
            
        config_file = Path(self.config_path)
        if not config_file.exists():
            raise ConfigurationError(f"Configuration file not found: {config_path}")
            
        try:
            if config_file.suffix.lower() == '.yaml':
                with open(config_file, 'r') as f:
                    config_data = yaml.safe_load(f)
            elif config_file.suffix.lower() == '.json':
                with open(config_file, 'r') as f:
                    config_data = json.load(f)
            else:
                raise ConfigurationError(f"Unsupported configuration file format: {config_file.suffix}")
                
            # Load environment-specific configuration
            env_config = config_data.get(self.environment, {})
            self._update_config_from_dict(env_config)
            
        except Exception as e:
            raise ConfigurationError(f"Failed to load configuration file: {str(e)}")
    
    def _load_environment_variables(self) -> None:
        """Load configuration from environment variables."""
        # GCP Configuration
        if os.getenv('GCP_PROJECT_ID'):
            self.gcp.project_id = os.getenv('GCP_PROJECT_ID')
            
        if os.getenv('GCP_REGION'):
            self.gcp.region = os.getenv('GCP_REGION')
            
        if os.getenv('GCP_ZONE'):
            self.gcp.zone = os.getenv('GCP_ZONE')
            
        if os.getenv('GCP_SERVICE_ACCOUNT_KEY_PATH'):
            self.gcp.service_account_key_path = os.getenv('GCP_SERVICE_ACCOUNT_KEY_PATH')
            
        # BigQuery Configuration
        if os.getenv('BIGQUERY_DATASET_ID'):
            self.bigquery.dataset_id = os.getenv('BIGQUERY_DATASET_ID')
            
        if os.getenv('BIGQUERY_PROJECT_ID'):
            self.bigquery.project_id = os.getenv('BIGQUERY_PROJECT_ID')
            
        # Storage Configuration
        if os.getenv('STORAGE_RAW_BUCKET'):
            self.storage.raw_bucket = os.getenv('STORAGE_RAW_BUCKET')
            
        if os.getenv('STORAGE_PROCESSED_BUCKET'):
            self.storage.processed_bucket = os.getenv('STORAGE_PROCESSED_BUCKET')
            
        if os.getenv('STORAGE_CURATED_BUCKET'):
            self.storage.curated_bucket = os.getenv('STORAGE_CURATED_BUCKET')
            
        # Pipeline Configuration
        if os.getenv('PIPELINE_LOG_LEVEL'):
            self.pipeline.log_level = os.getenv('PIPELINE_LOG_LEVEL')
            
        if os.getenv('PIPELINE_MAX_WORKERS'):
            self.pipeline.max_workers = int(os.getenv('PIPELINE_MAX_WORKERS'))
            
        if os.getenv('SLACK_WEBHOOK_URL'):
            self.pipeline.slack_webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    
    def _update_config_from_dict(self, config_dict: Dict[str, Any]) -> None:
        """Update configuration from dictionary."""
        # Update GCP config
        if 'gcp' in config_dict:
            gcp_config = config_dict['gcp']
            for key, value in gcp_config.items():
                if hasattr(self.gcp, key):
                    setattr(self.gcp, key, value)
                    
        # Update BigQuery config
        if 'bigquery' in config_dict:
            bq_config = config_dict['bigquery']
            for key, value in bq_config.items():
                if hasattr(self.bigquery, key):
                    setattr(self.bigquery, key, value)
                    
        # Update Storage config
        if 'storage' in config_dict:
            storage_config = config_dict['storage']
            for key, value in storage_config.items():
                if hasattr(self.storage, key):
                    setattr(self.storage, key, value)
                    
        # Update Data Quality config
        if 'data_quality' in config_dict:
            dq_config = config_dict['data_quality']
            for key, value in dq_config.items():
                if hasattr(self.data_quality, key):
                    setattr(self.data_quality, key, value)
                    
        # Update Pipeline config
        if 'pipeline' in config_dict:
            pipeline_config = config_dict['pipeline']
            for key, value in pipeline_config.items():
                if hasattr(self.pipeline, key):
                    setattr(self.pipeline, key, value)
    
    def _validate_config(self) -> None:
        """Validate configuration values."""
        # Validate GCP configuration
        if not self.gcp.project_id:
            raise ConfigurationError("GCP project ID is required")
            
        # Validate BigQuery configuration
        if not self.bigquery.project_id:
            self.bigquery.project_id = self.gcp.project_id
            
        # Validate Storage configuration
        if not self.storage.raw_bucket:
            raise ConfigurationError("Raw data bucket is required")
            
        if not self.storage.processed_bucket:
            raise ConfigurationError("Processed data bucket is required")
            
        if not self.storage.curated_bucket:
            raise ConfigurationError("Curated data bucket is required")
            
        # Validate Data Quality configuration
        if self.data_quality.min_quality_score < 0 or self.data_quality.min_quality_score > 1:
            raise ConfigurationError("Data quality score must be between 0 and 1")
            
        # Validate Pipeline configuration
        if self.pipeline.max_workers < 1:
            raise ConfigurationError("Max workers must be at least 1")
            
        if self.pipeline.chunk_size < 1:
            raise ConfigurationError("Chunk size must be at least 1")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key.
        
        Args:
            key: Configuration key (supports dot notation)
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        try:
            keys = key.split('.')
            value = self
            
            for k in keys:
                if hasattr(value, k):
                    value = getattr(value, k)
                elif isinstance(value, dict):
                    value = value.get(k, default)
                else:
                    return default
                    
            return value if value is not None else default
            
        except Exception:
            return default
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            'environment': self.environment,
            'gcp': {
                'project_id': self.gcp.project_id,
                'region': self.gcp.region,
                'zone': self.gcp.zone,
                'service_account_key_path': self.gcp.service_account_key_path,
                'service_account_email': self.gcp.service_account_email,
                'use_default_credentials': self.gcp.use_default_credentials
            },
            'bigquery': {
                'dataset_id': self.bigquery.dataset_id,
                'project_id': self.bigquery.project_id,
                'customer_analytics_table': self.bigquery.customer_analytics_table,
                'product_analytics_table': self.bigquery.product_analytics_table,
                'revenue_analytics_table': self.bigquery.revenue_analytics_table,
                'web_analytics_table': self.bigquery.web_analytics_table,
                'business_metrics_table': self.bigquery.business_metrics_table,
                'max_bytes_billed': self.bigquery.max_bytes_billed,
                'use_legacy_sql': self.bigquery.use_legacy_sql
            },
            'storage': {
                'raw_bucket': self.storage.raw_bucket,
                'processed_bucket': self.storage.processed_bucket,
                'curated_bucket': self.storage.curated_bucket,
                'backup_enabled': self.storage.backup_enabled,
                'backup_retention_days': self.storage.backup_retention_days,
                'raw_data_retention_days': self.storage.raw_data_retention_days,
                'processed_data_retention_days': self.storage.processed_data_retention_days
            },
            'data_quality': {
                'min_quality_score': self.data_quality.min_quality_score,
                'required_fields': self.data_quality.required_fields,
                'strict_type_checking': self.data_quality.strict_type_checking,
                'business_rules': self.data_quality.business_rules,
                'alert_on_quality_failure': self.data_quality.alert_on_quality_failure,
                'quality_thresholds': self.data_quality.quality_thresholds
            },
            'pipeline': {
                'max_retries': self.pipeline.max_retries,
                'retry_delay_seconds': self.pipeline.retry_delay_seconds,
                'timeout_seconds': self.pipeline.timeout_seconds,
                'max_workers': self.pipeline.max_workers,
                'chunk_size': self.pipeline.chunk_size,
                'enable_monitoring': self.pipeline.enable_monitoring,
                'log_level': self.pipeline.log_level,
                'slack_webhook_url': self.pipeline.slack_webhook_url,
                'email_notifications': self.pipeline.email_notifications
            }
        }
    
    def save_config(self, file_path: str) -> None:
        """
        Save configuration to file.
        
        Args:
            file_path: Path to save configuration
        """
        try:
            config_data = {self.environment: self.to_dict()}
            
            file_path = Path(file_path)
            if file_path.suffix.lower() == '.yaml':
                with open(file_path, 'w') as f:
                    yaml.dump(config_data, f, default_flow_style=False, indent=2)
            elif file_path.suffix.lower() == '.json':
                with open(file_path, 'w') as f:
                    json.dump(config_data, f, indent=2)
            else:
                raise ConfigurationError(f"Unsupported file format: {file_path.suffix}")
                
        except Exception as e:
            raise ConfigurationError(f"Failed to save configuration: {str(e)}")
    
    def __str__(self) -> str:
        """String representation of configuration."""
        return f"Config(environment={self.environment}, project={self.gcp.project_id})"
    
    def __repr__(self) -> str:
        """Representation of configuration."""
        return self.__str__()
