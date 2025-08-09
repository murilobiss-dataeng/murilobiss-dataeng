# 🛒 E-commerce Analytics Pipeline - GCP

**End-to-End ETL Pipeline for E-commerce Data Analytics using Google Cloud Platform**

## 🎯 Project Overview

This project implements a comprehensive data pipeline for e-commerce analytics using GCP services. The pipeline processes customer orders, product data, and web analytics to provide actionable business insights.

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Sources  │    │   Processing    │    │   Analytics     │
│                 │    │                 │    │                 │
│ • CSV Files     │───►│ • Cloud Dataflow│───►│ • BigQuery      │
│ • JSON APIs     │    │ • Cloud Functions│   │ • Looker Studio │
│ • Database      │    │ • Cloud Run     │    │ • BigQuery ML   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Storage       │    │ Orchestration   │    │   Monitoring    │
│                 │    │                 │    │                 │
│ • Cloud Storage │    │ • Cloud Composer│    │ • Cloud Monitoring│
│ • BigQuery      │    │ • Cloud Scheduler│   │ • Cloud Logging │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### 1. Prerequisites
- Google Cloud Platform account
- Google Cloud SDK installed
- Python 3.9+
- Terraform (for infrastructure)

### 2. Setup
```bash
# Clone and setup
git clone <repository>
cd ecommerce-analytics-pipeline

# Install dependencies
pip install -r requirements.txt

# Setup GCP credentials
gcloud auth application-default login

# Deploy infrastructure
cd terraform
terraform init
terraform plan
terraform apply
```

### 3. Run Pipeline
```bash
# Start the pipeline
python src/main.py

# Or use Cloud Composer
gcloud composer environments run <env-name> --location <location> trigger_dag -- ecommerce_pipeline
```

## 📁 Project Structure

```
ecommerce-analytics-pipeline/
├── 📁 data/                    # Data files
│   ├── 📁 raw/                # Raw data sources
│   ├── 📁 processed/          # Intermediate processed data
│   └── 📁 curated/            # Final curated datasets
├── 📁 src/                     # Source code
│   ├── 📁 extractors/         # Data extraction modules
│   ├── 📁 transformers/       # Data transformation logic
│   ├── 📁 loaders/            # Data loading modules
│   └── 📁 utils/              # Utility functions
├── 📁 scripts/                 # Utility scripts
├── 📁 config/                  # Configuration files
│   ├── 📁 environments/       # Environment configs
│   └── 📁 credentials/        # Credential management
├── 📁 dags/                    # Airflow DAGs
├── 📁 notebooks/               # Jupyter notebooks
├── 📁 docs/                    # Documentation
├── 📁 terraform/               # Infrastructure as Code
├── 📄 requirements.txt         # Python dependencies
├── 📄 main.py                  # Main pipeline entry point
└── 📄 README.md                # This file
```

## 🛠️ GCP Services

### **Data Processing**
- **Cloud Dataflow**: Apache Beam pipelines for data transformation
- **Cloud Functions**: Serverless data processing
- **Cloud Run**: Containerized data processing services

### **Storage & Analytics**
- **Cloud Storage**: Data lake storage (raw, processed, curated)
- **BigQuery**: Data warehouse and analytics
- **BigQuery ML**: Machine learning models

### **Orchestration**
- **Cloud Composer**: Apache Airflow managed service
- **Cloud Scheduler**: Automated job scheduling
- **Cloud Build**: CI/CD pipeline

### **Monitoring & Security**
- **Cloud Monitoring**: Performance and health monitoring
- **Cloud Logging**: Centralized logging
- **IAM**: Identity and access management
- **VPC**: Network security

## 📊 Data Pipeline

### **1. Data Extraction**
- **Customer Orders**: CSV files from ERP system
- **Product Catalog**: JSON API from product management system
- **Web Analytics**: Google Analytics 4 data export
- **Inventory**: Database exports from warehouse system

### **2. Data Transformation**
- **Data Cleaning**: Remove duplicates, handle missing values
- **Data Enrichment**: Add calculated fields, geocoding
- **Data Aggregation**: Daily, weekly, monthly summaries
- **Data Quality**: Validation rules and checks

### **3. Data Loading**
- **Raw Layer**: Store original data in Cloud Storage
- **Processed Layer**: Store cleaned data in BigQuery
- **Curated Layer**: Store business-ready datasets

## 🔧 Configuration

### **Environment Variables**
```bash
# GCP Configuration
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_REGION=us-central1
GOOGLE_CLOUD_ZONE=us-central1-a

# BigQuery Configuration
BIGQUERY_DATASET=ecommerce_analytics
BIGQUERY_LOCATION=US

# Cloud Storage Configuration
GCS_BUCKET=ecommerce-data-lake
GCS_RAW_PREFIX=raw
GCS_PROCESSED_PREFIX=processed
GCS_CURATED_PREFIX=curated
```

### **Service Account Permissions**
- BigQuery Admin
- Cloud Storage Admin
- Dataflow Admin
- Cloud Composer Admin
- Cloud Functions Admin

## 📈 Analytics & Insights

### **Key Metrics**
- **Revenue Analytics**: Daily sales, product performance
- **Customer Analytics**: Segmentation, lifetime value
- **Inventory Analytics**: Stock levels, turnover rates
- **Marketing Analytics**: Campaign performance, ROI

### **Dashboards**
- **Executive Dashboard**: High-level KPIs and trends
- **Operational Dashboard**: Daily operations and alerts
- **Analytical Dashboard**: Deep-dive analysis and insights

## 🧪 Testing

```bash
# Run unit tests
python -m pytest tests/unit/

# Run integration tests
python -m pytest tests/integration/

# Run data quality tests
python scripts/run_data_quality_tests.py

# Run performance tests
python scripts/run_performance_tests.py
```

## 📊 Monitoring & Alerting

### **Key Metrics**
- Pipeline execution time
- Data quality scores
- Error rates and types
- Resource utilization

### **Alerts**
- Pipeline failures
- Data quality issues
- Performance degradation
- Security incidents

## 🔐 Security

- **Data Encryption**: At rest and in transit
- **Access Control**: IAM roles and permissions
- **Audit Logging**: All data access logged
- **Network Security**: VPC and firewall rules
- **Compliance**: GDPR, CCPA, SOC2

## 🚀 Deployment

### **Development**
```bash
# Local development
python src/main.py --env dev

# Local testing
docker-compose up -d
```

### **Staging**
```bash
# Deploy to staging
gcloud app deploy --version staging
```

### **Production**
```bash
# Deploy to production
gcloud app deploy --version production
```

## 📚 Documentation

- **[API Documentation](docs/API.md)**: Service endpoints and usage
- **[Data Dictionary](docs/DATA_DICTIONARY.md)**: Field definitions and business logic
- **[Deployment Guide](docs/DEPLOYMENT.md)**: Step-by-step deployment instructions
- **[Troubleshooting](docs/TROUBLESHOOTING.md)**: Common issues and solutions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Documentation**: [docs/](docs/)
- **Email**: support@yourcompany.com

---

**🛒 E-commerce Analytics Pipeline - Powered by Google Cloud Platform**

*Built with ❤️ using modern data engineering practices*
