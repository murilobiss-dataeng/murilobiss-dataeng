# Social FIT Data Intelligence Platform - Makefile
# ===============================================

.PHONY: help install test lint format clean run setup deploy

# Default target
help:
	@echo "Social FIT Data Intelligence Platform"
	@echo "===================================="
	@echo ""
	@echo "Available commands:"
	@echo "  install    - Install dependencies"
	@echo "  setup      - Setup development environment"
	@echo "  test       - Run tests"
	@echo "  lint       - Run linting"
	@echo "  format     - Format code"
	@echo "  clean      - Clean build artifacts"
	@echo "  run        - Run ETL pipeline"
	@echo "  dashboard  - Start dashboard"
	@echo "  deploy     - Deploy to production"
	@echo "  docs       - Generate documentation"

# Install dependencies
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	pip install -e .[dev]

# Setup development environment
setup: install
	@echo "Setting up development environment..."
	@if [ ! -f .env ]; then \
		echo "Creating .env file from template..."; \
		cp env_example.txt .env; \
		echo "Please edit .env file with your credentials"; \
	fi
	@mkdir -p logs data
	@echo "Development environment setup complete!"

# Run tests
test:
	@echo "Running tests..."
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term-missing

# Run specific test categories
test-unit:
	@echo "Running unit tests..."
	pytest tests/unit/ -v

test-integration:
	@echo "Running integration tests..."
	pytest tests/integration/ -v

# Run linting
lint:
	@echo "Running linting..."
	flake8 src/ tests/ --max-line-length=100 --ignore=E203,W503
	mypy src/ --ignore-missing-imports

# Format code
format:
	@echo "Formatting code..."
	black src/ tests/ --line-length=100
	isort src/ tests/

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .pytest_cache/ htmlcov/ .coverage
	@echo "Clean complete!"

# Run ETL pipeline
run:
	@echo "Running ETL pipeline..."
	python main.py

# Run ETL pipeline with specific options
run-incremental:
	@echo "Running incremental update..."
	python main.py incremental

run-test:
	@echo "Running test mode..."
	python main.py test

# Start dashboard
dashboard:
	@echo "Starting dashboard..."
	python src/dashboard.py

# Deploy to production
deploy:
	@echo "Deploying to production..."
	@echo "Please ensure you have configured production environment variables"
	@echo "Running production deployment checks..."
	pytest tests/integration/ -m "not slow"
	@echo "Deployment checks passed!"

# Generate documentation
docs:
	@echo "Generating documentation..."
	@echo "Documentation is available in the docs/ directory"
	@echo "API documentation: docs/API.md"
	@echo "Development guide: docs/DEVELOPMENT.md"
	@echo "Deployment guide: docs/DEPLOYMENT.md"

# Database operations
db-test:
	@echo "Testing database connection..."
	python scripts/debug_tables.py

db-setup:
	@echo "Setting up database tables..."
	@echo "Please run the SQL script in scripts/create_tables_public_final.sql"
	@echo "in your Supabase SQL editor"

# Docker operations
docker-build:
	@echo "Building Docker image..."
	docker build -t social-fit .

docker-run:
	@echo "Running Docker container..."
	docker run -d --name social-fit -p 8050:8050 --env-file .env social-fit

docker-stop:
	@echo "Stopping Docker container..."
	docker stop social-fit
	docker rm social-fit

# Development utilities
dev-install:
	@echo "Installing development dependencies..."
	pip install -r requirements.txt
	pip install -e .[dev]
	pre-commit install

dev-setup: dev-install setup
	@echo "Development setup complete!"

# Monitoring and logs
logs:
	@echo "Viewing application logs..."
	tail -f logs/social_fit_etl.log

logs-clear:
	@echo "Clearing logs..."
	rm -f logs/*.log

# Backup and restore
backup:
	@echo "Creating backup..."
	@mkdir -p backups
	@echo "Please implement backup logic based on your deployment setup"

restore:
	@echo "Restoring from backup..."
	@echo "Please implement restore logic based on your deployment setup"

# Performance testing
perf-test:
	@echo "Running performance tests..."
	pytest tests/integration/test_pipeline.py::TestPipelineIntegration::test_performance_integration -v

# Security checks
security-check:
	@echo "Running security checks..."
	bandit -r src/ -f json -o security-report.json
	@echo "Security report generated: security-report.json"

# Full development cycle
dev-cycle: clean install test lint format
	@echo "Development cycle complete!"

# Production preparation
prod-prep: clean test lint security-check
	@echo "Production preparation complete!"

# Quick start for new developers
quickstart: dev-setup
	@echo "Quick start complete!"
	@echo "Next steps:"
	@echo "1. Edit .env file with your credentials"
	@echo "2. Run 'make run' to test the pipeline"
	@echo "3. Run 'make dashboard' to start the dashboard" 