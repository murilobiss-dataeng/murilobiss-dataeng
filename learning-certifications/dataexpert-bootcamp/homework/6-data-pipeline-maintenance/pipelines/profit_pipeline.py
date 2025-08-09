"""
Profit Pipeline for TechFlow Solutions
Calculates profit metrics and unit-level profitability for experiments and investor reporting
"""

import logging
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from .base_pipeline import BasePipeline
from .config import config

class ProfitPipeline(BasePipeline):
    """Pipeline for calculating profit metrics and unit-level profitability"""
    
    def __init__(self):
        super().__init__("Profit")
        self.db_engine = None
        self.revenue_data = None
        self.expense_data = None
        self.salary_data = None
        
    def _execute(self) -> bool:
        """Execute profit pipeline"""
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
            self.logger.error(f"Profit pipeline execution failed: {e}")
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
        """Extract revenue, expense, and salary data"""
        try:
            # Extract revenue data
            revenue_query = """
                SELECT 
                    account_id,
                    subscription_tier,
                    monthly_revenue,
                    user_licenses,
                    additional_features,
                    feature_revenue,
                    total_monthly_revenue,
                    billing_date,
                    payment_status
                FROM revenue_accounts 
                WHERE billing_date >= CURRENT_DATE - INTERVAL '1 month'
                AND payment_status = 'Paid'
            """
            
            self.revenue_data = pd.read_sql(revenue_query, self.db_engine)
            self.logger.info(f"Extracted {len(self.revenue_data)} revenue records")
            
            # Extract expense data
            expense_query = """
                SELECT 
                    account_id,
                    expense_category,
                    monthly_cost,
                    cost_breakdown,
                    expense_date
                FROM operational_expenses 
                WHERE expense_date >= CURRENT_DATE - INTERVAL '1 month'
            """
            
            self.expense_data = pd.read_sql(expense_query, self.db_engine)
            self.logger.info(f"Extracted {len(self.expense_data)} expense records")
            
            # Extract salary data
            salary_query = """
                SELECT 
                    team_id,
                    team_name,
                    monthly_salary_total,
                    headcount,
                    cost_per_engineer,
                    salary_month
                FROM team_salaries 
                WHERE salary_month >= CURRENT_DATE - INTERVAL '1 month'
            """
            
            self.salary_data = pd.read_sql(salary_query, self.db_engine)
            self.logger.info(f"Extracted {len(self.salary_data)} salary records")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Data extraction failed: {e}")
            return False
    
    def _validate_data(self) -> bool:
        """Validate extracted data"""
        try:
            # Check data completeness
            if self.revenue_data.empty:
                self.logger.error("No revenue data found")
                return False
            
            if self.expense_data.empty:
                self.logger.error("No expense data found")
                return False
            
            if self.salary_data.empty:
                self.logger.error("No salary data found")
                return False
            
            # Validate revenue data
            revenue_validation = self._validate_revenue_data()
            if not revenue_validation:
                return False
            
            # Validate expense data
            expense_validation = self._validate_expense_data()
            if not expense_validation:
                return False
            
            # Validate salary data
            salary_validation = self._validate_salary_data()
            if not salary_validation:
                return False
            
            self.logger.info("Data validation completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Data validation failed: {e}")
            return False
    
    def _validate_revenue_data(self) -> bool:
        """Validate revenue data quality"""
        try:
            # Check for missing values
            missing_values = self.revenue_data.isnull().sum()
            if missing_values.sum() > 0:
                self.logger.warning(f"Revenue data has missing values: {missing_values.to_dict()}")
            
            # Check for negative revenue
            negative_revenue = self.revenue_data[self.revenue_data['total_monthly_revenue'] < 0]
            if not negative_revenue.empty:
                self.logger.error(f"Found {len(negative_revenue)} records with negative revenue")
                return False
            
            # Check revenue calculation consistency
            calculated_revenue = self.revenue_data['monthly_revenue'] + self.revenue_data['feature_revenue']
            revenue_mismatch = abs(calculated_revenue - self.revenue_data['total_monthly_revenue']) > 0.01
            if revenue_mismatch.any():
                self.logger.error("Revenue calculation mismatch detected")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Revenue validation failed: {e}")
            return False
    
    def _validate_expense_data(self) -> bool:
        """Validate expense data quality"""
        try:
            # Check for missing values
            missing_values = self.expense_data.isnull().sum()
            if missing_values.sum() > 0:
                self.logger.warning(f"Expense data has missing values: {missing_values.to_dict()}")
            
            # Check for negative expenses
            negative_expenses = self.expense_data[self.expense_data['monthly_cost'] < 0]
            if not negative_expenses.empty:
                self.logger.error(f"Found {len(negative_expenses)} records with negative expenses")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Expense validation failed: {e}")
            return False
    
    def _validate_salary_data(self) -> bool:
        """Validate salary data quality"""
        try:
            # Check for missing values
            missing_values = self.salary_data.isnull().sum()
            if missing_values.sum() > 0:
                self.logger.warning(f"Salary data has missing values: {missing_values.to_dict()}")
            
            # Check salary calculation consistency
            calculated_salary = self.salary_data['cost_per_engineer'] * self.salary_data['headcount']
            salary_mismatch = abs(calculated_salary - self.salary_data['monthly_salary_total']) > 0.01
            if salary_mismatch.any():
                self.logger.error("Salary calculation mismatch detected")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Salary validation failed: {e}")
            return False
    
    def _process_data(self) -> bool:
        """Process data to calculate profit metrics"""
        try:
            # Calculate total revenue
            total_revenue = self.revenue_data['total_monthly_revenue'].sum()
            self.logger.info(f"Total monthly revenue: ${total_revenue:,.2f}")
            
            # Calculate total expenses
            total_expenses = self.expense_data['monthly_cost'].sum()
            self.logger.info(f"Total monthly expenses: ${total_expenses:,.2f}")
            
            # Calculate total salary costs
            total_salaries = self.salary_data['monthly_salary_total'].sum()
            self.logger.info(f"Total monthly salaries: ${total_salaries:,.2f}")
            
            # Calculate total costs
            total_costs = total_expenses + total_salaries
            
            # Calculate profit
            profit = total_revenue - total_costs
            self.logger.info(f"Monthly profit: ${profit:,.2f}")
            
            # Calculate unit-level profit
            total_subscribers = self.revenue_data['user_licenses'].sum()
            unit_profit = profit / total_subscribers if total_subscribers > 0 else 0
            self.logger.info(f"Unit-level profit: ${unit_profit:.2f}")
            
            # Store processed metrics
            self.processed_metrics = {
                'total_revenue': total_revenue,
                'total_expenses': total_expenses,
                'total_salaries': total_salaries,
                'total_costs': total_costs,
                'profit': profit,
                'total_subscribers': total_subscribers,
                'unit_profit': unit_profit,
                'profit_margin': (profit / total_revenue) * 100 if total_revenue > 0 else 0,
                'processing_date': datetime.now().isoformat()
            }
            
            # Update metrics
            self.metrics.records_processed = len(self.revenue_data) + len(self.expense_data) + len(self.salary_data)
            
            self.logger.info("Data processing completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Data processing failed: {e}")
            return False
    
    def _load_data(self) -> bool:
        """Load processed profit metrics to destination tables"""
        try:
            # Load aggregate profit metrics for investors
            self._load_investor_metrics()
            
            # Load unit-level profit metrics for experiments
            self._load_experiment_metrics()
            
            # Load detailed profit breakdown
            self._load_profit_breakdown()
            
            self.logger.info("Data loading completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Data loading failed: {e}")
            return False
    
    def _load_investor_metrics(self):
        """Load aggregate profit metrics for investor reporting"""
        try:
            investor_data = pd.DataFrame([{
                'report_date': datetime.now().date(),
                'total_revenue': self.processed_metrics['total_revenue'],
                'total_costs': self.processed_metrics['total_costs'],
                'profit': self.processed_metrics['profit'],
                'profit_margin': self.processed_metrics['profit_margin'],
                'report_type': 'monthly_investor'
            }])
            
            investor_data.to_sql('investor_profit_metrics', self.db_engine, 
                               if_exists='append', index=False)
            
            self.logger.info("Investor metrics loaded successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to load investor metrics: {e}")
            raise
    
    def _load_experiment_metrics(self):
        """Load unit-level profit metrics for data science experiments"""
        try:
            experiment_data = pd.DataFrame([{
                'metric_date': datetime.now().date(),
                'unit_profit': self.processed_metrics['unit_profit'],
                'total_subscribers': self.processed_metrics['total_subscribers'],
                'cost_per_account': self.processed_metrics['total_costs'] / self.processed_metrics['total_subscribers'],
                'metric_type': 'unit_profitability'
            }])
            
            experiment_data.to_sql('experiment_profit_metrics', self.db_engine, 
                                 if_exists='append', index=False)
            
            self.logger.info("Experiment metrics loaded successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to load experiment metrics: {e}")
            raise
    
    def _load_profit_breakdown(self):
        """Load detailed profit breakdown for analysis"""
        try:
            breakdown_data = pd.DataFrame([{
                'breakdown_date': datetime.now().date(),
                'revenue_breakdown': {
                    'subscription_revenue': self.revenue_data['monthly_revenue'].sum(),
                    'feature_revenue': self.revenue_data['feature_revenue'].sum()
                },
                'expense_breakdown': {
                    'operational_expenses': self.processed_metrics['total_expenses'],
                    'salary_costs': self.processed_metrics['total_salaries']
                },
                'profit_analysis': {
                    'gross_profit': self.processed_metrics['total_revenue'] - self.processed_metrics['total_expenses'],
                    'net_profit': self.processed_metrics['profit']
                }
            }])
            
            breakdown_data.to_sql('profit_breakdown', self.db_engine, 
                                if_exists='append', index=False)
            
            self.logger.info("Profit breakdown loaded successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to load profit breakdown: {e}")
            raise
    
    def get_profit_summary(self) -> Dict[str, Any]:
        """Get profit summary for monitoring and reporting"""
        if hasattr(self, 'processed_metrics'):
            return self.processed_metrics
        return {}
    
    def check_revenue_accuracy(self, accounting_system_revenue: float) -> bool:
        """Check if pipeline revenue matches accounting system"""
        if not hasattr(self, 'processed_metrics'):
            return False
        
        pipeline_revenue = self.processed_metrics['total_revenue']
        tolerance = self.pipeline_config.get('revenue_tolerance', 0.01)
        
        difference = abs(pipeline_revenue - accounting_system_revenue)
        accuracy = difference / accounting_system_revenue
        
        if accuracy > tolerance:
            self.logger.warning(f"Revenue accuracy check failed: {accuracy:.2%} difference")
            return False
        
        self.logger.info(f"Revenue accuracy check passed: {accuracy:.2%} difference")
        return True
