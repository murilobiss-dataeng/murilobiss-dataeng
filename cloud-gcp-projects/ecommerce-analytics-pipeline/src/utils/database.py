#!/usr/bin/env python3
"""
🗄️ Database Utilities Module

This module provides database utilities and connection management for the e-commerce analytics pipeline.
It includes connection pooling, query execution, and database-specific operations.

Author: Data Engineering Team
Version: 1.0.0
"""

import logging
from typing import Any, Dict, List, Optional, Union, Tuple
from contextlib import contextmanager
import pandas as pd
from datetime import datetime, timedelta

from .exceptions import DatabaseError, ConnectionError


class DatabaseConnection:
    """Base class for database connections."""
    
    def __init__(self, connection_string: str, **kwargs):
        """
        Initialize database connection.
        
        Args:
            connection_string: Database connection string
            **kwargs: Additional connection parameters
        """
        self.connection_string = connection_string
        self.connection_params = kwargs
        self.connection = None
        self.logger = logging.getLogger(__name__)
    
    def connect(self) -> bool:
        """
        Establish database connection.
        
        Returns:
            bool: True if connection successful
        """
        raise NotImplementedError("Subclasses must implement connect method")
    
    def disconnect(self) -> None:
        """Close database connection."""
        if self.connection:
            try:
                self.connection.close()
                self.connection = None
                self.logger.info("Database connection closed")
            except Exception as e:
                self.logger.error(f"Error closing database connection: {e}")
    
    def is_connected(self) -> bool:
        """
        Check if connection is active.
        
        Returns:
            bool: True if connected
        """
        return self.connection is not None
    
    def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Execute a database query.
        
        Args:
            query: SQL query to execute
            params: Query parameters
            
        Returns:
            Any: Query result
        """
        raise NotImplementedError("Subclasses must implement execute_query method")
    
    def execute_batch(self, queries: List[str], params: Optional[List[Dict[str, Any]]] = None) -> List[Any]:
        """
        Execute multiple queries in batch.
        
        Args:
            queries: List of SQL queries
            params: List of parameter dictionaries
            
        Returns:
            List[Any]: List of query results
        """
        results = []
        for i, query in enumerate(queries):
            param = params[i] if params and i < len(params) else None
            try:
                result = self.execute_query(query, param)
                results.append(result)
            except Exception as e:
                self.logger.error(f"Error executing query {i}: {e}")
                results.append(None)
        return results


class BigQueryConnection(DatabaseConnection):
    """BigQuery connection wrapper."""
    
    def __init__(self, project_id: str, dataset_id: str, **kwargs):
        """
        Initialize BigQuery connection.
        
        Args:
            project_id: GCP project ID
            dataset_id: BigQuery dataset ID
            **kwargs: Additional connection parameters
        """
        super().__init__(f"bigquery://{project_id}.{dataset_id}", **kwargs)
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.client = None
    
    def connect(self) -> bool:
        """
        Establish BigQuery connection.
        
        Returns:
            bool: True if connection successful
        """
        try:
            from google.cloud import bigquery
            self.client = bigquery.Client(project=self.project_id)
            self.connection = self.client
            self.logger.info(f"Connected to BigQuery project: {self.project_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to connect to BigQuery: {e}")
            raise ConnectionError(f"BigQuery connection failed: {e}")
    
    def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """
        Execute BigQuery query.
        
        Args:
            query: SQL query to execute
            params: Query parameters
            
        Returns:
            pd.DataFrame: Query result as DataFrame
        """
        if not self.is_connected():
            raise ConnectionError("Not connected to BigQuery")
        
        try:
            # Handle parameter substitution
            if params:
                for key, value in params.items():
                    if isinstance(value, str):
                        query = query.replace(f":{key}", f"'{value}'")
                    else:
                        query = query.replace(f":{key}", str(value))
            
            # Execute query
            query_job = self.client.query(query)
            results = query_job.result()
            
            # Convert to DataFrame
            return results.to_dataframe()
            
        except Exception as e:
            self.logger.error(f"Query execution failed: {e}")
            raise DatabaseError(f"Query execution failed: {e}")
    
    def create_table(self, table_name: str, schema: List[Dict[str, Any]], 
                    partition_field: Optional[str] = None) -> bool:
        """
        Create BigQuery table.
        
        Args:
            table_name: Name of the table
            schema: Table schema definition
            partition_field: Partition field name
            
        Returns:
            bool: True if successful
        """
        if not self.is_connected():
            raise ConnectionError("Not connected to BigQuery")
        
        try:
            from google.cloud import bigquery
            
            # Create schema fields
            schema_fields = []
            for field in schema:
                schema_fields.append(
                    bigquery.SchemaField(
                        name=field['name'],
                        field_type=field['type'],
                        mode=field.get('mode', 'NULLABLE'),
                        description=field.get('description', '')
                    )
                )
            
            # Create table reference
            table_ref = self.client.dataset(self.dataset_id).table(table_name)
            
            # Create table
            table = bigquery.Table(table_ref, schema=schema_fields)
            
            # Add partitioning if specified
            if partition_field:
                table.time_partitioning = bigquery.TimePartitioning(
                    type_=bigquery.TimePartitioningType.DAY,
                    field=partition_field
                )
            
            # Create the table
            self.client.create_table(table, exists_ok=True)
            self.logger.info(f"Table {table_name} created successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create table {table_name}: {e}")
            raise DatabaseError(f"Table creation failed: {e}")
    
    def insert_data(self, table_name: str, data: Union[pd.DataFrame, List[Dict[str, Any]]]) -> bool:
        """
        Insert data into BigQuery table.
        
        Args:
            table_name: Name of the target table
            data: Data to insert
            
        Returns:
            bool: True if successful
        """
        if not self.is_connected():
            raise ConnectionError("Not connected to BigQuery")
        
        try:
            # Convert to DataFrame if needed
            if isinstance(data, list):
                df = pd.DataFrame(data)
            else:
                df = data
            
            # Get table reference
            table_ref = self.client.dataset(self.dataset_id).table(table_name)
            
            # Load data
            job_config = bigquery.LoadJobConfig(
                write_disposition=bigquery.WriteDisposition.WRITE_APPEND
            )
            
            job = self.client.load_table_from_dataframe(
                df, table_ref, job_config=job_config
            )
            job.result()  # Wait for job to complete
            
            self.logger.info(f"Data inserted into {table_name} successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to insert data into {table_name}: {e}")
            raise DatabaseError(f"Data insertion failed: {e}")


class ConnectionPool:
    """Database connection pool manager."""
    
    def __init__(self, max_connections: int = 10):
        """
        Initialize connection pool.
        
        Args:
            max_connections: Maximum number of connections in pool
        """
        self.max_connections = max_connections
        self.connections = []
        self.active_connections = set()
        self.logger = logging.getLogger(__name__)
    
    def get_connection(self, connection_class: type, **kwargs) -> DatabaseConnection:
        """
        Get a database connection from the pool.
        
        Args:
            connection_class: Connection class to instantiate
            **kwargs: Connection parameters
            
        Returns:
            DatabaseConnection: Database connection instance
        """
        # Check if we can create a new connection
        if len(self.active_connections) < self.max_connections:
            connection = connection_class(**kwargs)
            if connection.connect():
                self.active_connections.add(connection)
                return connection
        
        # Wait for an available connection
        self.logger.warning("Connection pool full, waiting for available connection")
        return self._wait_for_connection(connection_class, **kwargs)
    
    def _wait_for_connection(self, connection_class: type, **kwargs) -> DatabaseConnection:
        """
        Wait for an available connection.
        
        Args:
            connection_class: Connection class to instantiate
            **kwargs: Connection parameters
            
        Returns:
            DatabaseConnection: Database connection instance
        """
        import time
        
        while len(self.active_connections) >= self.max_connections:
            time.sleep(0.1)
        
        return self.get_connection(connection_class, **kwargs)
    
    def release_connection(self, connection: DatabaseConnection) -> None:
        """
        Release a connection back to the pool.
        
        Args:
            connection: Connection to release
        """
        if connection in self.active_connections:
            connection.disconnect()
            self.active_connections.remove(connection)
            self.logger.debug("Connection released back to pool")
    
    def close_all(self) -> None:
        """Close all connections in the pool."""
        for connection in list(self.active_connections):
            self.release_connection(connection)
        self.logger.info("All connections closed")


@contextmanager
def get_db_connection(connection_class: type, **kwargs):
    """
    Context manager for database connections.
    
    Args:
        connection_class: Connection class to instantiate
        **kwargs: Connection parameters
        
    Yields:
        DatabaseConnection: Database connection instance
    """
    connection = None
    try:
        connection = connection_class(**kwargs)
        connection.connect()
        yield connection
    finally:
        if connection:
            connection.disconnect()


def execute_sql_file(file_path: str, connection: DatabaseConnection, 
                    params: Optional[Dict[str, Any]] = None) -> List[Any]:
    """
    Execute SQL commands from a file.
    
    Args:
        file_path: Path to SQL file
        connection: Database connection
        params: Parameters to substitute in queries
        
    Returns:
        List[Any]: Results of executed queries
    """
    try:
        with open(file_path, 'r') as f:
            sql_content = f.read()
        
        # Split into individual statements
        statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
        
        results = []
        for statement in statements:
            if statement:
                result = connection.execute_query(statement, params)
                results.append(result)
        
        return results
        
    except Exception as e:
        logging.error(f"Failed to execute SQL file {file_path}: {e}")
        raise DatabaseError(f"SQL file execution failed: {e}")


def backup_table(connection: DatabaseConnection, table_name: str, 
                backup_suffix: str = "_backup") -> str:
    """
    Create a backup of a table.
    
    Args:
        connection: Database connection
        table_name: Name of the table to backup
        backup_suffix: Suffix for backup table name
        
    Returns:
        str: Name of the backup table
    """
    backup_table_name = f"{table_name}{backup_suffix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    try:
        # Create backup table
        backup_query = f"CREATE TABLE {backup_table_name} AS SELECT * FROM {table_name}"
        connection.execute_query(backup_query)
        
        logging.info(f"Table {table_name} backed up to {backup_table_name}")
        return backup_table_name
        
    except Exception as e:
        logging.error(f"Failed to backup table {table_name}: {e}")
        raise DatabaseError(f"Table backup failed: {e}")


def restore_table(connection: DatabaseConnection, table_name: str, 
                 backup_table_name: str) -> bool:
    """
    Restore a table from backup.
    
    Args:
        connection: Database connection
        table_name: Name of the table to restore
        backup_table_name: Name of the backup table
        
    Returns:
        bool: True if successful
    """
    try:
        # Drop existing table
        drop_query = f"DROP TABLE IF EXISTS {table_name}"
        connection.execute_query(drop_query)
        
        # Restore from backup
        restore_query = f"CREATE TABLE {table_name} AS SELECT * FROM {backup_table_name}"
        connection.execute_query(restore_query)
        
        logging.info(f"Table {table_name} restored from {backup_table_name}")
        return True
        
    except Exception as e:
        logging.error(f"Failed to restore table {table_name}: {e}")
        raise DatabaseError(f"Table restore failed: {e}")
