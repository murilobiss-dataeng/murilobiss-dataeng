"""
Base pipeline class for TechFlow Solutions data pipelines
Common functionality and interface for all pipelines
"""

import logging
import time
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

from .config import config

@dataclass
class PipelineMetrics:
    """Pipeline execution metrics"""
    start_time: datetime
    end_time: Optional[datetime] = None
    records_processed: int = 0
    records_failed: int = 0
    processing_time_seconds: Optional[float] = None
    success: bool = False
    error_message: Optional[str] = None

class PipelineStatus:
    """Pipeline status enumeration"""
    IDLE = "idle"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    RETRYING = "retrying"

class BasePipeline(ABC):
    """Abstract base class for all data pipelines"""
    
    def __init__(self, pipeline_name: str):
        self.pipeline_name = pipeline_name
        self.status = PipelineStatus.IDLE
        self.metrics = PipelineMetrics(start_time=datetime.now())
        self.retry_count = 0
        self.max_retries = config.pipeline.retry_attempts
        
        # Setup logging
        self.logger = self._setup_logging()
        
        # Pipeline-specific configuration
        self.pipeline_config = config.get_pipeline_config(pipeline_name.lower())
        
    def _setup_logging(self) -> logging.Logger:
        """Setup pipeline-specific logging"""
        logger = logging.getLogger(f"pipeline.{self.pipeline_name}")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def run(self) -> bool:
        """Main pipeline execution method with error handling and retries"""
        self.logger.info(f"Starting {self.pipeline_name} pipeline")
        
        while self.retry_count <= self.max_retries:
            try:
                self.status = PipelineStatus.RUNNING
                self.metrics.start_time = datetime.now()
                
                # Execute pipeline-specific logic
                success = self._execute()
                
                if success:
                    self.status = PipelineStatus.SUCCESS
                    self.metrics.success = True
                    self._finalize_metrics()
                    self.logger.info(f"{self.pipeline_name} pipeline completed successfully")
                    return True
                else:
                    raise Exception("Pipeline execution returned False")
                    
            except Exception as e:
                self.retry_count += 1
                self.metrics.error_message = str(e)
                self.logger.error(f"Pipeline {self.pipeline_name} failed: {e}")
                
                if self.retry_count <= self.max_retries:
                    self.status = PipelineStatus.RETRYING
                    self.logger.info(f"Retrying {self.pipeline_name} pipeline (attempt {self.retry_count})")
                    time.sleep(min(60 * self.retry_count, 300))  # Exponential backoff, max 5 minutes
                else:
                    self.status = PipelineStatus.FAILED
                    self._finalize_metrics()
                    self.logger.error(f"Pipeline {self.pipeline_name} failed after {self.max_retries} retries")
                    return False
        
        return False
    
    def _finalize_metrics(self):
        """Finalize pipeline metrics"""
        self.metrics.end_time = datetime.now()
        if self.metrics.start_time and self.metrics.end_time:
            self.metrics.processing_time_seconds = (
                self.metrics.end_time - self.metrics.start_time
            ).total_seconds()
    
    @abstractmethod
    def _execute(self) -> bool:
        """Execute pipeline-specific logic - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def _validate_data(self) -> bool:
        """Validate input data - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def _process_data(self) -> bool:
        """Process data - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def _load_data(self) -> bool:
        """Load processed data to destination - must be implemented by subclasses"""
        pass
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get pipeline health status for monitoring"""
        return {
            'pipeline_name': self.pipeline_name,
            'status': self.status,
            'retry_count': self.retry_count,
            'last_run': self.metrics.start_time.isoformat() if self.metrics.start_time else None,
            'processing_time': self.metrics.processing_time_seconds,
            'records_processed': self.metrics.records_processed,
            'records_failed': self.metrics.records_failed,
            'success_rate': (
                (self.metrics.records_processed - self.metrics.records_failed) / 
                max(self.metrics.records_processed, 1)
            ),
            'sla_compliance': self._check_sla_compliance(),
        }
    
    def _check_sla_compliance(self) -> bool:
        """Check if pipeline meets SLA requirements"""
        if not self.metrics.end_time or not self.pipeline_config:
            return False
        
        sla_hours = self.pipeline_config.get('sla_hours', 24)
        processing_time_hours = self.metrics.processing_time_seconds / 3600 if self.metrics.processing_time_seconds else 0
        
        return processing_time_hours <= sla_hours
    
    def reset(self):
        """Reset pipeline state for next run"""
        self.status = PipelineStatus.IDLE
        self.retry_count = 0
        self.metrics = PipelineMetrics(start_time=datetime.now())
        self.logger.info(f"Pipeline {self.pipeline_name} reset for next run")
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Get pipeline configuration summary"""
        return {
            'pipeline_name': self.pipeline_name,
            'max_retries': self.max_retries,
            'pipeline_config': self.pipeline_config,
            'config_source': 'environment_variables'
        }
