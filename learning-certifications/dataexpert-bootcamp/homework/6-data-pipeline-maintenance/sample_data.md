# Sample Data for TechFlow Solutions Pipelines

## Pipeline Data Examples

### 1. Profit Pipeline Data

#### Revenue Data
```json
{
  "account_id": "ACC_001",
  "subscription_tier": "Enterprise",
  "monthly_revenue": 25000.00,
  "user_licenses": 150,
  "additional_features": ["Advanced Analytics", "API Access", "Priority Support"],
  "feature_revenue": 5000.00,
  "total_monthly_revenue": 30000.00,
  "billing_date": "2024-01-15",
  "payment_status": "Paid"
}
```

#### Expense Data
```json
{
  "account_id": "ACC_001",
  "expense_category": "Infrastructure",
  "monthly_cost": 8000.00,
  "cost_breakdown": {
    "cloud_services": 5000.00,
    "database_hosting": 2000.00,
    "monitoring_tools": 1000.00
  },
  "expense_date": "2024-01-31"
}
```

#### Salary Data
```json
{
  "team_id": "ENG_001",
  "team_name": "Data Engineering",
  "monthly_salary_total": 45000.00,
  "headcount": 4,
  "cost_per_engineer": 11250.00,
  "salary_month": "2024-01"
}
```

### 2. Growth Pipeline Data

#### Account Status Changes
```json
{
  "account_id": "ACC_002",
  "previous_status": "Trial",
  "new_status": "Active",
  "change_date": "2024-01-20",
  "change_reason": "Trial Conversion",
  "sales_rep": "John Smith",
  "contract_value": 15000.00
}
```

#### License Changes
```json
{
  "account_id": "ACC_003",
  "previous_licenses": 50,
  "new_licenses": 75,
  "change_date": "2024-01-25",
  "change_type": "Upgrade",
  "additional_revenue": 5000.00,
  "effective_date": "2024-02-01"
}
```

#### Subscription Renewals
```json
{
  "account_id": "ACC_004",
  "renewal_date": "2024-02-01",
  "previous_contract_value": 20000.00,
  "new_contract_value": 25000.00,
  "renewal_type": "Expansion",
  "contract_duration": "12 months"
}
```

### 3. Engagement Pipeline Data

#### User Click Events
```json
{
  "user_id": "USER_123",
  "account_id": "ACC_001",
  "event_type": "feature_click",
  "feature_name": "Advanced Analytics",
  "timestamp": "2024-01-15T10:30:00Z",
  "session_id": "SESS_456",
  "page_url": "/analytics/dashboard",
  "user_agent": "Mozilla/5.0...",
  "ip_address": "192.168.1.100"
}
```

#### Platform Usage Time
```json
{
  "user_id": "USER_123",
  "account_id": "ACC_001",
  "session_start": "2024-01-15T09:00:00Z",
  "session_end": "2024-01-15T17:00:00Z",
  "total_active_time_minutes": 420,
  "features_used": ["Dashboard", "Reports", "API"],
  "device_type": "Desktop"
}
```

#### Team Activity Metrics
```json
{
  "account_id": "ACC_001",
  "team_id": "TEAM_001",
  "date": "2024-01-15",
  "active_users": 45,
  "total_session_time_hours": 180,
  "features_accessed": ["Dashboard", "Reports", "Analytics", "API"],
  "api_calls": 1250,
  "reports_generated": 23
}
```

## Pipeline Dependencies

### Data Flow Diagram
```
User Activity (Kafka) → Engagement Pipeline → Aggregated Pipeline
Account Changes → Growth Pipeline → Aggregated Pipeline
Financial Data → Profit Pipeline → Aggregated Pipeline
```

### Common Data Issues

#### 1. Late Data Arrival
- **Scenario**: User clicks from 48+ hours ago arrive in Kafka
- **Impact**: Engagement metrics become stale
- **Detection**: Timestamp validation in pipeline

#### 2. Missing Account Status
- **Scenario**: Account status change missing intermediate step
- **Impact**: Growth metrics incomplete
- **Detection**: Data completeness checks

#### 3. Revenue Mismatch
- **Scenario**: Pipeline revenue doesn't match accounting system
- **Impact**: Profit calculations incorrect
- **Detection**: Cross-system validation

## SLA Requirements

### Data Freshness
- **Profit Pipeline**: 24 hours
- **Growth Pipeline**: End of week
- **Engagement Pipeline**: 48 hours
- **Aggregated Pipeline**: Monthly (investor reports)

### Data Quality
- **Completeness**: 100% for investor reports
- **Accuracy**: Validated by business teams
- **Timeliness**: Within defined SLAs

### Issue Resolution
- **Critical Issues**: 48 hours
- **Standard Issues**: 1 week
- **Investor Report Issues**: By end of month

## Monitoring Metrics

### Pipeline Health
- **Success Rate**: 99.9%
- **Processing Time**: <2 hours for daily pipelines
- **Data Volume**: Monitor for unusual spikes/drops

### Business Impact
- **Revenue Accuracy**: ±1% tolerance
- **Growth Metrics**: Real-time validation
- **Engagement Trends**: Weekly analysis

### Technical Performance
- **Kafka Lag**: <5 minutes
- **Spark Job Duration**: <1 hour
- **Database Query Time**: <30 seconds
