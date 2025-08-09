# Raw Data Directory

This directory contains the raw, unprocessed data files that are ingested into the pipeline.

## Purpose

Raw data files are the original data sources that have not been transformed, cleaned, or processed in any way. They serve as the starting point for all data processing workflows.

## Directory Structure

```
raw/
├── README.md                    # This documentation
├── .gitkeep                     # Keeps directory in git
├── orders/                      # Order-related data
│   ├── orders_2024_01.csv
│   ├── orders_2024_02.csv
│   └── orders_2024_03.csv
├── products/                    # Product catalog data
│   ├── products_catalog.json
│   └── product_categories.csv
├── customers/                   # Customer information
│   ├── customers.csv
│   └── customer_segments.json
├── transactions/                # Transaction logs
│   ├── transactions_2024_01.parquet
│   ├── transactions_2024_02.parquet
│   └── transactions_2024_03.parquet
└── external/                    # External data sources
    ├── market_data.csv
    └── competitor_prices.json
```

## Data Formats

The pipeline supports the following data formats:
- **CSV**: Comma-separated values
- **JSON**: JavaScript Object Notation
- **Parquet**: Columnar storage format
- **Avro**: Row-based storage format
- **Excel**: Microsoft Excel files (.xlsx, .xls)

## Data Sources

### Internal Sources
- **E-commerce Platform**: Orders, products, customers
- **Payment Gateway**: Transaction logs
- **CRM System**: Customer data and interactions
- **Inventory System**: Stock levels and movements

### External Sources
- **Market Data**: Industry benchmarks and trends
- **Competitor Analysis**: Pricing and product information
- **Economic Indicators**: GDP, inflation, currency rates

## Data Quality Requirements

Raw data should meet these basic requirements:
- **Completeness**: All required fields are present
- **Format**: Data follows expected structure
- **Encoding**: UTF-8 encoding for text data
- **Timestamps**: Consistent date/time format

## File Naming Convention

Use descriptive names with dates:
- `{data_type}_{YYYY}_{MM}.{extension}`
- `{data_type}_{YYYY}_{MM}_{DD}.{extension}`
- `{data_type}_v{version}.{extension}`

Examples:
- `orders_2024_01.csv`
- `transactions_2024_01_15.parquet`
- `products_catalog_v2.json`

## Monitoring

The pipeline monitors:
- **File arrival**: New files detected
- **File size**: Unexpected size changes
- **File format**: Schema validation
- **Data freshness**: Age of latest data

## Next Steps

Raw data files are processed by the **Extract** stage of the pipeline, which:
1. Reads the data files
2. Validates basic structure
3. Loads into staging tables
4. Triggers transformation workflows
