#!/usr/bin/env python3
"""
🛒 E-commerce Analytics Pipeline - Main Entry Point

This module orchestrates the complete ETL pipeline for e-commerce data analytics
using Google Cloud Platform services.

Author: Data Engineering Team
Version: 1.0.0
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import Dict, Any

# Add src to path for imports
sys.path.append(str(Path(__file__).parent))

from utils.config import Config
from utils.logger import setup_logger
from extractors.data_extractor import DataExtractor
from transformers.data_transformer import DataTransformer
from loaders.data_loader import DataLoader
from utils.monitoring import PipelineMonitor
from utils.exceptions import PipelineError


class EcommerceETLPipeline:
    """
    Main ETL Pipeline class for e-commerce analytics.
    
    Orchestrates data extraction, transformation, and loading processes
    using GCP services including Cloud Storage, BigQuery, and Dataflow.
    """
    
    def __init__(self, config: Config):
        """
        Initialize the ETL pipeline.
        
        Args:
            config: Configuration object containing pipeline settings
        """
        self.config = config
        self.logger = setup_logger(__name__)
        self.monitor = PipelineMonitor()
        
        # Initialize pipeline components
        self.extractor = DataExtractor(config)
        self.transformer = DataTransformer(config)
        self.loader = DataLoader(config)
        
        self.logger.info("🚀 E-commerce ETL Pipeline initialized successfully")
    
    def run(self) -> Dict[str, Any]:
        """
        Execute the complete ETL pipeline.
        
        Returns:
            Dictionary containing pipeline execution results and metrics
        """
        try:
            self.logger.info("🔄 Starting E-commerce ETL Pipeline execution")
            self.monitor.start_pipeline()
            
            # Phase 1: Data Extraction
            self.logger.info("📥 Phase 1: Data Extraction")
            raw_data = self.extract_data()
            
            # Phase 2: Data Transformation
            self.logger.info("🔄 Phase 2: Data Transformation")
            processed_data = self.transform_data(raw_data)
            
            # Phase 3: Data Loading
            self.logger.info("📤 Phase 3: Data Loading")
            load_results = self.load_data(processed_data)
            
            # Pipeline completion
            self.monitor.complete_pipeline()
            results = self.monitor.get_pipeline_results()
            
            self.logger.info("✅ E-commerce ETL Pipeline completed successfully")
            return results
            
        except Exception as e:
            self.logger.error(f"❌ Pipeline execution failed: {str(e)}")
            self.monitor.fail_pipeline(str(e))
            raise PipelineError(f"Pipeline execution failed: {str(e)}")
    
    def extract_data(self) -> Dict[str, Any]:
        """
        Extract data from various sources.
        
        Returns:
            Dictionary containing extracted data from different sources
        """
        try:
            self.logger.info("📥 Extracting data from multiple sources...")
            
            # Extract customer orders data
            customer_orders = self.extractor.extract_customer_orders()
            self.logger.info(f"✅ Extracted {len(customer_orders)} customer orders")
            
            # Extract product catalog data
            product_catalog = self.extractor.extract_product_catalog()
            self.logger.info(f"✅ Extracted {len(product_catalog)} products")
            
            # Extract web analytics data
            web_analytics = self.extractor.extract_web_analytics()
            self.logger.info(f"✅ Extracted web analytics data")
            
            # Extract inventory data
            inventory_data = self.extractor.extract_inventory_data()
            self.logger.info(f"✅ Extracted inventory data")
            
            raw_data = {
                'customer_orders': customer_orders,
                'product_catalog': product_catalog,
                'web_analytics': web_analytics,
                'inventory_data': inventory_data
            }
            
            self.monitor.record_extraction_metrics(raw_data)
            return raw_data
            
        except Exception as e:
            self.logger.error(f"❌ Data extraction failed: {str(e)}")
            raise PipelineError(f"Data extraction failed: {str(e)}")
    
    def transform_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform and clean the extracted data.
        
        Args:
            raw_data: Raw data extracted from various sources
            
        Returns:
            Dictionary containing transformed and cleaned data
        """
        try:
            self.logger.info("🔄 Transforming and cleaning data...")
            
            # Transform customer orders
            transformed_orders = self.transformer.transform_customer_orders(
                raw_data['customer_orders']
            )
            self.logger.info(f"✅ Transformed {len(transformed_orders)} customer orders")
            
            # Transform product catalog
            transformed_products = self.transformer.transform_product_catalog(
                raw_data['product_catalog']
            )
            self.logger.info(f"✅ Transformed {len(transformed_products)} products")
            
            # Transform web analytics
            transformed_analytics = self.transformer.transform_web_analytics(
                raw_data['web_analytics']
            )
            self.logger.info("✅ Transformed web analytics data")
            
            # Transform inventory data
            transformed_inventory = self.transformer.transform_inventory_data(
                raw_data['inventory_data']
            )
            self.logger.info("✅ Transformed inventory data")
            
            # Create business metrics and aggregations
            business_metrics = self.transformer.create_business_metrics(
                transformed_orders, transformed_products, transformed_inventory
            )
            self.logger.info("✅ Created business metrics and aggregations")
            
            processed_data = {
                'customer_orders': transformed_orders,
                'product_catalog': transformed_products,
                'web_analytics': transformed_analytics,
                'inventory_data': transformed_inventory,
                'business_metrics': business_metrics
            }
            
            self.monitor.record_transformation_metrics(processed_data)
            return processed_data
            
        except Exception as e:
            self.logger.error(f"❌ Data transformation failed: {str(e)}")
            raise PipelineError(f"Data transformation failed: {str(e)}")
    
    def load_data(self, processed_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Load transformed data into target systems.
        
        Args:
            processed_data: Transformed and cleaned data
            
        Returns:
            Dictionary containing loading results and metrics
        """
        try:
            self.logger.info("📤 Loading data into target systems...")
            
            # Load raw data to Cloud Storage
            raw_storage_results = self.loader.load_raw_data(processed_data)
            self.logger.info("✅ Loaded raw data to Cloud Storage")
            
            # Load processed data to BigQuery
            bigquery_results = self.loader.load_to_bigquery(processed_data)
            self.logger.info("✅ Loaded data to BigQuery")
            
            # Create curated datasets
            curated_results = self.loader.create_curated_datasets(processed_data)
            self.logger.info("✅ Created curated datasets")
            
            # Update data catalog and metadata
            catalog_results = self.loader.update_data_catalog(processed_data)
            self.logger.info("✅ Updated data catalog and metadata")
            
            load_results = {
                'raw_storage': raw_storage_results,
                'bigquery': bigquery_results,
                'curated': curated_results,
                'catalog': catalog_results
            }
            
            self.monitor.record_loading_metrics(load_results)
            return load_results
            
        except Exception as e:
            self.logger.error(f"❌ Data loading failed: {str(e)}")
            raise PipelineError(f"Data loading failed: {str(e)}")
    
    def validate_pipeline(self) -> bool:
        """
        Validate pipeline configuration and dependencies.
        
        Returns:
            True if validation passes, False otherwise
        """
        try:
            self.logger.info("🔍 Validating pipeline configuration...")
            
            # Validate GCP credentials and permissions
            gcp_valid = self.extractor.validate_gcp_access()
            if not gcp_valid:
                self.logger.error("❌ GCP access validation failed")
                return False
            
            # Validate data sources
            sources_valid = self.extractor.validate_data_sources()
            if not sources_valid:
                self.logger.error("❌ Data sources validation failed")
                return False
            
            # Validate target systems
            targets_valid = self.loader.validate_target_systems()
            if not targets_valid:
                self.logger.error("❌ Target systems validation failed")
                return False
            
            self.logger.info("✅ Pipeline validation completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Pipeline validation failed: {str(e)}")
            return False


def main():
    """Main entry point for the ETL pipeline."""
    parser = argparse.ArgumentParser(
        description="E-commerce Analytics ETL Pipeline"
    )
    parser.add_argument(
        "--env", 
        default="dev",
        choices=["dev", "staging", "prod"],
        help="Environment to run the pipeline in"
    )
    parser.add_argument(
        "--config", 
        default="config/environments/config.yaml",
        help="Path to configuration file"
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only validate pipeline configuration without execution"
    )
    
    args = parser.parse_args()
    
    try:
        # Load configuration
        config = Config(env=args.env, config_path=args.config)
        
        # Initialize pipeline
        pipeline = EcommerceETLPipeline(config)
        
        if args.validate_only:
            # Only validate pipeline
            if pipeline.validate_pipeline():
                print("✅ Pipeline validation passed")
                sys.exit(0)
            else:
                print("❌ Pipeline validation failed")
                sys.exit(1)
        
        # Run pipeline
        results = pipeline.run()
        
        # Print results summary
        print("\n" + "="*50)
        print("🎉 PIPELINE EXECUTION COMPLETED SUCCESSFULLY")
        print("="*50)
        print(f"📊 Records Processed: {results.get('total_records', 'N/A')}")
        print(f"⏱️  Execution Time: {results.get('execution_time', 'N/A')}")
        print(f"💾 Data Quality Score: {results.get('data_quality_score', 'N/A')}")
        print(f"📈 Success Rate: {results.get('success_rate', 'N/A')}")
        print("="*50)
        
    except Exception as e:
        print(f"❌ Pipeline execution failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
