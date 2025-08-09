# Terraform Configuration for E-commerce Analytics Pipeline
# Google Cloud Platform Infrastructure

terraform {
  required_version = ">= 1.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "~> 4.0"
    }
  }
  
  backend "gcs" {
    bucket = "ecommerce-analytics-terraform-state"
    prefix = "terraform/state"
  }
}

# Provider configuration
provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

provider "google-beta" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

# Variables
variable "project_id" {
  description = "The ID of the project to deploy to"
  type        = string
}

variable "region" {
  description = "The region to deploy to"
  type        = string
  default     = "us-central1"
}

variable "zone" {
  description = "The zone to deploy to"
  type        = string
  default     = "us-central1-a"
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "dataset_id" {
  description = "BigQuery dataset ID"
  type        = string
  default     = "ecommerce_analytics"
}

variable "bucket_names" {
  description = "Cloud Storage bucket names"
  type        = map(string)
  default = {
    raw_data     = "ecommerce-analytics-raw-data"
    processed    = "ecommerce-analytics-processed"
    curated      = "ecommerce-analytics-curated"
    terraform    = "ecommerce-analytics-terraform-state"
  }
}

# Enable required APIs
resource "google_project_service" "required_apis" {
  for_each = toset([
    "bigquery.googleapis.com",
    "storage.googleapis.com",
    "dataflow.googleapis.com",
    "composer.googleapis.com",
    "monitoring.googleapis.com",
    "logging.googleapis.com",
    "cloudfunctions.googleapis.com",
    "run.googleapis.com",
    "scheduler.googleapis.com",
    "build.googleapis.com",
    "iam.googleapis.com"
  ])
  
  project = var.project_id
  service = each.value
  
  disable_dependent_services = true
  disable_on_destroy         = false
}

# Create service account for the pipeline
resource "google_service_account" "pipeline_sa" {
  account_id   = "ecommerce-pipeline-sa"
  display_name = "E-commerce Analytics Pipeline Service Account"
  description  = "Service account for e-commerce analytics ETL pipeline"
  project      = var.project_id
}

# Grant BigQuery Admin role to service account
resource "google_project_iam_member" "bigquery_admin" {
  project = var.project_id
  role    = "roles/bigquery.admin"
  member  = "serviceAccount:${google_service_account.pipeline_sa.email}"
  
  depends_on = [google_project_service.required_apis]
}

# Grant Storage Admin role to service account
resource "google_project_iam_member" "storage_admin" {
  project = var.project_id
  role    = "roles/storage.admin"
  member  = "serviceAccount:${google_service_account.pipeline_sa.email}"
  
  depends_on = [google_project_service.required_apis]
}

# Grant Dataflow Admin role to service account
resource "google_project_iam_member" "dataflow_admin" {
  project = var.project_id
  role    = "roles/dataflow.admin"
  member  = "serviceAccount:${google_service_account.pipeline_sa.email}"
  
  depends_on = [google_project_service.required_apis]
}

# Grant Monitoring Admin role to service account
resource "google_project_iam_member" "monitoring_admin" {
  project = var.project_id
  role    = "roles/monitoring.admin"
  member  = "serviceAccount:${google_service_account.pipeline_sa.email}"
  
  depends_on = [google_project_service.required_apis]
}

# Grant Logging Admin role to service account
resource "google_project_iam_member" "logging_admin" {
  project = var.project_id
  role    = "roles/logging.admin"
  member  = "serviceAccount:${google_service_account.pipeline_sa.email}"
  
  depends_on = [google_project_service.required_apis]
}

# Create Cloud Storage buckets
resource "google_storage_bucket" "raw_data" {
  name          = "${var.bucket_names.raw_data}-${var.environment}"
  location      = var.region
  force_destroy = var.environment == "dev"
  
  uniform_bucket_level_access = true
  
  versioning {
    enabled = var.environment == "prod"
  }
  
  lifecycle_rule {
    condition {
      age = var.environment == "prod" ? 365 : 90
    }
    action {
      type = "Delete"
    }
  }
  
  depends_on = [google_project_service.required_apis]
}

resource "google_storage_bucket" "processed" {
  name          = "${var.bucket_names.processed}-${var.environment}"
  location      = var.region
  force_destroy = var.environment == "dev"
  
  uniform_bucket_level_access = true
  
  versioning {
    enabled = var.environment == "prod"
  }
  
  lifecycle_rule {
    condition {
      age = var.environment == "prod" ? 365 : 90
    }
    action {
      type = "Delete"
    }
  }
  
  depends_on = [google_project_service.required_apis]
}

resource "google_storage_bucket" "curated" {
  name          = "${var.bucket_names.curated}-${var.environment}"
  location      = var.region
  force_destroy = var.environment == "dev"
  
  uniform_bucket_level_access = true
  
  versioning {
    enabled = var.environment == "prod"
  }
  
  lifecycle_rule {
    condition {
      age = var.environment == "prod" ? 2555 : 180
    }
    action {
      type = "Delete"
    }
  }
  
  depends_on = [google_project_service.required_apis]
}

# Create BigQuery dataset
resource "google_bigquery_dataset" "analytics_dataset" {
  dataset_id  = "${var.dataset_id}_${var.environment}"
  project     = var.project_id
  location    = var.region
  description = "E-commerce analytics dataset for ${var.environment} environment"
  
  default_table_expiration_ms = var.environment == "prod" ? 7776000000 : 2592000000
  
  labels = {
    environment = var.environment
    project     = "ecommerce-analytics"
    managed_by  = "terraform"
  }
  
  depends_on = [google_project_service.required_apis]
}

# Create BigQuery tables
resource "google_bigquery_table" "customer_orders" {
  dataset_id = google_bigquery_dataset.analytics_dataset.dataset_id
  project    = var.project_id
  table_id   = "customer_orders"
  
  schema = file("${path.module}/schemas/customer_orders.json")
  
  clustering = ["date", "customer_id"]
  
  time_partitioning {
    type                     = "DAY"
    field                    = "order_date"
    expiration_ms            = var.environment == "prod" ? 7776000000 : 2592000000
    require_partition_filter = false
  }
  
  labels = {
    environment = var.environment
    table_type  = "fact"
    managed_by  = "terraform"
  }
  
  depends_on = [google_bigquery_dataset.analytics_dataset]
}

resource "google_bigquery_table" "product_catalog" {
  dataset_id = google_bigquery_dataset.analytics_dataset.dataset_id
  project    = var.project_id
  table_id   = "product_catalog"
  
  schema = file("${path.module}/schemas/product_catalog.json")
  
  clustering = ["category", "product_id"]
  
  labels = {
    environment = var.environment
    table_type  = "dimension"
    managed_by  = "terraform"
  }
  
  depends_on = [google_bigquery_dataset.analytics_dataset]
}

resource "google_bigquery_table" "web_analytics" {
  dataset_id = google_bigquery_dataset.analytics_dataset.dataset_id
  project    = var.project_id
  table_id   = "web_analytics"
  
  schema = file("${path.module}/schemas/web_analytics.json")
  
  clustering = ["date", "session_id"]
  
  time_partitioning {
    type                     = "DAY"
    field                    = "date"
    expiration_ms            = var.environment == "prod" ? 7776000000 : 2592000000
    require_partition_filter = false
  }
  
  labels = {
    environment = var.environment
    table_type  = "fact"
    managed_by  = "terraform"
  }
  
  depends_on = [google_bigquery_dataset.analytics_dataset]
}

resource "google_bigquery_table" "inventory" {
  dataset_id = google_bigquery_dataset.analytics_dataset.dataset_id
  project    = var.project_id
  table_id   = "inventory"
  
  schema = file("${path.module}/schemas/inventory.json")
  
  clustering = ["product_id", "warehouse_id"]
  
  labels = {
    environment = var.environment
    table_type  = "fact"
    managed_by  = "terraform"
  }
  
  depends_on = [google_bigquery_dataset.analytics_dataset]
}

# Create Cloud Composer environment (Apache Airflow)
resource "google_composer_environment" "pipeline_composer" {
  count = var.environment == "prod" ? 1 : 0
  
  name   = "ecommerce-pipeline-composer"
  region = var.region
  project = var.project_id
  
  config {
    software_config {
      image_version = "composer-2.0.31-airflow-2.2.5"
      
      airflow_config_overrides = {
        core-dags_are_paused_at_creation = "True"
        core-max_active_runs_per_dag     = "1"
        core-parallelism                 = "32"
        core-dag_concurrency            = "16"
      }
      
      env_variables = {
        ENVIRONMENT = var.environment
        PROJECT_ID  = var.project_id
        DATASET_ID  = google_bigquery_dataset.analytics_dataset.dataset_id
      }
    }
    
    node_config {
      network    = google_compute_network.pipeline_network[0].self_link
      subnetwork = google_compute_subnetwork.pipeline_subnet[0].self_link
      
      service_account = google_service_account.pipeline_sa.email
      
      machine_type = "n1-standard-2"
      disk_size_gb = 100
      
      oauth_scopes = [
        "https://www.googleapis.com/auth/cloud-platform"
      ]
    }
    
    private_environment_config {
      enable_private_endpoint = false
      cloud_sql_ipv4_cidr    = "10.0.0.0/24"
    }
  }
  
  depends_on = [google_project_service.required_apis]
}

# Create VPC network for Composer
resource "google_compute_network" "pipeline_network" {
  count = var.environment == "prod" ? 1 : 0
  
  name                    = "ecommerce-pipeline-network"
  auto_create_subnetworks = false
  project                 = var.project_id
}

# Create subnet for Composer
resource "google_compute_subnetwork" "pipeline_subnet" {
  count = var.environment == "prod" ? 1 : 0
  
  name          = "ecommerce-pipeline-subnet"
  ip_cidr_range = "10.0.0.0/24"
  region        = var.region
  network       = google_compute_network.pipeline_network[0].id
  project       = var.project_id
  
  private_ip_google_access = true
}

# Create Cloud Scheduler job for pipeline orchestration
resource "google_cloud_scheduler_job" "pipeline_scheduler" {
  count = var.environment == "prod" ? 1 : 0
  
  name        = "ecommerce-pipeline-scheduler"
  description = "Scheduler for e-commerce analytics pipeline"
  schedule    = "0 */4 * * *"  # Every 4 hours
  
  http_target {
    http_method = "POST"
    uri         = "https://${var.region}-${var.project_id}.cloudfunctions.net/trigger-pipeline"
    
    headers = {
      "Content-Type" = "application/json"
    }
    
    body = base64encode(jsonencode({
      environment = var.environment
      pipeline    = "ecommerce-analytics"
    }))
  }
  
  depends_on = [google_project_service.required_apis]
}

# Create Cloud Function for pipeline triggering
resource "google_cloudfunctions_function" "pipeline_trigger" {
  count = var.environment == "prod" ? 1 : 0
  
  name        = "ecommerce-pipeline-trigger"
  description = "Cloud Function to trigger e-commerce analytics pipeline"
  runtime     = "python39"
  
  available_memory_mb   = 256
  source_archive_bucket = google_storage_bucket.curated.name
  source_archive_object = google_storage_bucket_object.pipeline_function_zip.name
  
  trigger_http = true
  entry_point  = "trigger_pipeline"
  
  environment_variables = {
    ENVIRONMENT = var.environment
    PROJECT_ID  = var.project_id
    DATASET_ID  = google_bigquery_dataset.analytics_dataset.dataset_id
  }
  
  depends_on = [google_project_service.required_apis]
}

# Create zip file for Cloud Function
resource "google_storage_bucket_object" "pipeline_function_zip" {
  count = var.environment == "prod" ? 1 : 0
  
  name   = "pipeline-function.zip"
  bucket = google_storage_bucket.curated.name
  source = "${path.module}/functions/pipeline-trigger.zip"
}

# Create monitoring dashboard
resource "google_monitoring_dashboard" "pipeline_dashboard" {
  count = var.environment == "prod" ? 1 : 0
  
  dashboard_json = file("${path.module}/monitoring/pipeline-dashboard.json")
  
  depends_on = [google_project_service.required_apis]
}

# Create alerting policies
resource "google_monitoring_alert_policy" "pipeline_failure" {
  count = var.environment == "prod" ? 1 : 0
  
  display_name = "E-commerce Pipeline Failure Alert"
  combiner     = "OR"
  
  conditions {
    display_name = "Pipeline execution failed"
    
    condition_threshold {
      filter = "metric.type=\"custom.googleapis.com/pipeline/execution_status\""
      
      comparison = "COMPARISON_GREATER_THAN"
      threshold_value = 0
      
      duration = "300s"
      
      trigger {
        count = 1
      }
    }
  }
  
  notification_channels = [google_monitoring_notification_channel.email[0].name]
  
  depends_on = [google_project_service.required_apis]
}

# Create notification channel
resource "google_monitoring_notification_channel" "email" {
  count = var.environment == "prod" ? 1 : 0
  
  display_name = "Data Team Email Notifications"
  type         = "email"
  
  labels = {
    email_address = "data-team@company.com"
  }
  
  depends_on = [google_project_service.required_apis]
}

# Outputs
output "project_id" {
  description = "The ID of the project"
  value       = var.project_id
}

output "dataset_id" {
  description = "The ID of the BigQuery dataset"
  value       = google_bigquery_dataset.analytics_dataset.dataset_id
}

output "raw_data_bucket" {
  description = "The name of the raw data bucket"
  value       = google_storage_bucket.raw_data.name
}

output "processed_bucket" {
  description = "The name of the processed data bucket"
  value       = google_storage_bucket.processed.name
}

output "curated_bucket" {
  description = "The name of the curated data bucket"
  value       = google_storage_bucket.curated.name
}

output "service_account_email" {
  description = "The email of the service account"
  value       = google_service_account.pipeline_sa.email
}

output "composer_environment" {
  description = "The Cloud Composer environment"
  value       = var.environment == "prod" ? google_composer_environment.pipeline_composer[0].name : "Not created for ${var.environment}"
}
