# Terraform Variables for E-commerce Analytics Pipeline
# Google Cloud Platform Infrastructure

variable "project_id" {
  description = "The ID of the Google Cloud project to deploy the infrastructure to"
  type        = string
  
  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{4,28}[a-z0-9]$", var.project_id))
    error_message = "Project ID must be 6-30 characters long, contain only lowercase letters, numbers, and hyphens, and start with a letter."
  }
}

variable "region" {
  description = "The default region for GCP resources"
  type        = string
  default     = "us-central1"
  
  validation {
    condition     = contains([
      "us-central1", "us-east1", "us-west1", "us-west2", "us-west3", "us-west4",
      "us-east4", "us-east5", "northamerica-northeast1", "northamerica-northeast2",
      "southamerica-east1", "europe-west1", "europe-west2", "europe-west3", "europe-west4",
      "europe-west5", "europe-west6", "europe-west8", "europe-west9", "europe-west10",
      "europe-west12", "europe-central2", "europe-north1", "europe-southwest1",
      "asia-east1", "asia-southeast1", "asia-southeast2", "asia-northeast1",
      "asia-northeast2", "asia-northeast3", "asia-south1", "asia-south2",
      "australia-southeast1", "australia-southeast2"
    ], var.region)
    error_message = "Region must be a valid GCP region."
  }
}

variable "zone" {
  description = "The default zone for GCP resources"
  type        = string
  default     = "us-central1-a"
  
  validation {
    condition     = can(regex("^[a-z0-9-]+-[a-z]$", var.zone))
    error_message = "Zone must be a valid GCP zone format (e.g., us-central1-a)."
  }
}

variable "environment" {
  description = "The deployment environment (dev, staging, prod)"
  type        = string
  default     = "dev"
  
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be one of: dev, staging, prod."
  }
}

variable "dataset_id" {
  description = "The BigQuery dataset ID for e-commerce analytics"
  type        = string
  default     = "ecommerce_analytics"
  
  validation {
    condition     = can(regex("^[a-zA-Z_][a-zA-Z0-9_]*$", var.dataset_id))
    error_message = "Dataset ID must start with a letter or underscore and contain only letters, numbers, and underscores."
  }
}

variable "bucket_names" {
  description = "Cloud Storage bucket names for different data layers"
  type        = map(string)
  default = {
    raw_data     = "ecommerce-analytics-raw-data"
    processed    = "ecommerce-analytics-processed"
    curated      = "ecommerce-analytics-curated"
    terraform    = "ecommerce-analytics-terraform-state"
  }
  
  validation {
    condition = alltrue([
      for name in values(var.bucket_names) : 
      can(regex("^[a-z0-9][a-z0-9-]*[a-z0-9]$", name)) && length(name) >= 3 && length(name) <= 63
    ])
    error_message = "Bucket names must be 3-63 characters long, contain only lowercase letters, numbers, and hyphens, and start/end with a letter or number."
  }
}

variable "composer_config" {
  description = "Configuration for Cloud Composer environment"
  type        = object({
    image_version = string
    machine_type  = string
    disk_size_gb  = number
    node_count    = number
    enable_private_endpoint = bool
  })
  default = {
    image_version = "composer-2.0.31-airflow-2.2.5"
    machine_type  = "n1-standard-2"
    disk_size_gb  = 100
    node_count    = 3
    enable_private_endpoint = false
  }
  
  validation {
    condition = alltrue([
      can(regex("^composer-\\d+\\.\\d+\\.\\d+-airflow-\\d+\\.\\d+\\.\\d+$", var.composer_config.image_version)),
      contains(["n1-standard-1", "n1-standard-2", "n1-standard-4", "n1-standard-8", "n1-standard-16", "n1-standard-32", "n1-standard-64", "n1-standard-96"], var.composer_config.machine_type),
      var.composer_config.disk_size_gb >= 20 && var.composer_config.disk_size_gb <= 2000,
      var.composer_config.node_count >= 3 && var.composer_config.node_count <= 10
    ])
    error_message = "Invalid Composer configuration values."
  }
}

variable "monitoring_config" {
  description = "Configuration for monitoring and alerting"
  type        = object({
    enable_dashboard = bool
    enable_alerting = bool
    alert_email     = string
    alert_slack_webhook = optional(string)
  })
  default = {
    enable_dashboard = true
    enable_alerting = true
    alert_email     = "data-team@company.com"
    alert_slack_webhook = null
  }
  
  validation {
    condition = can(regex("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$", var.monitoring_config.alert_email))
    error_message = "Alert email must be a valid email address."
  }
}

