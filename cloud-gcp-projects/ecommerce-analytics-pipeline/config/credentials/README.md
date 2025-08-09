# Credentials Configuration

This directory is for storing credential files and configuration that should NOT be committed to version control.

## Security Notice

⚠️ **NEVER commit actual credential files to this repository!**

## Required Credentials

### 1. Google Cloud Service Account Key
- **File**: `service-account-key.json`
- **Description**: JSON key file for the GCP service account
- **How to obtain**: 
  1. Go to GCP Console > IAM & Admin > Service Accounts
  2. Create or select a service account
  3. Create a new key (JSON format)
  4. Download and place in this directory

### 2. Environment Variables
Copy `env.example` to `.env` and fill in your actual values:

```bash
cp ../env.example .env
```

### 3. Required Environment Variables
- `GOOGLE_APPLICATION_CREDENTIALS`: Path to service account key
- `GCP_PROJECT_ID`: Your GCP project ID
- `GCP_REGION`: Your GCP region
- `SLACK_WEBHOOK_URL`: Slack webhook for notifications (optional)

## File Structure
```
credentials/
├── .gitkeep          # This file (keeps directory in git)
├── README.md         # This documentation
├── .env              # Your environment variables (create from env.example)
└── service-account-key.json  # GCP service account key (download manually)
```

## Setup Instructions

1. **Download GCP Service Account Key**:
   ```bash
   # Place your downloaded JSON key file here
   mv ~/Downloads/your-project-key.json ./service-account-key.json
   ```

2. **Set Environment Variables**:
   ```bash
   cp ../env.example .env
   # Edit .env with your actual values
   ```

3. **Verify Setup**:
   ```bash
   # Test that credentials are working
   python ../test_imports.py
   ```

## Troubleshooting

- **Permission Denied**: Ensure the service account has the necessary roles
- **Authentication Failed**: Verify the key file path in your `.env`
- **Project Not Found**: Check your `GCP_PROJECT_ID` in `.env`
