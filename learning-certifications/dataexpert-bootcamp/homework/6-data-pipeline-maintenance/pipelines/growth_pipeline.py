"""
Growth Pipeline for TechFlow Solutions
Tracks account growth metrics and subscription changes for experiments and investor reporting
"""

import logging
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from .base_pipeline import BasePipeline
from .config import config

class GrowthPipeline(BasePipeline):
    """Pipeline for tracking account growth metrics and subscription changes"""
    
    def __init__(self):
        super().__init__("Growth")
        self.db_engine = None
        self.account_changes = None
        self.license_changes = None
        self.subscription_renewals = None
        self.account_status_history = None
        
    def _execute(self) -> bool:
        """Execute growth pipeline"""
        try:
            # Connect to database
            if not self._connect_database():
                return False
            
            # Extract data
            if not self._extract_data():
                return False
            
            # Validate data
            if not self._validate_data():
                return False
            
            # Process data
            if not self._process_data():
                return False
            
            # Load data
            if not self._load_data():
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Growth pipeline execution failed: {e}")
            return False
        finally:
            if self.db_engine:
                self.db_engine.dispose()
    
    def _connect_database(self) -> bool:
        """Connect to database"""
        try:
            connection_string = (
                f"postgresql://{config.database.username}:{config.database.password}"
                f"@{config.database.host}:{config.database.port}/{config.database.database}"
            )
            self.db_engine = create_engine(connection_string)
            
            # Test connection
            with self.db_engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            self.logger.info("Database connection established")
            return True
            
        except Exception as e:
            self.logger.error(f"Database connection failed: {e}")
            return False
    
    def _extract_data(self) -> bool:
        """Extract account growth and subscription data"""
        try:
            # Extract account status changes
            status_query = """
                SELECT 
                    account_id,
                    previous_status,
                    new_status,
                    change_date,
                    change_reason,
                    sales_rep,
                    contract_value
                FROM account_status_changes 
                WHERE change_date >= CURRENT_DATE - INTERVAL '1 week'
                ORDER BY change_date DESC
            """
            
            self.account_changes = pd.read_sql(status_query, self.db_engine)
            self.logger.info(f"Extracted {len(self.account_changes)} account status changes")
            
            # Extract license changes
            license_query = """
                SELECT 
                    account_id,
                    previous_licenses,
                    new_licenses,
                    change_date,
                    change_type,
                    additional_revenue,
                    effective_date
                FROM license_changes 
                WHERE change_date >= CURRENT_DATE - INTERVAL '1 week'
                ORDER BY change_date DESC
            """
            
            self.license_changes = pd.read_sql(license_query, self.db_engine)
            self.logger.info(f"Extracted {len(self.license_changes)} license changes")
            
            # Extract subscription renewals
            renewal_query = """
                SELECT 
                    account_id,
                    renewal_date,
                    previous_contract_value,
                    new_contract_value,
                    renewal_type,
                    contract_duration
                FROM subscription_renewals 
                WHERE renewal_date >= CURRENT_DATE - INTERVAL '1 week'
                ORDER BY renewal_date DESC
            """
            
            self.subscription_renewals = pd.read_sql(renewal_query, self.db_engine)
            self.logger.info(f"Extracted {len(self.subscription_renewals)} subscription renewals")
            
            # Extract account status history for validation
            history_query = """
                SELECT 
                    account_id,
                    status,
                    effective_date,
                    end_date
                FROM account_status_history 
                WHERE effective_date >= CURRENT_DATE - INTERVAL '1 month'
                ORDER BY account_id, effective_date
            """
            
            self.account_status_history = pd.read_sql(history_query, self.db_engine)
            self.logger.info(f"Extracted {len(self.account_status_history)} account status history records")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Data extraction failed: {e}")
            return False
    
    def _validate_data(self) -> bool:
        """Validate extracted data"""
        try:
            # Check data completeness
            if self.account_changes.empty and self.license_changes.empty and self.subscription_renewals.empty:
                self.logger.warning("No growth data found for the week")
                # This is not necessarily an error, just a warning
            
            # Validate account status changes
            if not self.account_changes.empty:
                status_validation = self._validate_account_status_changes()
                if not status_validation:
                    return False
            
            # Validate license changes
            if not self.license_changes.empty:
                license_validation = self._validate_license_changes()
                if not license_validation:
                    return False
            
            # Validate subscription renewals
            if not self.subscription_renewals.empty:
                renewal_validation = self._validate_subscription_renewals()
                if not renewal_validation:
                    return False
            
            # Validate account status completeness
            completeness_validation = self._validate_account_status_completeness()
            if not completeness_validation:
                return False
            
            self.logger.info("Data validation completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Data validation failed: {e}")
            return False
    
    def _validate_account_status_changes(self) -> bool:
        """Validate account status change data quality"""
        try:
            # Check for missing values
            missing_values = self.account_changes.isnull().sum()
            if missing_values.sum() > 0:
                self.logger.warning(f"Account changes have missing values: {missing_values.to_dict()}")
            
            # Check for invalid status transitions
            invalid_transitions = self._check_invalid_status_transitions()
            if invalid_transitions:
                self.logger.error(f"Found {len(invalid_transitions)} invalid status transitions")
                return False
            
            # Check for missing intermediate steps
            missing_steps = self._check_missing_intermediate_steps()
            if missing_steps:
                self.logger.error(f"Found {len(missing_steps)} missing intermediate status steps")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Account status validation failed: {e}")
            return False
    
    def _validate_license_changes(self) -> bool:
        """Validate license change data quality"""
        try:
            # Check for missing values
            missing_values = self.license_changes.isnull().sum()
            if missing_values.sum() > 0:
                self.logger.warning(f"License changes have missing values: {missing_values.to_dict()}")
            
            # Check for negative license changes
            negative_changes = self.license_changes[
                self.license_changes['new_licenses'] < self.license_changes['previous_licenses']
            ]
            if not negative_changes.empty:
                self.logger.warning(f"Found {len(negative_changes)} license downgrades")
            
            # Check for unreasonable license increases
            unreasonable_increases = self.license_changes[
                self.license_changes['new_licenses'] > self.license_changes['previous_licenses'] * 10
            ]
            if not unreasonable_increases.empty:
                self.logger.warning(f"Found {len(unreasonable_increases)} potentially unreasonable license increases")
            
            return True
            
        except Exception as e:
            self.logger.error(f"License validation failed: {e}")
            return False
    
    def _validate_subscription_renewals(self) -> bool:
        """Validate subscription renewal data quality"""
        try:
            # Check for missing values
            missing_values = self.subscription_renewals.isnull().sum()
            if missing_values.sum() > 0:
                self.logger.warning(f"Subscription renewals have missing values: {missing_values.sum()}")
            
            # Check for negative contract values
            negative_values = self.subscription_renewals[
                self.subscription_renewals['new_contract_value'] < 0
            ]
            if not negative_values.empty:
                self.logger.error(f"Found {len(negative_values)} records with negative contract values")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Subscription renewal validation failed: {e}")
            return False
    
    def _validate_account_status_completeness(self) -> bool:
        """Validate that all accounts have current status"""
        try:
            if self.account_status_history.empty:
                self.logger.warning("No account status history available for validation")
                return True
            
            # Get current account statuses
            current_statuses = self.account_status_history[
                (self.account_status_history['end_date'].isna()) | 
                (self.account_status_history['end_date'] > datetime.now())
            ]
            
            # Get all unique account IDs from changes
            changed_accounts = set()
            if not self.account_changes.empty:
                changed_accounts.update(self.account_changes['account_id'].unique())
            if not self.license_changes.empty:
                changed_accounts.update(self.license_changes['account_id'].unique())
            if not self.subscription_renewals.empty:
                changed_accounts.update(self.subscription_renewals['account_id'].unique())
            
            # Check if all changed accounts have current status
            missing_statuses = changed_accounts - set(current_statuses['account_id'].unique())
            
            if missing_statuses:
                self.logger.error(f"Found {len(missing_statuses)} accounts without current status")
                return False
            
            self.logger.info("Account status completeness validation passed")
            return True
            
        except Exception as e:
            self.logger.error(f"Account status completeness validation failed: {e}")
            return False
    
    def _check_invalid_status_transitions(self) -> List[Dict[str, Any]]:
        """Check for invalid status transitions"""
        invalid_transitions = []
        
        # Define valid status transitions
        valid_transitions = {
            'Trial': ['Active', 'Cancelled'],
            'Active': ['Suspended', 'Cancelled', 'Expired'],
            'Suspended': ['Active', 'Cancelled'],
            'Expired': ['Active', 'Cancelled']
        }
        
        for _, change in self.account_changes.iterrows():
            previous = change['previous_status']
            new = change['new_status']
            
            if previous in valid_transitions and new not in valid_transitions[previous]:
                invalid_transitions.append({
                    'account_id': change['account_id'],
                    'invalid_transition': f"{previous} -> {new}",
                    'change_date': change['change_date']
                })
        
        return invalid_transitions
    
    def _check_missing_intermediate_steps(self) -> List[Dict[str, Any]]:
        """Check for missing intermediate status steps"""
        missing_steps = []
        
        # Check for direct transitions that should have intermediate steps
        direct_transitions = {
            ('Trial', 'Expired'): 'Active',  # Should go through Active first
            ('Active', 'Expired'): 'Suspended'  # Should go through Suspended first
        }
        
        for _, change in self.account_changes.iterrows():
            transition = (change['previous_status'], change['new_status'])
            
            if transition in direct_transitions:
                missing_step = direct_transitions[transition]
                missing_steps.append({
                    'account_id': change['account_id'],
                    'missing_step': missing_step,
                    'transition': f"{transition[0]} -> {transition[1]}",
                    'change_date': change['change_date']
                })
        
        return missing_steps
    
    def _process_data(self) -> bool:
        """Process data to calculate growth metrics"""
        try:
            # Calculate account growth metrics
            account_growth_metrics = self._calculate_account_growth()
            
            # Calculate license growth metrics
            license_growth_metrics = self._calculate_license_growth()
            
            # Calculate revenue growth metrics
            revenue_growth_metrics = self._calculate_revenue_growth()
            
            # Combine all metrics
            self.processed_metrics = {
                'account_growth': account_growth_metrics,
                'license_growth': license_growth_metrics,
                'revenue_growth': revenue_growth_metrics,
                'processing_date': datetime.now().isoformat(),
                'data_completeness': self._calculate_data_completeness()
            }
            
            # Update metrics
            total_records = (
                len(self.account_changes) + 
                len(self.license_changes) + 
                len(self.subscription_renewals)
            )
            self.metrics.records_processed = total_records
            
            self.logger.info("Data processing completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Data processing failed: {e}")
            return False
    
    def _calculate_account_growth(self) -> Dict[str, Any]:
        """Calculate account growth metrics"""
        if self.account_changes.empty:
            return {'total_changes': 0, 'new_accounts': 0, 'cancelled_accounts': 0}
        
        total_changes = len(self.account_changes)
        new_accounts = len(self.account_changes[
            self.account_changes['new_status'] == 'Active'
        ])
        cancelled_accounts = len(self.account_changes[
            self.account_changes['new_status'] == 'Cancelled'
        ])
        
        return {
            'total_changes': total_changes,
            'new_accounts': new_accounts,
            'cancelled_accounts': cancelled_accounts,
            'net_growth': new_accounts - cancelled_accounts
        }
    
    def _calculate_license_growth(self) -> Dict[str, Any]:
        """Calculate license growth metrics"""
        if self.license_changes.empty:
            return {'total_changes': 0, 'license_increases': 0, 'total_additional_licenses': 0}
        
        total_changes = len(self.license_changes)
        license_increases = len(self.license_changes[
            self.license_changes['new_licenses'] > self.license_changes['previous_licenses']
        ])
        total_additional_licenses = self.license_changes[
            self.license_changes['new_licenses'] > self.license_changes['previous_licenses']
        ]['new_licenses'].sum() - self.license_changes[
            self.license_changes['new_licenses'] > self.license_changes['previous_licenses']
        ]['previous_licenses'].sum()
        
        return {
            'total_changes': total_changes,
            'license_increases': license_increases,
            'total_additional_licenses': int(total_additional_licenses)
        }
    
    def _calculate_revenue_growth(self) -> Dict[str, Any]:
        """Calculate revenue growth metrics"""
        if self.subscription_renewals.empty:
            return {'total_renewals': 0, 'revenue_increase': 0, 'expansion_rate': 0}
        
        total_renewals = len(self.subscription_renewals)
        revenue_increase = self.subscription_renewals['new_contract_value'].sum() - \
                         self.subscription_renewals['previous_contract_value'].sum()
        expansion_rate = len(self.subscription_renewals[
            self.subscription_renewals['new_contract_value'] > self.subscription_renewals['previous_contract_value']
        ]) / total_renewals if total_renewals > 0 else 0
        
        return {
            'total_renewals': total_renewals,
            'revenue_increase': revenue_increase,
            'expansion_rate': expansion_rate
        }
    
    def _calculate_data_completeness(self) -> float:
        """Calculate data completeness percentage"""
        if self.account_status_history.empty:
            return 0.0
        
        # Get total accounts
        total_accounts = self.account_status_history['account_id'].nunique()
        
        # Get accounts with current status
        current_accounts = self.account_status_history[
            (self.account_status_history['end_date'].isna()) | 
            (self.account_status_history['end_date'] > datetime.now())
        ]['account_id'].nunique()
        
        return current_accounts / total_accounts if total_accounts > 0 else 0.0
    
    def _load_data(self) -> bool:
        """Load processed growth metrics to destination tables"""
        try:
            # Load aggregate growth metrics for investors
            self._load_investor_metrics()
            
            # Load daily growth metrics for experiments
            self._load_experiment_metrics()
            
            # Load growth trend analysis
            self._load_growth_trends()
            
            self.logger.info("Data loading completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Data loading failed: {e}")
            return False
    
    def _load_investor_metrics(self):
        """Load aggregate growth metrics for investor reporting"""
        try:
            investor_data = pd.DataFrame([{
                'report_date': datetime.now().date(),
                'account_growth': self.processed_metrics['account_growth']['net_growth'],
                'license_growth': self.processed_metrics['license_growth']['total_additional_licenses'],
                'revenue_growth': self.processed_metrics['revenue_growth']['revenue_increase'],
                'expansion_rate': self.processed_metrics['revenue_growth']['expansion_rate'],
                'report_type': 'weekly_investor'
            }])
            
            investor_data.to_sql('investor_growth_metrics', self.db_engine, 
                               if_exists='append', index=False)
            
            self.logger.info("Investor growth metrics loaded successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to load investor growth metrics: {e}")
            raise
    
    def _load_experiment_metrics(self):
        """Load daily growth metrics for data science experiments"""
        try:
            experiment_data = pd.DataFrame([{
                'metric_date': datetime.now().date(),
                'new_accounts': self.processed_metrics['account_growth']['new_accounts'],
                'cancelled_accounts': self.processed_metrics['account_growth']['cancelled_accounts'],
                'license_increases': self.processed_metrics['license_growth']['license_increases'],
                'revenue_expansions': self.processed_metrics['revenue_growth']['total_renewals'],
                'metric_type': 'daily_growth'
            }])
            
            experiment_data.to_sql('experiment_growth_metrics', self.db_engine, 
                                 if_exists='append', index=False)
            
            self.logger.info("Experiment growth metrics loaded successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to load experiment growth metrics: {e}")
            raise
    
    def _load_growth_trends(self):
        """Load growth trend analysis for business intelligence"""
        try:
            trends_data = pd.DataFrame([{
                'analysis_date': datetime.now().date(),
                'account_growth_trend': self.processed_metrics['account_growth']['net_growth'],
                'license_growth_trend': self.processed_metrics['license_growth']['total_additional_licenses'],
                'revenue_growth_trend': self.processed_metrics['revenue_growth']['revenue_increase'],
                'data_completeness': self.processed_metrics['data_completeness'],
                'analysis_type': 'weekly_trend'
            }])
            
            trends_data.to_sql('growth_trend_analysis', self.db_engine, 
                             if_exists='append', index=False)
            
            self.logger.info("Growth trend analysis loaded successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to load growth trend analysis: {e}")
            raise
    
    def get_growth_summary(self) -> Dict[str, Any]:
        """Get growth summary for monitoring and reporting"""
        if hasattr(self, 'processed_metrics'):
            return self.processed_metrics
        return {}
    
    def check_account_status_completeness(self) -> bool:
        """Check if all accounts have current status"""
        if not hasattr(self, 'processed_metrics'):
            return False
        
        completeness_threshold = self.pipeline_config.get('account_completeness_threshold', 1.0)
        current_completeness = self.processed_metrics['data_completeness']
        
        if current_completeness < completeness_threshold:
            self.logger.warning(f"Account status completeness below threshold: {current_completeness:.2%}")
            return False
        
        self.logger.info(f"Account status completeness check passed: {current_completeness:.2%}")
        return True
