"""
Configuration file for TechFlow Solutions data pipelines
Centralized configuration management for all pipelines
"""

import os
from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class DatabaseConfig:
    """Database connection configuration"""
    host: str
    port: int
    database: str
    username: str
    password: str
    
    @classmethod
    def from_env(cls) -> 'DatabaseConfig':
        return cls(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', '5432')),
            database=os.getenv('DB_NAME', 'techflow_solutions'),
            username=os.getenv('DB_USER', 'data_engineer'),
            password=os.getenv('DB_PASSWORD', 'password')
        )

@dataclass
class KafkaConfig:
    """Kafka streaming configuration"""
    bootstrap_servers: str
    topic_prefix: str
    consumer_group: str
    auto_offset_reset: str
    
    @classmethod
    def from_env(cls) -> 'KafkaConfig':
        return cls(
            bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
            topic_prefix=os.getenv('KAFKA_TOPIC_PREFIX', 'techflow_solutions'),
            consumer_group=os.getenv('KAFKA_CONSUMER_GROUP', 'data_pipelines'),
            auto_offset_reset=os.getenv('KAFKA_AUTO_OFFSET_RESET', 'latest')
        )

@dataclass
class SparkConfig:
    """Apache Spark configuration"""
    app_name: str
    master: str
    executor_memory: str
    driver_memory: str
    executor_cores: int
    
    @classmethod
    def from_env(cls) -> 'SparkConfig':
        return cls(
            app_name=os.getenv('SPARK_APP_NAME', 'TechFlowSolutionsPipelines'),
            master=os.getenv('SPARK_MASTER', 'local[*]'),
            executor_memory=os.getenv('SPARK_EXECUTOR_MEMORY', '2g'),
            driver_memory=os.getenv('SPARK_DRIVER_MEMORY', '1g'),
            executor_cores=int(os.getenv('SPARK_EXECUTOR_CORES', '2'))
        )

@dataclass
class PipelineConfig:
    """Pipeline-specific configuration"""
    batch_size: int
    processing_interval: str
    retry_attempts: int
    timeout_seconds: int
    
    @classmethod
    def from_env(cls) -> 'PipelineConfig':
        return cls(
            batch_size=int(os.getenv('PIPELINE_BATCH_SIZE', '1000')),
            processing_interval=os.getenv('PIPELINE_INTERVAL', '1h'),
            retry_attempts=int(os.getenv('PIPELINE_RETRY_ATTEMPTS', '3')),
            timeout_seconds=int(os.getenv('PIPELINE_TIMEOUT', '3600'))
        )

class Config:
    """Main configuration class"""
    
    def __init__(self):
        self.database = DatabaseConfig.from_env()
        self.kafka = KafkaConfig.from_env()
        self.spark = SparkConfig.from_env()
        self.pipeline = PipelineConfig.from_env()
        
        # Pipeline-specific configurations for TechFlow Solutions
        self.profit_pipeline = {
            'sla_hours': 24,
            'critical_threshold': 0.95,  # 95% data completeness
            'revenue_tolerance': 0.01,   # 1% revenue accuracy tolerance
        }
        
        self.growth_pipeline = {
            'sla_hours': 168,  # 1 week
            'account_completeness_threshold': 1.0,  # 100% account coverage
            'status_validation_enabled': True,
        }
        
        self.engagement_pipeline = {
            'sla_hours': 48,
            'data_freshness_threshold': 48,  # hours
            'duplicate_detection_enabled': True,
            'kafka_lag_threshold': 300,  # 5 minutes in seconds
        }
        
        self.aggregated_pipeline = {
            'sla_hours': 720,  # 1 month
            'join_timeout_seconds': 1800,  # 30 minutes
            'memory_safety_factor': 1.5,  # 50% memory buffer
        }
    
    def get_pipeline_config(self, pipeline_name: str) -> Dict[str, Any]:
        """Get configuration for specific pipeline"""
        pipeline_configs = {
            'profit': self.profit_pipeline,
            'growth': self.growth_pipeline,
            'engagement': self.engagement_pipeline,
            'aggregated': self.aggregated_pipeline,
        }
        return pipeline_configs.get(pipeline_name, {})
    
    def validate_config(self) -> bool:
        """Validate configuration values"""
        try:
            assert self.database.host, "Database host is required"
            assert self.database.port > 0, "Database port must be positive"
            assert self.kafka.bootstrap_servers, "Kafka bootstrap servers are required"
            assert self.spark.executor_memory, "Spark executor memory is required"
            return True
        except AssertionError as e:
            print(f"Configuration validation failed: {e}")
            return False

# Global configuration instance
config = Config()
