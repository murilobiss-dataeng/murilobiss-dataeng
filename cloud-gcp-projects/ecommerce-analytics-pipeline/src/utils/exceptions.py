#!/usr/bin/env python3
"""
🚨 Custom Exceptions Module

This module defines custom exceptions for the e-commerce analytics pipeline.
These exceptions provide better error handling and more informative error messages.

Author: Data Engineering Team
Version: 1.0.0
"""


class PipelineError(Exception):
    """Base exception for all pipeline-related errors."""
    
    def __init__(self, message: str, error_code: str = None, details: dict = None):
        """
        Initialize the pipeline error.
        
        Args:
            message: Error message
            error_code: Optional error code for categorization
            details: Optional dictionary with additional error details
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        
    def __str__(self):
        """Return string representation of the error."""
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message


class ExtractionError(PipelineError):
    """Exception raised when data extraction fails."""
    
    def __init__(self, message: str, source: str = None, details: dict = None):
        """
        Initialize extraction error.
        
        Args:
            message: Error message
            source: Data source that failed
            details: Additional error details
        """
        super().__init__(message, "EXTRACTION_ERROR", details)
        self.source = source


class TransformationError(PipelineError):
    """Exception raised when data transformation fails."""
    
    def __init__(self, message: str, transformation_step: str = None, details: dict = None):
        """
        Initialize transformation error.
        
        Args:
            message: Error message
            transformation_step: Step that failed
            details: Additional error details
        """
        super().__init__(message, "TRANSFORMATION_ERROR", details)
        self.transformation_step = transformation_step


class LoadingError(PipelineError):
    """Exception raised when data loading fails."""
    
    def __init__(self, message: str, destination: str = None, details: dict = None):
        """
        Initialize loading error.
        
        Args:
            message: Error message
            destination: Destination that failed
            details: Additional error details
        """
        super().__init__(message, "LOADING_ERROR", details)
        self.destination = destination


class ValidationError(PipelineError):
    """Exception raised when data validation fails."""
    
    def __init__(self, message: str, validation_rule: str = None, details: dict = None):
        """
        Initialize validation error.
        
        Args:
            message: Error message
            validation_rule: Rule that failed
            details: Additional error details
        """
        super().__init__(message, "VALIDATION_ERROR", details)
        self.validation_rule = validation_rule


class ConfigurationError(PipelineError):
    """Exception raised when configuration is invalid."""
    
    def __init__(self, message: str, config_key: str = None, details: dict = None):
        """
        Initialize configuration error.
        
        Args:
            message: Error message
            config_key: Configuration key that caused the error
            details: Additional error details
        """
        super().__init__(message, "CONFIGURATION_ERROR", details)
        self.config_key = config_key


class GCPError(PipelineError):
    """Exception raised when GCP service operations fail."""
    
    def __init__(self, message: str, service: str = None, operation: str = None, details: dict = None):
        """
        Initialize GCP error.
        
        Args:
            message: Error message
            service: GCP service that failed
            operation: Operation that failed
            details: Additional error details
        """
        super().__init__(message, "GCP_ERROR", details)
        self.service = service
        self.operation = operation


class DataQualityError(PipelineError):
    """Exception raised when data quality checks fail."""
    
    def __init__(self, message: str, quality_score: float = None, failed_checks: list = None, details: dict = None):
        """
        Initialize data quality error.
        
        Args:
            message: Error message
            quality_score: Data quality score
            failed_checks: List of failed quality checks
            details: Additional error details
        """
        super().__init__(message, "DATA_QUALITY_ERROR", details)
        self.quality_score = quality_score
        self.failed_checks = failed_checks or []


class AuthenticationError(PipelineError):
    """Exception raised when authentication fails."""
    
    def __init__(self, message: str, service: str = None, details: dict = None):
        """
        Initialize authentication error.
        
        Args:
            message: Error message
            service: Service that failed authentication
            details: Additional error details
        """
        super().__init__(message, "AUTHENTICATION_ERROR", details)
        self.service = service


class NetworkError(PipelineError):
    """Exception raised when network operations fail."""
    
    def __init__(self, message: str, endpoint: str = None, status_code: int = None, details: dict = None):
        """
        Initialize network error.
        
        Args:
            message: Error message
            endpoint: Endpoint that failed
            status_code: HTTP status code if applicable
            details: Additional error details
        """
        super().__init__(message, "NETWORK_ERROR", details)
        self.endpoint = endpoint
        self.status_code = status_code


class ResourceNotFoundError(PipelineError):
    """Exception raised when a required resource is not found."""
    
    def __init__(self, message: str, resource_type: str = None, resource_id: str = None, details: dict = None):
        """
        Initialize resource not found error.
        
        Args:
            message: Error message
            resource_type: Type of resource not found
            resource_id: ID of resource not found
            details: Additional error details
        """
        super().__init__(message, "RESOURCE_NOT_FOUND", details)
        self.resource_type = resource_type
        self.resource_id = resource_id


class RateLimitError(PipelineError):
    """Exception raised when rate limits are exceeded."""
    
    def __init__(self, message: str, service: str = None, retry_after: int = None, details: dict = None):
        """
        Initialize rate limit error.
        
        Args:
            message: Error message
            service: Service that hit rate limit
            retry_after: Seconds to wait before retrying
            details: Additional error details
        """
        super().__init__(message, "RATE_LIMIT_ERROR", details)
        self.service = service
        self.retry_after = retry_after


class TimeoutError(PipelineError):
    """Exception raised when operations timeout."""
    
    def __init__(self, message: str, operation: str = None, timeout_seconds: int = None, details: dict = None):
        """
        Initialize timeout error.
        
        Args:
            message: Error message
            operation: Operation that timed out
            timeout_seconds: Timeout duration in seconds
            details: Additional error details
        """
        super().__init__(message, "TIMEOUT_ERROR", details)
        self.operation = operation
        self.timeout_seconds = timeout_seconds


class DatabaseError(PipelineError):
    """Exception raised when database operations fail."""
    
    def __init__(self, message: str, operation: str = None, table: str = None, details: dict = None):
        """
        Initialize database error.
        
        Args:
            message: Error message
            operation: Operation that failed
            table: Table involved in the operation
            details: Additional error details
        """
        super().__init__(message, "DATABASE_ERROR", details)
        self.operation = operation
        self.table = table


class ConnectionError(PipelineError):
    """Exception raised when database connections fail."""
    
    def __init__(self, message: str, service: str = None, connection_string: str = None, details: dict = None):
        """
        Initialize connection error.
        
        Args:
            message: Error message
            service: Service that failed to connect
            connection_string: Connection string used
            details: Additional error details
        """
        super().__init__(message, "CONNECTION_ERROR", details)
        self.service = service
        self.connection_string = connection_string


def handle_pipeline_error(error: Exception, context: str = None) -> dict:
    """
    Handle pipeline errors and return structured error information.
    
    Args:
        error: The exception that occurred
        context: Context where the error occurred
        
    Returns:
        dict: Structured error information
    """
    if isinstance(error, PipelineError):
        return {
            'error_type': error.__class__.__name__,
            'error_code': error.error_code,
            'message': error.message,
            'context': context,
            'details': error.details,
            'timestamp': None  # Will be set by caller
        }
    else:
        return {
            'error_type': 'UnexpectedError',
            'error_code': 'UNEXPECTED_ERROR',
            'message': str(error),
            'context': context,
            'details': {},
            'timestamp': None  # Will be set by caller
        }
