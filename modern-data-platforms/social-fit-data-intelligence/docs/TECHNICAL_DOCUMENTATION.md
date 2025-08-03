# Social FIT Data Intelligence Platform – Technical Documentation

## 1. Project Overview

Social FIT is a Data Intelligence Platform that integrates gym ERP data with Instagram analytics to generate actionable business insights. It features a robust ETL pipeline, analytics engine, and a professional web dashboard for real-time monitoring and decision-making.

## 2. Architecture & Components

- **Backend:** Python 3.9+, Pydantic, Pandas, Supabase (PostgreSQL), Loguru
- **Frontend:** HTML5, Bootstrap 5, Chart.js, Supabase JS, Leaflet (map)
- **DevOps:** GitHub Actions, GitHub Pages, Docker (for Metabase alternative)

### Directory Structure
```
social_fit/
├── index.html                # Main dashboard (GitHub Pages)
├── dashboard/                # Dashboard config & setup
├── metabase/                 # Metabase alternative
├── src/                      # Main source code
│   ├── etl/                  # ETL pipeline
│   ├── analytics/            # Analytics engine
│   ├── database/             # Database management
│   ├── models/               # Data models
│   └── config/               # Configuration
├── tests/                    # Automated tests
├── docs/                     # Documentation
├── scripts/                  # Utility scripts
├── data/                     # Example data
```

## 3. ETL Pipeline

- **Extract:** Reads student and Instagram data from CSV files in `/data`.
- **Transform:** Cleans, validates, and converts data into Pydantic models. Handles type conversion, deduplication, and normalization.
- **Load:** Inserts data into Supabase PostgreSQL database using SQLAlchemy.
- **Analytics:** Generates KPIs, distributions, and actionable insights, storing results in the database.

## 4. Data Models

- **Student:**
  - id, name, gender, birth_date, address, neighborhood, plan_type, gympass, monthly_value, total_value, plan_start_date, active_plan
- **InstagramPost:**
  - date, likes, comments, saves, reach, profile_visits, new_followers, main_hashtag
- **Analytics Models:**
  - StudentAnalytics, InstagramAnalytics, CrossPlatformAnalytics

## 5. Analytics Engine

- Computes KPIs: total students, active plans, monthly revenue, average engagement, etc.
- Generates distributions (plan, gender, neighborhood)
- Correlates Instagram engagement with enrollments
- Produces actionable business insights

## 6. Dashboard (Frontend)

- **KPIs:** Total students, active plans, monthly revenue, average engagement
- **Charts:** Plan distribution, gender distribution, engagement trends
- **Tables:** Top students by total plan value
- **Insights:** Actionable recommendations
- **Map:** Student distribution by neighborhood (Curitiba)
- **Theme:** Black, yellow, and white (Social FIT branding)
- **Tech:** Bootstrap 5, Chart.js, Leaflet, Supabase JS

## 7. Deployment & Configuration

- **Local:**
  - `pip install -r requirements.txt`
  - Configure `.env` with Supabase credentials
  - Run ETL: `python main.py`
  - Open dashboard: `open index.html`
- **Production:**
  - Deploy dashboard via GitHub Pages
  - Use `scripts/deploy_dashboard.sh` for automation
  - Configure GitHub Pages to serve from root of `main` branch

## 8. Security

- Credentials managed via environment variables (`.env`)
- Row Level Security enabled in Supabase
- Public dashboard uses anonymous key
- HTTPS enforced in production

## 9. Testing

- Unit and integration tests in `/tests`
- Run all tests: `make test`
- Pytest for test discovery and execution

## 10. Contribution & License

- Fork, branch, commit, and open Pull Requests for contributions
- Licensed under MIT (see LICENSE) 