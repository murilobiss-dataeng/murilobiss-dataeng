# Data Pipeline Maintenance Exercise Solution

## Group Information
**Group:** Data Engineering Team - TechFlow Solutions 
**Members:** 4 Data Engineers  
**Business Context:** SaaS platform provider (similar to Salesforce) that provides licenses and features to other companies

## Pipeline Overview

### 1. Profit Pipeline
- **Purpose:** Calculate profit (subscription costs - expenses) and unit-level profit
- **Outputs:** 
  - Unit-level profit for experiments (profit / # subscribers)
  - Aggregate profit for investors
- **Data Sources:** Revenue from accounts, operational expenses, aggregated salaries

### 2. Growth Pipeline
- **Purpose:** Track account growth metrics and subscription changes
- **Outputs:**
  - Daily growth data for experiments
  - Aggregate growth for investors
- **Data Sources:** Account type changes, license increases, subscription renewals

### 3. Engagement Pipeline
- **Purpose:** Measure user engagement and platform usage
- **Outputs:** Aggregate engagement metrics for investors
- **Data Sources:** User clicks, platform usage time, team activity

## Pipeline Ownership Matrix

| Pipeline | Primary Owner | Secondary Owner | Business Stakeholder |
|----------|---------------|------------------|---------------------|
| Profit | Finance Team | Data Engineering | CFO, Risk Team |
| Growth | Accounts Team | Data Engineering | Sales, Account Executives |
| Engagement | Software Frontend Team | Data Engineering | Product Team |
| **All Aggregated Pipelines** | Business Analytics Team | Data Engineering | Executives, Investors |

## On-Call Schedule

### Weekly Rotation (Fair Distribution)
- **Week 1:** Data Engineer A
- **Week 2:** Data Engineer B  
- **Week 3:** Data Engineer C
- **Week 4:** Data Engineer D

### Holiday Considerations
- **Major Holidays:** Rotate responsibility to next person in sequence
- **Vacation Coverage:** Team member going on vacation swaps with next person in rotation
- **Emergency Coverage:** If primary on-call person is unavailable, next person in rotation covers

### Monthly Investor Report Period
- **Last Week of Month:** All DE team members monitor pipelines closely
- **Priority:** Profit, Growth, and Engagement pipelines must be running smoothly

## Runbooks for Investor-Reporting Pipelines

### 1. Profit Pipeline Runbook

#### Pipeline Details
- **Name:** Profit Calculation Pipeline
- **Schedule:** Monthly (for investors), Daily (for experiments)
- **Critical Level:** HIGH (affects financial reporting)

#### Data Types
- Revenue from all active accounts
- Operational expenses (assets, services)
- Aggregated salaries by team
- Account subscription costs

#### Common Issues & Troubleshooting
1. **Revenue Mismatch**
   - **Symptom:** Numbers don't align with account filings
   - **Action:** Verify with accounting team, check data freshness
   - **Escalation:** Immediate escalation to Finance Team

2. **Missing Expense Data**
   - **Symptom:** Incomplete expense records
   - **Action:** Check Ops team data feeds, verify data completeness
   - **Escalation:** Contact Ops team lead

3. **Salary Aggregation Errors**
   - **Symptom:** Incorrect team salary totals
   - **Action:** Verify HR data source, check for duplicate records
   - **Escalation:** Contact HR data team

#### SLA Requirements
- **Data Freshness:** 24 hours
- **Accuracy Review:** Monthly by account team
- **Issue Resolution:** Within 48 hours for critical issues

#### Monitoring & Alerts
- **Revenue Threshold Alerts:** If revenue drops >10% from previous month
- **Expense Anomaly Detection:** Unusual expense spikes
- **Data Completeness:** Ensure all accounts are included

---

### 2. Growth Pipeline Runbook

#### Pipeline Details
- **Name:** Growth Metrics Pipeline
- **Schedule:** Weekly (for investors), Daily (for experiments)
- **Critical Level:** MEDIUM-HIGH

#### Data Types
- Account type changes
- License count changes
- Subscription renewal status
- Account upgrade/downgrade events

#### Common Issues & Troubleshooting
1. **Missing Account Status**
   - **Symptom:** Current account status missing from time series
   - **Action:** Check for missing intermediate steps in status changes
   - **Escalation:** Contact Account Executive team

2. **Data Gaps in Time Series**
   - **Symptom:** Missing data points in growth trends
   - **Action:** Identify missing data sources, check upstream pipelines
   - **Escalation:** Data Engineering team investigation

3. **License Count Discrepancies**
   - **Symptom:** License numbers don't match account records
   - **Action:** Verify license management system data
   - **Escalation:** Account team verification

#### SLA Requirements
- **Data Freshness:** End of week for latest account statuses
- **Issue Resolution:** Within 1 week
- **Data Completeness:** 100% of active accounts

#### Monitoring & Alerts
- **Growth Rate Alerts:** If growth drops below expected threshold
- **Account Status Completeness:** Ensure all accounts have current status
- **License Count Validation:** Verify against account management system

---

### 3. Engagement Pipeline Runbook

#### Pipeline Details
- **Name:** User Engagement Pipeline
- **Schedule:** Weekly (for investors), Daily (for experiments)
- **Critical Level:** MEDIUM

#### Data Types
- User click events
- Platform usage time
- Team activity metrics
- Feature usage patterns

#### Common Issues & Troubleshooting
1. **Late Data Arrival**
   - **Symptom:** Click events arrive >48 hours after occurrence
   - **Action:** Check Kafka queue health, investigate upstream delays
   - **Escalation:** Contact Software Frontend team

2. **Kafka Outages**
   - **Symptom:** No user click data flowing through pipeline
   - **Action:** Check Kafka cluster status, verify connectivity
   - **Escalation:** Infrastructure team, immediate alert

3. **Duplicate Events**
   - **Symptom:** Same event processed multiple times
   - **Action:** Implement deduplication logic, check event IDs
   - **Escalation:** Data Engineering team

4. **Data Quality Issues**
   - **Symptom:** Invalid click timestamps or user IDs
   - **Action:** Validate data format, check upstream data quality
   - **Escalation:** Frontend team for data format issues

#### SLA Requirements
- **Data Freshness:** Within 48 hours of event occurrence
- **Issue Resolution:** Within 1 week
- **Data Quality:** 99.9% valid events

#### Monitoring & Alerts
- **Data Freshness Alerts:** If latest timestamp > current time - 48 hours
- **Kafka Health Monitoring:** Queue depth, consumer lag
- **Duplicate Event Detection:** Monitor for unusual duplicate rates

---

### 4. Aggregated Executive/Investor Pipeline Runbook

#### Pipeline Details
- **Name:** Executive Dashboard Pipeline
- **Schedule:** Monthly (for investors), Weekly (for executives)
- **Critical Level:** HIGHEST (affects investor reporting)

#### Data Types
- Aggregated profit metrics
- Growth summaries
- Engagement overviews
- Cross-pipeline joined data

#### Common Issues & Troubleshooting
1. **Spark Join Failures**
   - **Symptom:** Out of Memory (OOM) errors during large joins
   - **Action:** Optimize join strategies, increase memory allocation
   - **Escalation:** Data Engineering team, infrastructure team

2. **Stale Data Issues**
   - **Symptom:** Data from previous pipelines is outdated
   - **Action:** Check upstream pipeline freshness, trigger backfills
   - **Escalation:** Data Engineering team

3. **Missing Data Errors**
   - **Symptom:** NA values or divide-by-zero errors in calculations
   - **Action:** Implement data validation, check for null values
   - **Escalation:** Data Engineering team

4. **Calculation Errors**
   - **Symptom:** Incorrect aggregated metrics
   - **Action:** Verify calculation logic, check input data quality
   - **Escalation:** Business Analytics team validation

#### SLA Requirements
- **Data Freshness:** Monthly for investor reports
- **Issue Resolution:** By end of month (before investor reporting)
- **Data Accuracy:** 100% validated by Business Analytics team

#### Monitoring & Alerts
- **Pipeline Success Rate:** 100% for monthly runs
- **Data Completeness:** Ensure all required metrics are available
- **Calculation Validation:** Automated checks for metric ranges

## Escalation Matrix

### Level 1: Data Engineering Team
- Pipeline failures
- Data quality issues
- Performance problems

### Level 2: Business Teams
- Finance Team (Profit pipeline)
- Accounts Team (Growth pipeline)
- Software Frontend Team (Engagement pipeline)

### Level 3: Management
- Business Analytics Team Lead
- Data Engineering Team Lead
- CFO (for critical financial issues)

## Communication Protocols

### Daily Standups
- Pipeline status updates
- Issue identification and assignment
- Resource allocation

### Weekly Reviews
- Pipeline performance metrics
- SLA compliance review
- On-call handoff meetings

### Monthly Reviews
- Investor report preparation
- Pipeline optimization opportunities
- Team capacity planning

## Success Metrics

### Pipeline Reliability
- **Uptime:** 99.9%
- **SLA Compliance:** 100%
- **Issue Resolution Time:** <48 hours for critical issues

### Data Quality
- **Completeness:** 100% for investor reports
- **Accuracy:** Validated by business teams
- **Freshness:** Within defined SLAs

### Team Efficiency
- **On-call Rotation:** Fair distribution
- **Knowledge Transfer:** 30-minute handoff meetings
- **Documentation:** Updated runbooks and procedures
