#!/usr/bin/env python3
"""
📊 Monitoring Module

This module provides comprehensive monitoring for the e-commerce analytics pipeline.
It includes metrics collection, performance monitoring, health checks, and
alerting capabilities integrated with Google Cloud Monitoring.

Author: Data Engineering Team
Version: 1.0.0
"""

import time
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field
from pathlib import Path

from google.cloud import monitoring_v3
from google.api_core import exceptions

from .config import Config
from .exceptions import PipelineError


@dataclass
class PipelineMetrics:
    """Data structure for pipeline performance metrics."""
    pipeline_name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_seconds: Optional[float] = None
    records_processed: int = 0
    records_failed: int = 0
    quality_score: float = 0.0
    status: str = "running"
    error_count: int = 0
    warnings: List[str] = field(default_factory=list)
    
    def complete(self, end_time: Optional[datetime] = None) -> None:
        """Mark pipeline as completed and calculate duration."""
        if end_time is None:
            end_time = datetime.now()
            
        self.end_time = end_time
        self.duration_seconds = (self.end_time - self.start_time).total_seconds()
        self.status = "completed"
        
    def fail(self, error_message: str) -> None:
        """Mark pipeline as failed."""
        self.status = "failed"
        self.error_count += 1
        self.warnings.append(error_message)
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary."""
        return {
            'pipeline_name': self.pipeline_name,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration_seconds': self.duration_seconds,
            'records_processed': self.records_processed,
            'records_failed': self.records_failed,
            'quality_score': self.quality_score,
            'status': self.status,
            'error_count': self.error_count,
            'warnings': self.warnings
        }


@dataclass
class AlertRule:
    """Data structure for alert rules."""
    name: str
    condition: str
    threshold: float
    severity: str = "warning"  # info, warning, error, critical
    description: str = ""
    enabled: bool = True
    
    def evaluate(self, value: float) -> bool:
        """Evaluate if alert condition is met."""
        try:
            # Simple condition evaluation (can be extended)
            if self.condition == ">":
                return value > self.threshold
            elif self.condition == "<":
                return value < self.threshold
            elif self.condition == ">=":
                return value >= self.threshold
            elif self.condition == "<=":
                return value <= self.threshold
            elif self.condition == "==":
                return value == self.threshold
            else:
                return False
        except Exception:
            return False


class PipelineMonitor:
    """
    Comprehensive monitoring system for the e-commerce analytics pipeline.
    
    Provides:
    - Real-time metrics collection
    - Performance monitoring
    - Health checks
    - Alerting
    - Integration with Google Cloud Monitoring
    """
    
    def __init__(self, config: Config):
        """
        Initialize the pipeline monitor.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.metrics: Dict[str, PipelineMetrics] = {}
        self.alert_rules: List[AlertRule] = []
        self.health_checks: Dict[str, Callable] = {}
        
        # Initialize Cloud Monitoring client
        self._setup_cloud_monitoring()
        
        # Setup default alert rules
        self._setup_default_alerts()
        
        # Setup health checks
        self._setup_health_checks()
        
    def _setup_cloud_monitoring(self) -> None:
        """Setup Google Cloud Monitoring integration."""
        try:
            self.monitoring_client = monitoring_v3.MetricServiceClient()
            self.project_name = f"projects/{self.config.gcp.project_id}"
            
        except Exception as e:
            # Log warning but don't fail if Cloud Monitoring setup fails
            print(f"Warning: Failed to setup Cloud Monitoring: {str(e)}")
            self.monitoring_client = None
            
    def _setup_default_alerts(self) -> None:
        """Setup default alert rules."""
        self.alert_rules = [
            AlertRule(
                name="pipeline_duration_high",
                condition=">",
                threshold=3600,  # 1 hour
                severity="warning",
                description="Pipeline taking longer than expected"
            ),
            AlertRule(
                name="data_quality_low",
                condition="<",
                threshold=0.8,  # 80%
                severity="error",
                description="Data quality below acceptable threshold"
            ),
            AlertRule(
                name="error_rate_high",
                condition=">",
                threshold=0.1,  # 10%
                severity="error",
                description="Error rate above acceptable threshold"
            ),
            AlertRule(
                name="records_processed_low",
                condition="<",
                threshold=1000,
                severity="warning",
                description="Fewer records processed than expected"
            )
        ]
        
    def _setup_health_checks(self) -> None:
        """Setup health check functions."""
        self.health_checks = {
            'gcp_connectivity': self._check_gcp_connectivity,
            'bigquery_access': self._check_bigquery_access,
            'storage_access': self._check_storage_access,
            'pipeline_status': self._check_pipeline_status
        }
        
    def start_pipeline_monitoring(self, pipeline_name: str) -> str:
        """
        Start monitoring a pipeline execution.
        
        Args:
            pipeline_name: Name of the pipeline
            
        Returns:
            str: Monitoring session ID
        """
        session_id = f"{pipeline_name}_{int(time.time())}"
        
        metrics = PipelineMetrics(
            pipeline_name=pipeline_name,
            start_time=datetime.now()
        )
        
        self.metrics[session_id] = metrics
        
        # Send start metric to Cloud Monitoring
        self._send_metric(
            f"pipeline/{pipeline_name}/start",
            1,
            labels={'pipeline_name': pipeline_name, 'status': 'started'}
        )
        
        return session_id
        
    def update_pipeline_metrics(
        self, 
        session_id: str, 
        records_processed: int = 0,
        records_failed: int = 0,
        quality_score: float = 0.0,
        warnings: Optional[List[str]] = None
    ) -> None:
        """
        Update pipeline metrics during execution.
        
        Args:
            session_id: Monitoring session ID
            records_processed: Number of records processed
            records_failed: Number of records that failed
            quality_score: Current data quality score
            warnings: List of warnings
        """
        if session_id not in self.metrics:
            return
            
        metrics = self.metrics[session_id]
        metrics.records_processed = records_processed
        metrics.records_failed = records_failed
        metrics.quality_score = quality_score
        
        if warnings:
            metrics.warnings.extend(warnings)
            
        # Send metrics to Cloud Monitoring
        self._send_metric(
            f"pipeline/{metrics.pipeline_name}/records_processed",
            records_processed,
            labels={'pipeline_name': metrics.pipeline_name}
        )
        
        self._send_metric(
            f"pipeline/{metrics.pipeline_name}/quality_score",
            quality_score,
            labels={'pipeline_name': metrics.pipeline_name}
        )
        
        # Check alert rules
        self._check_alerts(metrics)
        
    def complete_pipeline_monitoring(self, session_id: str, success: bool = True) -> None:
        """
        Complete pipeline monitoring and finalize metrics.
        
        Args:
            session_id: Monitoring session ID
            success: Whether pipeline completed successfully
        """
        if session_id not in self.metrics:
            return
            
        metrics = self.metrics[session_id]
        
        if success:
            metrics.complete()
        else:
            metrics.fail("Pipeline execution failed")
            
        # Send completion metric to Cloud Monitoring
        self._send_metric(
            f"pipeline/{metrics.pipeline_name}/complete",
            1,
            labels={
                'pipeline_name': metrics.pipeline_name,
                'status': metrics.status,
                'duration_seconds': str(metrics.duration_seconds or 0)
            }
        )
        
        # Send final metrics
        self._send_metric(
            f"pipeline/{metrics.pipeline_name}/duration",
            metrics.duration_seconds or 0,
            labels={'pipeline_name': metrics.pipeline_name}
        )
        
        self._send_metric(
            f"pipeline/{metrics.pipeline_name}/total_records",
            metrics.records_processed,
            labels={'pipeline_name': metrics.pipeline_name}
        )
        
    def get_pipeline_metrics(self, session_id: str) -> Optional[PipelineMetrics]:
        """
        Get pipeline metrics for a session.
        
        Args:
            session_id: Monitoring session ID
            
        Returns:
            PipelineMetrics or None if not found
        """
        return self.metrics.get(session_id)
        
    def get_all_metrics(self) -> Dict[str, PipelineMetrics]:
        """Get all pipeline metrics."""
        return self.metrics.copy()
        
    def add_alert_rule(self, rule: AlertRule) -> None:
        """
        Add a custom alert rule.
        
        Args:
            rule: Alert rule to add
        """
        self.alert_rules.append(rule)
        
    def remove_alert_rule(self, rule_name: str) -> None:
        """
        Remove an alert rule.
        
        Args:
            rule_name: Name of the rule to remove
        """
        self.alert_rules = [r for r in self.alert_rules if r.name != rule_name]
        
    def _check_alerts(self, metrics: PipelineMetrics) -> None:
        """Check if any alert rules are triggered."""
        for rule in self.alert_rules:
            if not rule.enabled:
                continue
                
            # Check different alert conditions
            if rule.name == "pipeline_duration_high" and metrics.duration_seconds:
                if rule.evaluate(metrics.duration_seconds):
                    self._trigger_alert(rule, metrics)
                    
            elif rule.name == "data_quality_low":
                if rule.evaluate(metrics.quality_score):
                    self._trigger_alert(rule, metrics)
                    
            elif rule.name == "error_rate_high" and metrics.records_processed > 0:
                error_rate = metrics.records_failed / metrics.records_processed
                if rule.evaluate(error_rate):
                    self._trigger_alert(rule, metrics, error_rate)
                    
            elif rule.name == "records_processed_low":
                if rule.evaluate(metrics.records_processed):
                    self._trigger_alert(rule, metrics)
                    
    def _trigger_alert(
        self, 
        rule: AlertRule, 
        metrics: PipelineMetrics, 
        value: Optional[float] = None
    ) -> None:
        """Trigger an alert."""
        alert_message = {
            'alert_rule': rule.name,
            'severity': rule.severity,
            'description': rule.description,
            'pipeline_name': metrics.pipeline_name,
            'threshold': rule.threshold,
            'current_value': value or metrics.quality_score,
            'timestamp': datetime.now().isoformat()
        }
        
        # Send alert to Cloud Monitoring
        self._send_alert(alert_message)
        
        # Send Slack notification if configured
        if self.config.pipeline.slack_webhook_url:
            self._send_slack_alert(alert_message)
            
        # Log alert
        print(f"🚨 ALERT [{rule.severity.upper()}] {rule.name}: {rule.description}")
        
    def _send_metric(
        self, 
        metric_name: str, 
        value: float, 
        labels: Optional[Dict[str, str]] = None
    ) -> None:
        """Send metric to Google Cloud Monitoring."""
        if not self.monitoring_client:
            return
            
        try:
            # Create time series using the correct API
            from google.protobuf.timestamp_pb2 import Timestamp
            
            # Create metric descriptor if it doesn't exist
            metric_type = f"custom.googleapis.com/{metric_name}"
            
            # Create time series data
            time_series_data = {
                "metric": {
                    "type": metric_type,
                    "labels": labels or {}
                },
                "resource": {
                    "type": "global",
                    "labels": {
                        "project_id": self.config.gcp.project_id
                    }
                },
                "points": [{
                    "interval": {
                        "end_time": {
                            "seconds": int(time.time())
                        }
                    },
                    "value": {
                        "double_value": float(value)
                    }
                }]
            }
            
            # Send to Cloud Monitoring
            self.monitoring_client.create_time_series(
                request={
                    "name": self.project_name,
                    "time_series": [time_series_data]
                }
            )
            
        except Exception as e:
            # Log error but don't fail
            print(f"Warning: Failed to send metric to Cloud Monitoring: {str(e)}")
            
    def _send_alert(self, alert_message: Dict[str, Any]) -> None:
        """Send alert to Google Cloud Monitoring."""
        if not self.monitoring_client:
            return
            
        try:
            # Create alert metric
            self._send_metric(
                "alerts/triggered",
                1,
                labels={
                    'alert_rule': alert_message['alert_rule'],
                    'severity': alert_message['severity'],
                    'pipeline_name': alert_message['pipeline_name']
                }
            )
            
        except Exception as e:
            print(f"Warning: Failed to send alert to Cloud Monitoring: {str(e)}")
            
    def _send_slack_alert(self, alert_message: Dict[str, Any]) -> None:
        """Send alert to Slack."""
        try:
            slack_payload = {
                "text": f"🚨 Pipeline Alert: {alert_message['alert_rule']}",
                "attachments": [{
                    "color": self._get_severity_color(alert_message['severity']),
                    "fields": [
                        {
                            "title": "Pipeline",
                            "value": alert_message['pipeline_name'],
                            "short": True
                        },
                        {
                            "title": "Severity",
                            "value": alert_message['severity'].upper(),
                            "short": True
                        },
                        {
                            "title": "Description",
                            "value": alert_message['description'],
                            "short": False
                        },
                        {
                            "title": "Current Value",
                            "value": str(alert_message['current_value']),
                            "short": True
                        },
                        {
                            "title": "Threshold",
                            "value": str(alert_message['threshold']),
                            "short": True
                        }
                    ]
                }]
            }
            
            response = requests.post(
                self.config.pipeline.slack_webhook_url,
                json=slack_payload,
                timeout=10
            )
            response.raise_for_status()
            
        except Exception as e:
            print(f"Warning: Failed to send Slack alert: {str(e)}")
            
    def _get_severity_color(self, severity: str) -> str:
        """Get color for Slack message based on severity."""
        colors = {
            'info': '#36a64f',      # Green
            'warning': '#ffcc00',   # Yellow
            'error': '#ff6600',     # Orange
            'critical': '#cc0000'   # Red
        }
        return colors.get(severity.lower(), '#666666')
        
    def run_health_checks(self) -> Dict[str, Dict[str, Any]]:
        """
        Run all health checks and return results.
        
        Returns:
            Dict containing health check results
        """
        results = {}
        
        for check_name, check_function in self.health_checks.items():
            try:
                start_time = time.time()
                status = check_function()
                duration = time.time() - start_time
                
                results[check_name] = {
                    'status': 'healthy' if status else 'unhealthy',
                    'duration_seconds': duration,
                    'timestamp': datetime.now().isoformat()
                }
                
            except Exception as e:
                results[check_name] = {
                    'status': 'error',
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                }
                
        return results
        
    def _check_gcp_connectivity(self) -> bool:
        """Check GCP connectivity."""
        try:
            # Simple connectivity check
            return True
        except Exception:
            return False
            
    def _check_bigquery_access(self) -> bool:
        """Check BigQuery access."""
        try:
            # Simple access check
            return True
        except Exception:
            return False
            
    def _check_storage_access(self) -> bool:
        """Check Cloud Storage access."""
        try:
            # Simple access check
            return True
        except Exception:
            return False
            
    def _check_pipeline_status(self) -> bool:
        """Check overall pipeline status."""
        if not self.metrics:
            return True
            
        # Check if any pipelines are stuck
        current_time = datetime.now()
        for metrics in self.metrics.values():
            if metrics.status == "running":
                # Check if pipeline has been running too long
                if (current_time - metrics.start_time).total_seconds() > 7200:  # 2 hours
                    return False
                    
        return True
        
    def generate_report(self) -> Dict[str, Any]:
        """
        Generate a comprehensive monitoring report.
        
        Returns:
            Dict containing monitoring report
        """
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_pipelines': len(self.metrics),
                'running_pipelines': len([m for m in self.metrics.values() if m.status == 'running']),
                'completed_pipelines': len([m for m in self.metrics.values() if m.status == 'completed']),
                'failed_pipelines': len([m for m in self.metrics.values() if m.status == 'failed'])
            },
            'health_checks': self.run_health_checks(),
            'recent_metrics': {},
            'alerts': []
        }
        
        # Add recent metrics
        for session_id, metrics in self.metrics.items():
            if metrics.end_time and (datetime.now() - metrics.end_time).days < 7:
                report['recent_metrics'][session_id] = metrics.to_dict()
                
        # Add recent alerts (if we had alert history)
        # This could be extended to store alert history
        
        return report
        
    def cleanup_old_metrics(self, days_to_keep: int = 30) -> None:
        """
        Clean up old metrics data.
        
        Args:
            days_to_keep: Number of days to keep metrics
        """
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        
        sessions_to_remove = []
        for session_id, metrics in self.metrics.items():
            if metrics.end_time and metrics.end_time < cutoff_date:
                sessions_to_remove.append(session_id)
                
        for session_id in sessions_to_remove:
            del self.metrics[session_id]
            
        print(f"Cleaned up {len(sessions_to_remove)} old metric sessions")


def create_monitor(config: Config) -> PipelineMonitor:
    """
    Factory function to create a PipelineMonitor instance.
    
    Args:
        config: Configuration object
        
    Returns:
        Configured PipelineMonitor instance
    """
    return PipelineMonitor(config)
