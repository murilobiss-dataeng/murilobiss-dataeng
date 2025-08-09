#!/usr/bin/env python3
"""
Test Runner Script for E-commerce Analytics Pipeline

This script executes the test suite for the pipeline components.
It can run unit tests, integration tests, and custom test scenarios.

Usage:
    python run_tests.py [--type TYPE] [--verbose] [--output FILE]

Options:
    --type TYPE      Type of tests to run (unit, integration, all)
    --verbose        Enable verbose output
    --output FILE    Save test results to file
"""

import argparse
import sys
import os
import subprocess
import json
from datetime import datetime
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from utils.logger import PipelineLogger
from utils.config import Config


class TestRunner:
    """Manages test execution and reporting."""
    
    def __init__(self, config: Config = None):
        """Initialize test runner."""
        self.config = config or Config()
        self.logger = PipelineLogger("test_runner")
        self.test_results = []
        
    def run_unit_tests(self, verbose: bool = False) -> dict:
        """Run unit tests for all modules."""
        self.logger.info("Running unit tests...")
        
        results = {
            "type": "unit",
            "start_time": datetime.now().isoformat(),
            "tests": [],
            "summary": {"passed": 0, "failed": 0, "total": 0}
        }
        
        # Test core utility modules
        modules_to_test = [
            "utils.config",
            "utils.logger", 
            "utils.monitoring",
            "utils.data_quality",
            "utils.helpers",
            "utils.database",
            "utils.data_processing"
        ]
        
        for module in modules_to_test:
            try:
                # Test module import
                __import__(module)
                test_result = {
                    "module": module,
                    "status": "PASSED",
                    "message": "Module imported successfully"
                }
                results["summary"]["passed"] += 1
            except Exception as e:
                test_result = {
                    "module": module,
                    "status": "FAILED",
                    "message": str(e)
                }
                results["summary"]["failed"] += 1
            
            results["tests"].append(test_result)
            results["summary"]["total"] += 1
            
            if verbose:
                self.logger.info(f"{module}: {test_result['status']}")
        
        results["end_time"] = datetime.now().isoformat()
        return results
    
    def run_integration_tests(self, verbose: bool = False) -> dict:
        """Run integration tests for pipeline components."""
        self.logger.info("Running integration tests...")
        
        results = {
            "type": "integration",
            "start_time": datetime.now().isoformat(),
            "tests": [],
            "summary": {"passed": 0, "failed": 0, "total": 0}
        }
        
        # Test pipeline component integration
        integration_tests = [
            ("config_loading", self._test_config_loading),
            ("logger_setup", self._test_logger_setup),
            ("monitoring_basic", self._test_monitoring_basic),
            ("data_quality_basic", self._test_data_quality_basic)
        ]
        
        for test_name, test_func in integration_tests:
            try:
                test_result = test_func()
                test_result["test"] = test_name
                results["tests"].append(test_result)
                
                if test_result["status"] == "PASSED":
                    results["summary"]["passed"] += 1
                else:
                    results["summary"]["failed"] += 1
                    
                results["summary"]["total"] += 1
                
                if verbose:
                    self.logger.info(f"{test_name}: {test_result['status']}")
                    
            except Exception as e:
                test_result = {
                    "test": test_name,
                    "status": "FAILED",
                    "message": f"Test execution failed: {str(e)}"
                }
                results["tests"].append(test_result)
                results["summary"]["failed"] += 1
                results["summary"]["total"] += 1
        
        results["end_time"] = datetime.now().isoformat()
        return results
    
    def _test_config_loading(self) -> dict:
        """Test configuration loading functionality."""
        try:
            config = Config()
            return {
                "status": "PASSED",
                "message": "Configuration loaded successfully"
            }
        except Exception as e:
            return {
                "status": "FAILED",
                "message": f"Configuration loading failed: {str(e)}"
            }
    
    def _test_logger_setup(self) -> dict:
        """Test logger setup functionality."""
        try:
            logger = PipelineLogger("test_logger")
            logger.info("Test log message")
            return {
                "status": "PASSED",
                "message": "Logger setup successful"
            }
        except Exception as e:
            return {
                "status": "FAILED",
                "message": f"Logger setup failed: {str(e)}"
            }
    
    def _test_monitoring_basic(self) -> dict:
        """Test basic monitoring functionality."""
        try:
            from utils.monitoring import PipelineMonitor
            monitor = PipelineMonitor(self.config)
            return {
                "status": "PASSED",
                "message": "Monitoring setup successful"
            }
        except Exception as e:
            return {
                "status": "FAILED",
                "message": f"Monitoring setup failed: {str(e)}"
            }
    
    def _test_data_quality_basic(self) -> dict:
        """Test basic data quality functionality."""
        try:
            from utils.data_quality import DataQualityValidator
            validator = DataQualityValidator()
            return {
                "status": "PASSED",
                "message": "Data quality validator setup successful"
            }
        except Exception as e:
            return {
                "status": "FAILED",
                "message": f"Data quality validator setup failed: {str(e)}"
            }
    
    def run_all_tests(self, verbose: bool = False) -> dict:
        """Run all test types."""
        self.logger.info("Running complete test suite...")
        
        unit_results = self.run_unit_tests(verbose)
        integration_results = self.run_integration_tests(verbose)
        
        # Combine results
        combined_results = {
            "test_suite": "ecommerce_analytics_pipeline",
            "run_time": datetime.now().isoformat(),
            "unit_tests": unit_results,
            "integration_tests": integration_results,
            "overall_summary": {
                "total_tests": unit_results["summary"]["total"] + integration_results["summary"]["total"],
                "total_passed": unit_results["summary"]["passed"] + integration_results["summary"]["passed"],
                "total_failed": unit_results["summary"]["failed"] + integration_results["summary"]["failed"]
            }
        }
        
        return combined_results
    
    def save_results(self, results: dict, output_file: str):
        """Save test results to file."""
        try:
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2)
            self.logger.info(f"Test results saved to {output_file}")
        except Exception as e:
            self.logger.error(f"Failed to save results: {str(e)}")
    
    def print_summary(self, results: dict):
        """Print test summary to console."""
        if "overall_summary" in results:
            # Combined results
            summary = results["overall_summary"]
            print(f"\n{'='*60}")
            print(f"TEST SUITE SUMMARY")
            print(f"{'='*60}")
            print(f"Total Tests: {summary['total_tests']}")
            print(f"Passed: {summary['total_passed']}")
            print(f"Failed: {summary['total_failed']}")
            print(f"Success Rate: {(summary['total_passed']/summary['total_tests']*100):.1f}%")
        else:
            # Single test type results
            summary = results["summary"]
            print(f"\n{'='*40}")
            print(f"{results['type'].upper()} TESTS SUMMARY")
            print(f"{'='*40}")
            print(f"Total: {summary['total']}")
            print(f"Passed: {summary['passed']}")
            print(f"Failed: {summary['failed']}")
            print(f"Success Rate: {(summary['passed']/summary['total']*100):.1f}%")


def main():
    """Main entry point for test runner."""
    parser = argparse.ArgumentParser(description="Run pipeline tests")
    parser.add_argument("--type", choices=["unit", "integration", "all"], 
                       default="all", help="Type of tests to run")
    parser.add_argument("--verbose", action="store_true", 
                       help="Enable verbose output")
    parser.add_argument("--output", help="Output file for test results")
    
    args = parser.parse_args()
    
    try:
        # Initialize test runner
        runner = TestRunner()
        
        # Run tests based on type
        if args.type == "unit":
            results = runner.run_unit_tests(args.verbose)
        elif args.type == "integration":
            results = runner.run_integration_tests(args.verbose)
        else:  # all
            results = runner.run_all_tests(args.verbose)
        
        # Print summary
        runner.print_summary(results)
        
        # Save results if output file specified
        if args.output:
            runner.save_results(results, args.output)
        
        # Exit with appropriate code
        if "overall_summary" in results:
            failed = results["overall_summary"]["total_failed"]
        else:
            failed = results["summary"]["failed"]
        
        sys.exit(1 if failed > 0 else 0)
        
    except Exception as e:
        print(f"Test runner failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