variable "network_config" {
  description = "Network configuration for VPC and subnets"
  type        = object({
    vpc_name = string
    subnet_name = string
    subnet_cidr = string
    enable_private_google_access = bool
  })
  default = {
    vpc_name = "ecommerce-pipeline-network"
    subnet_name = "ecommerce-pipeline-subnet"
    subnet_cidr = "10.0.0.0/24"
    enable_private_google_access = true
  }
  
  validation {
    condition = can(cidrhost(var.network_config.subnet_cidr, 0))
    error_message = "Subnet CIDR must be a valid IP address range."
  }
}

variable "data_retention" {
  description = "Data retention policies for different environments"
  type        = object({
    raw_data_days = number
    processed_days = number
    curated_days = number
    table_expiration_days = number
  })
  default = {
    raw_data_days = 90
    processed_days = 90
    curated_days = 180
    table_expiration_days = 30
  }
  
  validation {
    condition = alltrue([
      var.data_retention.raw_data_days >= 1 && var.data_retention.raw_data_days <= 3650,
      var.data_retention.processed_days >= 1 && var.data_retention.processed_days <= 3650,
      var.data_retention.curated_days >= 1 && var.data_retention.curated_days <= 3650,
      var.data_retention.table_expiration_days >= 1 && var.data_retention.table_expiration_days <= 3650
    ])
    error_message = "Data retention days must be between 1 and 3650."
  }
}

variable "security_config" {
  description = "Security configuration for the infrastructure"
  type        = object({
    enable_encryption = bool
    enable_audit_logging = bool
    service_account_rotation_days = number
    enable_vpc_service_controls = bool
  })
  default = {
    enable_encryption = true
    enable_audit_logging = true
    service_account_rotation_days = 90
    enable_vpc_service_controls = false
  }
  
  validation {
    condition = var.security_config.service_account_rotation_days >= 30 && var.security_config.service_account_rotation_days <= 365
    error_message = "Service account rotation days must be between 30 and 365."
  }
}

variable "cost_optimization" {
  description = "Cost optimization settings"
  type        = object({
    enable_autoscaling = bool
    enable_spot_instances = bool
    enable_preemptible_workers = bool
    budget_amount = number
    budget_currency = string
  })
  default = {
    enable_autoscaling = true
    enable_spot_instances = false
    enable_preemptible_workers = false
    budget_amount = 1000
    budget_currency = "USD"
  }
  
  validation {
    condition = alltrue([
      var.cost_optimization.budget_amount > 0,
      contains(["USD", "EUR", "GBP", "JPY", "CAD", "AUD"], var.cost_optimization.budget_currency)
    ])
    error_message = "Invalid cost optimization configuration."
  }
}

variable "tags" {
  description = "Common tags to apply to all resources"
  type        = map(string)
  default = {
    Project     = "ecommerce-analytics"
    Environment = "dev"
    ManagedBy   = "terraform"
    Owner       = "data-engineering"
    CostCenter  = "data-platform"
  }
}

variable "backup_config" {
  description = "Backup and disaster recovery configuration"
  type        = object({
    enable_backup = bool
    backup_retention_days = number
    backup_schedule = string
    enable_cross_region = bool
    enable_point_in_time_recovery = bool
  })
  default = {
    enable_backup = true
    backup_retention_days = 30
    backup_schedule = "0 2 * * *"  # Daily at 2 AM
    enable_cross_region = false
    enable_point_in_time_recovery = false
  }
  
  validation {
    condition = alltrue([
      var.backup_config.backup_retention_days >= 1 && var.backup_config.backup_retention_days <= 3650,
      can(regex("^[0-9*/-]+ [0-9*/-]+ [0-9*/-]+ [0-9*/-]+ [0-9*/-]+$", var.backup_config.backup_schedule))
    ])
    error_message = "Invalid backup configuration."
  }
}

variable "compliance_config" {
  description = "Compliance and regulatory requirements"
  type        = object({
    enable_data_governance = bool
    enable_pii_detection = bool
    enable_data_classification = bool
    compliance_frameworks = list(string)
    data_residency_region = string
  })
  default = {
    enable_data_governance = false
    enable_pii_detection = false
    enable_data_classification = false
    compliance_frameworks = []
    data_residency_region = "us-central1"
  }
  
  validation {
    condition = contains([
      "us-central1", "us-east1", "us-west1", "us-west2", "us-west3", "us-west4",
      "us-east4", "us-east5", "europe-west1", "europe-west2", "europe-west3",
      "europe-west4", "europe-west5", "europe-west6", "europe-west8", "europe-west9",
      "europe-west10", "europe-west12", "europe-central2", "europe-north1",
      "asia-east1", "asia-southeast1", "asia-southeast2", "asia-northeast1",
      "asia-northeast2", "asia-northeast3", "asia-south1", "asia-south2",
      "australia-southeast1", "australia-southeast2"
    ], var.compliance_config.data_residency_region)
    error_message = "Data residency region must be a valid GCP region."
  }
}
