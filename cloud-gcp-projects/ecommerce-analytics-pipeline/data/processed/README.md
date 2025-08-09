# Processed Data Directory

This directory contains data that has been cleaned, transformed, and prepared for analysis.

## Purpose

Processed data files are the output of the **Transform** stage of the pipeline. They contain data that has been:
- Cleaned and standardized
- Transformed according to business rules
- Validated for quality
- Prepared for loading into the data warehouse

## Directory Structure

```
processed/
├── README.md                    # This documentation
├── .gitkeep                     # Keeps directory in git
├── orders/                      # Processed order data
│   ├── orders_cleaned_2024_01.parquet
│   ├── orders_cleaned_2024_02.parquet
│   └── orders_cleaned_2024_03.parquet
├── products/                    # Processed product data
│   ├── products_standardized.parquet
│   └── product_hierarchy.json
├── customers/                   # Processed customer data
│   ├── customers_enriched.parquet
│   └── customer_lifetime_value.csv
├── transactions/                # Processed transaction data
│   ├── transactions_aggregated_2024_01.parquet
│   ├── transactions_aggregated_2024_02.parquet
│   └── transactions_aggregated_2024_03.parquet
├── analytics/                   # Analytical datasets
│   ├── daily_sales_summary.parquet
│   ├── customer_segmentation.parquet
│   └── product_performance.csv
└── staging/                     # Staging data for loading
    ├── orders_staging.parquet
    ├── products_staging.parquet
    └── customers_staging.parquet
```

## Data Processing Steps

### 1. Data Cleaning
- Remove duplicates and invalid records
- Handle missing values
- Standardize data formats
- Fix encoding issues

### 2. Data Transformation
- Apply business rules and calculations
- Create derived fields
- Aggregate data at different levels
- Normalize data structures

### 3. Data Validation
- Check data quality rules
- Validate business constraints
- Ensure referential integrity
- Generate quality reports

### 4. Data Preparation
- Optimize for analysis
- Create analytical views
- Prepare for loading into BigQuery
- Generate metadata

## File Formats

Processed data is primarily stored in:
- **Parquet**: For large analytical datasets (compressed, columnar)
- **CSV**: For smaller datasets and human readability
- **JSON**: For complex nested data structures

## Data Quality Metrics

Each processed dataset includes:
- **Record count**: Total number of records
- **Quality score**: Overall data quality rating
- **Processing timestamp**: When the data was processed
- **Validation results**: Summary of quality checks
- **Error logs**: Any issues encountered during processing

## Monitoring

The pipeline tracks:
- **Processing time**: How long each transformation takes
- **Data volume**: Number of records processed
- **Quality metrics**: Validation results and scores
- **Error rates**: Failed transformations and reasons

## Next Steps

Processed data files are loaded by the **Load** stage into:
- **BigQuery tables**: For analytical queries
- **Cloud Storage**: For backup and archival
- **Data Lake**: For long-term storage
- **Analytics tools**: For business intelligence

## File Naming Convention

Use descriptive names with processing details:
- `{data_type}_{processing_step}_{YYYY}_{MM}.{extension}`
- `{data_type}_{processing_step}_v{version}.{extension}`

Examples:
- `orders_cleaned_2024_01.parquet`
- `products_standardized_v2.parquet`
- `transactions_aggregated_2024_01.parquet`
