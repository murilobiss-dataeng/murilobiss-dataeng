#!/usr/bin/env python3
"""
📝 Logging Module

This module provides structured logging for the e-commerce analytics pipeline.
It supports multiple log levels, structured logging, and integration with
Google Cloud Logging for production environments.

Author: Data Engineering Team
Version: 1.0.0
"""

import logging
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Union
from google.cloud import logging as cloud_logging

from .config import Config


class StructuredFormatter(logging.Formatter):
    """
    Custom formatter that outputs structured JSON logs.
    
    This formatter creates logs that are easily parseable by log aggregation
    systems and provide structured information for debugging and monitoring.
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as structured JSON."""
        log_entry = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # Add extra fields if they exist
        if hasattr(record, 'extra_fields'):
            log_entry.update(record.extra_fields)
            
        # Add exception info if present
        if record.exc_info:
            log_entry['exception'] = {
                'type': record.exc_info[0].__name__,
                'message': str(record.exc_info[1]),
                'traceback': self.formatException(record.exc_info)
            }
            
        # Add pipeline context if available
        if hasattr(record, 'pipeline_context'):
            log_entry['pipeline_context'] = record.pipeline_context
            
        return json.dumps(log_entry, ensure_ascii=False)


class PipelineLogger:
    """
    Enhanced logger for the e-commerce analytics pipeline.
    
    Provides structured logging with pipeline-specific context and
    integration with Google Cloud Logging.
    """
    
    def __init__(self, name: str, config: Config):
        """
        Initialize the pipeline logger.
        
        Args:
            name: Logger name
            config: Configuration object
        """
        self.name = name
        self.config = config
        self.logger = logging.getLogger(name)
        
        # Set log level
        log_level = getattr(logging, config.pipeline.log_level.upper(), logging.INFO)
        self.logger.setLevel(log_level)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Setup handlers
        self._setup_handlers()
        
        # Initialize Cloud Logging if enabled
        self._setup_cloud_logging()
        
    def _setup_handlers(self) -> None:
        """Setup logging handlers."""
        # Console handler with structured formatting
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        if self.config.environment == 'prod':
            # Production: JSON format
            console_formatter = StructuredFormatter()
        else:
            # Development: Human readable format
            console_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # File handler for local logging
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        file_handler = logging.FileHandler(
            log_dir / f'{self.name}_{datetime.now().strftime("%Y%m%d")}.log'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(StructuredFormatter())
        self.logger.addHandler(file_handler)
        
    def _setup_cloud_logging(self) -> None:
        """Setup Google Cloud Logging integration."""
        if not self.config.pipeline.enable_monitoring:
            return
            
        try:
            # Initialize Cloud Logging client
            cloud_logging_client = cloud_logging.Client()
            
            # Create Cloud Logging handler
            cloud_handler = cloud_logging_client.get_default_handler()
            cloud_handler.setFormatter(StructuredFormatter())
            
            # Add Cloud Logging handler
            self.logger.addHandler(cloud_handler)
            
        except Exception as e:
            # Log warning but don't fail if Cloud Logging setup fails
            self.logger.warning(f"Failed to setup Cloud Logging: {str(e)}")
            
    def _log_with_context(
        self, 
        level: int, 
        message: str, 
        extra_fields: Optional[Dict[str, Any]] = None,
        pipeline_context: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Log message with additional context.
        
        Args:
            level: Log level
            message: Log message
            extra_fields: Additional fields to include
            pipeline_context: Pipeline execution context
        """
        extra = {}
        
        if extra_fields:
            extra['extra_fields'] = extra_fields
            
        if pipeline_context:
            extra['pipeline_context'] = pipeline_context
            
        self.logger.log(level, message, extra=extra)
        
    def info(self, message: str, **kwargs) -> None:
        """Log info message with optional context."""
        self._log_with_context(logging.INFO, message, **kwargs)
        
    def warning(self, message: str, **kwargs) -> None:
        """Log warning message with optional context."""
        self._log_with_context(logging.WARNING, message, **kwargs)
        
    def error(self, message: str, **kwargs) -> None:
        """Log error message with optional context."""
        self._log_with_context(logging.ERROR, message, **kwargs)
        
    def critical(self, message: str, **kwargs) -> None:
        """Log critical message with optional context."""
        self._log_with_context(logging.CRITICAL, message, **kwargs)
        
    def debug(self, message: str, **kwargs) -> None:
        """Log debug message with optional context."""
        self._log_with_context(logging.DEBUG, message, **kwargs)
        
    def exception(self, message: str, **kwargs) -> None:
        """Log exception message with traceback."""
        extra_fields = kwargs.get('extra_fields', {})
        pipeline_context = kwargs.get('pipeline_context', {})
        
        self._log_with_context(
            logging.ERROR, 
            message, 
            extra_fields=extra_fields,
            pipeline_context=pipeline_context
        )
        
    def pipeline_start(self, pipeline_name: str, **kwargs) -> None:
        """Log pipeline start event."""
        context = {
            'pipeline_name': pipeline_name,
            'event_type': 'pipeline_start',
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            **kwargs
        }
        
        self.info(f"🚀 Starting pipeline: {pipeline_name}", pipeline_context=context)
        
    def pipeline_step(self, step_name: str, status: str = "started", **kwargs) -> None:
        """Log pipeline step event."""
        context = {
            'step_name': step_name,
            'status': status,
            'event_type': 'pipeline_step',
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            **kwargs
        }
        
        self.info(f"📋 Pipeline step: {step_name} - {status}", pipeline_context=context)
        
    def pipeline_complete(self, pipeline_name: str, duration_seconds: float, **kwargs) -> None:
        """Log pipeline completion event."""
        context = {
            'pipeline_name': pipeline_name,
            'event_type': 'pipeline_complete',
            'duration_seconds': duration_seconds,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            **kwargs
        }
        
        self.info(
            f"✅ Pipeline completed: {pipeline_name} in {duration_seconds:.2f}s",
            pipeline_context=context
        )
        
    def pipeline_error(self, pipeline_name: str, error: Exception, **kwargs) -> None:
        """Log pipeline error event."""
        context = {
            'pipeline_name': pipeline_name,
            'event_type': 'pipeline_error',
            'error_type': type(error).__name__,
            'error_message': str(error),
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            **kwargs
        }
        
        self.error(
            f"❌ Pipeline error: {pipeline_name} - {str(error)}",
            pipeline_context=context
        )
        
    def data_quality(self, quality_score: float, failed_checks: list, **kwargs) -> None:
        """Log data quality assessment."""
        context = {
            'event_type': 'data_quality',
            'quality_score': quality_score,
            'failed_checks': failed_checks,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            **kwargs
        }
        
        if quality_score >= self.config.data_quality.min_quality_score:
            self.info(
                f"✅ Data quality check passed: {quality_score:.2%}",
                pipeline_context=context
            )
        else:
            self.warning(
                f"⚠️ Data quality check failed: {quality_score:.2%}",
                pipeline_context=context
            )
            
    def gcp_operation(self, service: str, operation: str, status: str, **kwargs) -> None:
        """Log GCP operation status."""
        context = {
            'event_type': 'gcp_operation',
            'service': service,
            'operation': operation,
            'status': status,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            **kwargs
        }
        
        if status == 'success':
            self.info(
                f"☁️ GCP {service} {operation}: {status}",
                pipeline_context=context
            )
        elif status == 'error':
            self.error(
                f"❌ GCP {service} {operation}: {status}",
                pipeline_context=context
            )
        else:
            self.info(
                f"🔄 GCP {service} {operation}: {status}",
                pipeline_context=context
            )


def setup_logger(name: str, config: Optional[Config] = None) -> PipelineLogger:
    """
    Setup and return a configured pipeline logger.
    
    Args:
        name: Logger name
        config: Configuration object (optional)
        
    Returns:
        Configured PipelineLogger instance
    """
    if config is None:
        # Create default config if none provided
        config = Config()
        
    return PipelineLogger(name, config)


def get_logger(name: str) -> PipelineLogger:
    """
    Get an existing logger by name.
    
    Args:
        name: Logger name
        
    Returns:
        PipelineLogger instance
    """
    return PipelineLogger(name, Config())


# Convenience functions for common logging patterns
def log_pipeline_metrics(logger: PipelineLogger, metrics: Dict[str, Any]) -> None:
    """Log pipeline performance metrics."""
    logger.info(
        "📊 Pipeline metrics",
        extra_fields={
            'metrics': metrics,
            'event_type': 'pipeline_metrics'
        }
    )


def log_data_volume(logger: PipelineLogger, source: str, record_count: int, **kwargs) -> None:
    """Log data volume information."""
    logger.info(
        f"📈 Data volume from {source}: {record_count:,} records",
        extra_fields={
            'source': source,
            'record_count': record_count,
            'event_type': 'data_volume',
            **kwargs
        }
    )


def log_performance(logger: PipelineLogger, operation: str, duration_seconds: float, **kwargs) -> None:
    """Log performance metrics."""
    logger.info(
        f"⚡ Performance: {operation} completed in {duration_seconds:.2f}s",
        extra_fields={
            'operation': operation,
            'duration_seconds': duration_seconds,
            'event_type': 'performance',
            **kwargs
        }
    )
