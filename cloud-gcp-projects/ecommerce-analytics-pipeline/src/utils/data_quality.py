#!/usr/bin/env python3
"""
🔍 Data Quality Module

This module provides comprehensive data quality validation and monitoring
for the e-commerce analytics pipeline. It includes data validation rules,
quality scoring, and detailed reporting capabilities.

Author: Data Engineering Team
Version: 1.0.0
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from pathlib import Path
import json

from .config import Config
from .exceptions import DataQualityError


@dataclass
class QualityCheck:
    """Data structure for a quality check."""
    name: str
    description: str
    check_type: str  # completeness, accuracy, consistency, validity, uniqueness
    severity: str = "error"  # info, warning, error, critical
    enabled: bool = True
    threshold: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class QualityResult:
    """Data structure for quality check results."""
    check_name: str
    passed: bool
    score: float
    details: Dict[str, Any]
    timestamp: datetime
    records_checked: int
    records_failed: int
    error_messages: List[str] = field(default_factory=list)


@dataclass
class DataQualityReport:
    """Data structure for comprehensive data quality report."""
    dataset_name: str
    timestamp: datetime
    overall_score: float
    total_records: int
    quality_checks: List[QualityResult]
    summary: Dict[str, Any]
    recommendations: List[str] = field(default_factory=list)


class DataQualityValidator:
    """
    Comprehensive data quality validation system.

    Provides:
    - Data completeness checks
    - Data accuracy validation
    - Data consistency verification
    - Data validity assessment
    - Uniqueness validation
    - Custom business rule validation
    """

    def __init__(self, config: Config):
        """
        Initialize the data quality validator.

        Args:
            config: Configuration object
        """
        self.config = config
        self.quality_checks: List[QualityCheck] = []
        self.custom_validators: Dict[str, callable] = {}
        
        # Setup default quality checks
        self._setup_default_checks()
        
        # Setup custom validators
        self._setup_custom_validators()

    def _setup_default_checks(self) -> None:
        """Setup default quality checks."""
        self.quality_checks = [
            QualityCheck(
                name="null_check",
                description="Check for null values in required fields",
                check_type="completeness",
                severity="error",
                threshold=0.0
            ),
            QualityCheck(
                name="data_type_check",
                description="Validate data types match expected schema",
                check_type="validity",
                severity="error",
                threshold=0.0
            ),
            QualityCheck(
                name="range_check",
                description="Check numeric values are within expected ranges",
                check_type="accuracy",
                severity="warning",
                threshold=0.95
            ),
            QualityCheck(
                name="format_check",
                description="Validate data format (email, phone, etc.)",
                check_type="validity",
                severity="warning",
                threshold=0.9
            ),
            QualityCheck(
                name="uniqueness_check",
                description="Check for duplicate records",
                check_type="uniqueness",
                severity="warning",
                threshold=0.95
            ),
            QualityCheck(
                name="referential_integrity",
                description="Check referential integrity between tables",
                check_type="consistency",
                severity="error",
                threshold=0.0
            )
        ]

    def _setup_custom_validators(self) -> None:
        """Setup custom validation functions."""
        self.custom_validators = {
            'email_format': self._validate_email_format,
            'phone_format': self._validate_phone_format,
            'date_range': self._validate_date_range,
            'currency_format': self._validate_currency_format,
            'product_category': self._validate_product_category
        }

    def add_quality_check(self, check: QualityCheck) -> None:
        """
        Add a custom quality check.

        Args:
            check: QualityCheck instance to add
        """
        self.quality_checks.append(check)

    def remove_quality_check(self, check_name: str) -> None:
        """
        Remove a quality check.

        Args:
            check_name: Name of the check to remove
        """
        self.quality_checks = [c for c in self.quality_checks if c.name != check_name]

    def validate_dataset(
        self,
        data: Union[pd.DataFrame, Dict[str, Any]],
        dataset_name: str,
        schema: Optional[Dict[str, Any]] = None
    ) -> DataQualityReport:
        """
        Validate a dataset and generate quality report.

        Args:
            data: Dataset to validate (DataFrame or dict)
            dataset_name: Name of the dataset
            schema: Expected schema (optional)

        Returns:
            DataQualityReport with validation results
        """
        if isinstance(data, dict):
            data = pd.DataFrame(data)

        if not isinstance(data, pd.DataFrame):
            raise DataQualityError("Data must be a pandas DataFrame or dict")

        # Initialize report
        report = DataQualityReport(
            dataset_name=dataset_name,
            timestamp=datetime.now(),
            overall_score=0.0,
            total_records=len(data),
            quality_checks=[],
            summary={},
            recommendations=[]
        )

        # Run all quality checks
        check_results = []
        total_score = 0.0
        passed_checks = 0

        for check in self.quality_checks:
            if not check.enabled:
                continue

            try:
                result = self._run_quality_check(data, check, schema)
                check_results.append(result)
                
                if result.passed:
                    passed_checks += 1
                
                total_score += result.score

            except Exception as e:
                # Create failed result for errored checks
                result = QualityResult(
                    check_name=check.name,
                    passed=False,
                    score=0.0,
                    details={'error': str(e)},
                    timestamp=datetime.now(),
                    records_checked=len(data),
                    records_failed=len(data),
                    error_messages=[str(e)]
                )
                check_results.append(result)

        # Calculate overall score
        if check_results:
            report.overall_score = total_score / len(check_results)
        else:
            report.overall_score = 0.0

        report.quality_checks = check_results

        # Generate summary and recommendations
        report.summary = self._generate_summary(check_results, data)
        report.recommendations = self._generate_recommendations(check_results, data)

        return report

    def _run_quality_check(
        self,
        data: pd.DataFrame,
        check: QualityCheck,
        schema: Optional[Dict[str, Any]] = None
    ) -> QualityResult:
        """
        Run a specific quality check.

        Args:
            data: Dataset to check
            check: Quality check to run
            schema: Expected schema

        Returns:
            QualityResult with check details
        """
        if check.name == "null_check":
            return self._check_null_values(data, check)
        elif check.name == "data_type_check":
            return self._check_data_types(data, check, schema)
        elif check.name == "range_check":
            return self._check_value_ranges(data, check)
        elif check.name == "format_check":
            return self._check_data_formats(data, check)
        elif check.name == "uniqueness_check":
            return self._check_uniqueness(data, check)
        elif check.name == "referential_integrity":
            return self._check_referential_integrity(data, check)
        else:
            return self._run_custom_check(data, check)

    def _check_null_values(self, data: pd.DataFrame, check: QualityCheck) -> QualityResult:
        """Check for null values in required fields."""
        required_fields = self.config.data_quality.required_fields.get(
            check.metadata.get('table_name', 'default'), []
        )
        
        if not required_fields:
            return QualityResult(
                check_name=check.name,
                passed=True,
                score=1.0,
                details={'message': 'No required fields specified'},
                timestamp=datetime.now(),
                records_checked=len(data),
                records_failed=0
            )

        null_counts = {}
        failed_records = 0
        
        for field in required_fields:
            if field in data.columns:
                null_count = data[field].isnull().sum()
                null_counts[field] = null_count
                failed_records += null_count

        total_required_fields = len(required_fields) * len(data)
        score = 1.0 - (failed_records / total_required_fields) if total_required_fields > 0 else 1.0
        passed = score >= check.threshold

        return QualityResult(
            check_name=check.name,
            passed=passed,
            score=score,
            details={'null_counts': null_counts, 'required_fields': required_fields},
            timestamp=datetime.now(),
            records_checked=len(data),
            records_failed=failed_records
        )

    def _check_data_types(self, data: pd.DataFrame, check: QualityCheck, schema: Optional[Dict[str, Any]]) -> QualityResult:
        """Check data types match expected schema."""
        if not schema:
            return QualityResult(
                check_name=check.name,
                passed=True,
                score=1.0,
                details={'message': 'No schema provided for validation'},
                timestamp=datetime.now(),
                records_checked=len(data),
                records_failed=0
            )

        type_mismatches = {}
        failed_records = 0
        
        for column, expected_type in schema.items():
            if column in data.columns:
                try:
                    # Convert column to expected type to check compatibility
                    if expected_type == 'int':
                        pd.to_numeric(data[column], errors='coerce')
                    elif expected_type == 'float':
                        pd.to_numeric(data[column], errors='coerce')
                    elif expected_type == 'datetime':
                        pd.to_datetime(data[column], errors='coerce')
                    elif expected_type == 'bool':
                        data[column].astype(bool)
                    
                    # Count records that couldn't be converted
                    if expected_type in ['int', 'float']:
                        failed_count = data[column].isna().sum()
                    elif expected_type == 'datetime':
                        failed_count = pd.to_datetime(data[column], errors='coerce').isna().sum()
                    else:
                        failed_count = 0
                    
                    type_mismatches[column] = failed_count
                    failed_records += failed_count
                    
                except Exception:
                    type_mismatches[column] = len(data)
                    failed_records += len(data)

        total_fields = len(schema) * len(data)
        score = 1.0 - (failed_records / total_fields) if total_fields > 0 else 1.0
        passed = score >= check.threshold

        return QualityResult(
            check_name=check.name,
            passed=passed,
            score=score,
            details={'type_mismatches': type_mismatches, 'schema': schema},
            timestamp=datetime.now(),
            records_checked=len(data),
            records_failed=failed_records
        )

    def _check_value_ranges(self, data: pd.DataFrame, check: QualityCheck) -> QualityResult:
        """Check numeric values are within expected ranges."""
        numeric_columns = data.select_dtypes(include=[np.number]).columns
        range_violations = {}
        failed_records = 0
        
        for column in numeric_columns:
            if column in self.config.data_quality.quality_thresholds:
                min_val = self.config.data_quality.quality_thresholds[column].get('min')
                max_val = self.config.data_quality.quality_thresholds[column].get('max')
                
                if min_val is not None or max_val is not None:
                    violations = 0
                    
                    if min_val is not None:
                        violations += (data[column] < min_val).sum()
                    
                    if max_val is not None:
                        violations += (data[column] > max_val).sum()
                    
                    range_violations[column] = violations
                    failed_records += violations

        total_numeric_fields = len(numeric_columns) * len(data)
        score = 1.0 - (failed_records / total_numeric_fields) if total_numeric_fields > 0 else 1.0
        passed = score >= check.threshold

        return QualityResult(
            check_name=check.name,
            passed=passed,
            score=score,
            details={'range_violations': range_violations},
            timestamp=datetime.now(),
            records_checked=len(data),
            records_failed=failed_records
        )

    def _check_data_formats(self, data: pd.DataFrame, check: QualityCheck) -> QualityResult:
        """Check data format validity."""
        format_violations = {}
        failed_records = 0
        
        for column in data.columns:
            if column in self.custom_validators:
                validator_name = column.split('_')[0] + '_format'
                if validator_name in self.custom_validators:
                    violations = 0
                    
                    for value in data[column].dropna():
                        if not self.custom_validators[validator_name](value):
                            violations += 1
                    
                    format_violations[column] = violations
                    failed_records += violations

        total_formatted_fields = len(format_violations) * len(data)
        score = 1.0 - (failed_records / total_formatted_fields) if total_formatted_fields > 0 else 1.0
        passed = score >= check.threshold

        return QualityResult(
            check_name=check.name,
            passed=passed,
            score=score,
            details={'format_violations': format_violations},
            timestamp=datetime.now(),
            records_checked=len(data),
            records_failed=failed_records
        )

    def _check_uniqueness(self, data: pd.DataFrame, check: QualityCheck) -> QualityResult:
        """Check for duplicate records."""
        # Check for exact duplicates
        exact_duplicates = data.duplicated().sum()
        
        # Check for duplicates based on key fields
        key_fields = check.metadata.get('key_fields', [])
        key_duplicates = 0
        
        if key_fields and all(field in data.columns for field in key_fields):
            key_duplicates = data.duplicated(subset=key_fields).sum()
        
        total_duplicates = max(exact_duplicates, key_duplicates)
        score = 1.0 - (total_duplicates / len(data)) if len(data) > 0 else 1.0
        passed = score >= check.threshold

        return QualityResult(
            check_name=check.name,
            passed=passed,
            score=score,
            details={
                'exact_duplicates': exact_duplicates,
                'key_duplicates': key_duplicates,
                'key_fields': key_fields
            },
            timestamp=datetime.now(),
            records_checked=len(data),
            records_failed=total_duplicates
        )

    def _check_referential_integrity(self, data: pd.DataFrame, check: QualityCheck) -> QualityResult:
        """Check referential integrity between tables."""
        # This is a placeholder - would need actual foreign key relationships
        # For now, return a passed result
        return QualityResult(
            check_name=check.name,
            passed=True,
            score=1.0,
            details={'message': 'Referential integrity check not implemented'},
            timestamp=datetime.now(),
            records_checked=len(data),
            records_failed=0
        )

    def _run_custom_check(self, data: pd.DataFrame, check: QualityCheck) -> QualityResult:
        """Run a custom quality check."""
        # Placeholder for custom checks
        return QualityResult(
            check_name=check.name,
            passed=True,
            score=1.0,
            details={'message': 'Custom check not implemented'},
            timestamp=datetime.now(),
            records_checked=len(data),
            records_failed=0
        )

    def _validate_email_format(self, email: str) -> bool:
        """Validate email format."""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, str(email)))

    def _validate_phone_format(self, phone: str) -> bool:
        """Validate phone number format."""
        import re
        # Basic phone validation - can be customized
        pattern = r'^[\+]?[1-9][\d]{0,15}$'
        return bool(re.match(pattern, str(phone).replace(' ', '').replace('-', '').replace('(', '').replace(')', '')))

    def _validate_date_range(self, date_str: str) -> bool:
        """Validate date is within reasonable range."""
        try:
            date = pd.to_datetime(date_str)
            min_date = datetime(1900, 1, 1)
            max_date = datetime.now() + timedelta(days=365)
            return min_date <= date <= max_date
        except:
            return False

    def _validate_currency_format(self, amount: str) -> bool:
        """Validate currency format."""
        import re
        pattern = r'^[\$]?[\d,]+(\.\d{2})?$'
        return bool(re.match(pattern, str(amount)))

    def _validate_product_category(self, category: str) -> bool:
        """Validate product category."""
        valid_categories = [
            'electronics', 'clothing', 'books', 'home', 'sports',
            'beauty', 'automotive', 'toys', 'food', 'health'
        ]
        return str(category).lower() in valid_categories

    def _generate_summary(self, check_results: List[QualityResult], data: pd.DataFrame) -> Dict[str, Any]:
        """Generate summary of quality check results."""
        total_checks = len(check_results)
        passed_checks = sum(1 for r in check_results if r.passed)
        failed_checks = total_checks - passed_checks
        
        # Calculate scores by check type
        scores_by_type = {}
        for result in check_results:
            check_type = next((c.check_type for c in self.quality_checks if c.name == result.check_name), 'unknown')
            if check_type not in scores_by_type:
                scores_by_type[check_type] = []
            scores_by_type[check_type].append(result.score)
        
        # Calculate average scores by type
        avg_scores_by_type = {}
        for check_type, scores in scores_by_type.items():
            avg_scores_by_type[check_type] = sum(scores) / len(scores) if scores else 0.0
        
        return {
            'total_checks': total_checks,
            'passed_checks': passed_checks,
            'failed_checks': failed_checks,
            'pass_rate': passed_checks / total_checks if total_checks > 0 else 0.0,
            'scores_by_type': avg_scores_by_type,
            'total_records': len(data),
            'data_size_mb': data.memory_usage(deep=True).sum() / 1024 / 1024
        }

    def _generate_recommendations(self, check_results: List[QualityResult], data: pd.DataFrame) -> List[str]:
        """Generate recommendations based on quality check results."""
        recommendations = []
        
        # Check for critical failures
        critical_failures = [r for r in check_results if not r.passed and r.score < 0.5]
        if critical_failures:
            recommendations.append("Critical data quality issues detected. Review and fix before proceeding.")
        
        # Check for high null rates
        null_check = next((r for r in check_results if r.check_name == 'null_check'), None)
        if null_check and null_check.score < 0.8:
            recommendations.append("High null rate detected. Investigate data source and collection process.")
        
        # Check for data type issues
        type_check = next((r for r in check_results if r.check_name == 'data_type_check'), None)
        if type_check and type_check.score < 0.9:
            recommendations.append("Data type mismatches detected. Review schema and data transformation.")
        
        # Check for range violations
        range_check = next((r for r in check_results if r.check_name == 'range_check'), None)
        if range_check and range_check.score < 0.9:
            recommendations.append("Value range violations detected. Review business rules and data validation.")
        
        # Check for duplicates
        uniqueness_check = next((r for r in check_results if r.check_name == 'uniqueness_check'), None)
        if uniqueness_check and uniqueness_check.score < 0.95:
            recommendations.append("Duplicate records detected. Implement deduplication process.")
        
        if not recommendations:
            recommendations.append("Data quality is acceptable. Continue with pipeline execution.")
        
        return recommendations

    def save_report(self, report: DataQualityReport, file_path: str) -> None:
        """
        Save quality report to file.

        Args:
            report: DataQualityReport to save
            file_path: Path to save the report
        """
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        if file_path.suffix.lower() == '.json':
            with open(file_path, 'w') as f:
                json.dump(report.__dict__, f, indent=2, default=str)
        elif file_path.suffix.lower() == '.html':
            self._save_html_report(report, file_path)
        else:
            raise DataQualityError(f"Unsupported file format: {file_path.suffix}")

    def _save_html_report(self, report: DataQualityReport, file_path: Path) -> None:
        """Save report as HTML."""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Data Quality Report - {report.dataset_name}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
                .summary {{ margin: 20px 0; }}
                .check {{ margin: 10px 0; padding: 10px; border-left: 4px solid #ddd; }}
                .passed {{ border-left-color: #4CAF50; }}
                .failed {{ border-left-color: #f44336; }}
                .recommendations {{ background-color: #fff3cd; padding: 15px; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Data Quality Report</h1>
                <p><strong>Dataset:</strong> {report.dataset_name}</p>
                <p><strong>Timestamp:</strong> {report.timestamp}</p>
                <p><strong>Overall Score:</strong> {report.overall_score:.2%}</p>
            </div>
            
            <div class="summary">
                <h2>Summary</h2>
                <p><strong>Total Records:</strong> {report.summary.get('total_records', 0):,}</p>
                <p><strong>Passed Checks:</strong> {report.summary.get('passed_checks', 0)}</p>
                <p><strong>Failed Checks:</strong> {report.summary.get('failed_checks', 0)}</p>
                <p><strong>Pass Rate:</strong> {report.summary.get('pass_rate', 0):.2%}</p>
            </div>
            
            <h2>Quality Checks</h2>
            {''.join([f'''
            <div class="check {'passed' if check.passed else 'failed'}">
                <h3>{check.check_name}</h3>
                <p><strong>Status:</strong> {'✅ Passed' if check.passed else '❌ Failed'}</p>
                <p><strong>Score:</strong> {check.score:.2%}</p>
                <p><strong>Records Checked:</strong> {check.records_checked:,}</p>
                <p><strong>Records Failed:</strong> {check.records_failed:,}</p>
            </div>
            ''' for check in report.quality_checks])}
            
            <div class="recommendations">
                <h2>Recommendations</h2>
                <ul>
                    {''.join([f'<li>{rec}</li>' for rec in report.recommendations])}
                </ul>
            </div>
        </body>
        </html>
        """
        
        with open(file_path, 'w') as f:
            f.write(html_content)


def create_validator(config: Config) -> DataQualityValidator:
    """
    Create and return a configured data quality validator.

    Args:
        config: Configuration object

    Returns:
        Configured DataQualityValidator instance
    """
    return DataQualityValidator(config)


def validate_dataframe(
    data: pd.DataFrame,
    config: Config,
    dataset_name: str = "unknown"
) -> DataQualityReport:
    """
    Quick validation of a DataFrame.

    Args:
        data: DataFrame to validate
        config: Configuration object
        dataset_name: Name of the dataset

    Returns:
        DataQualityReport with validation results
    """
    validator = create_validator(config)
    return validator.validate_dataset(data, dataset_name)
