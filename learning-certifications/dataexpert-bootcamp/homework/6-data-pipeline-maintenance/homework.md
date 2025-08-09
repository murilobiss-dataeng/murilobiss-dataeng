# Week 6 Data Pipeline Maintenance

## Homework Assignment

Imagine you're in a group of 4 data engineers, you will be in charge of creating the following things:

### Business Context
You are managing data pipelines for **TechFlow Solutions**, a SaaS platform provider (similar to Salesforce) that provides licenses and features to other companies. Companies can sign up, provide licenses to a certain number of their staff, as well as buy additional features/support.

### Pipeline Management
You are in charge of managing these 5 pipelines that cover the following business areas:

1. **Profit Pipeline**
   - Unit-level profit needed for experiments
   - Aggregate profit reported to investors

2. **Growth Pipeline**
   - Aggregate growth reported to investors
   - Daily growth needed for experiments

3. **Engagement Pipeline**
   - Aggregate engagement reported to investors

4. **Aggregated Pipeline for Executives/Investors**
   - Combines data from all pipelines for executive reporting

5. **Aggregated Pipeline for Experiment Team**
   - Data science team uses unit level/daily level data for AB testing

### Your Tasks

#### 1. Pipeline Ownership Matrix
- Determine who is the **primary owner** and **secondary owner** of each pipeline
- Identify the **business stakeholders** for each pipeline
- Consider the business impact and technical complexity

#### 2. Fair On-Call Schedule
- Create an **on-call schedule** that is fair for all 4 team members
- Consider **holidays and vacation time**
- Plan for **monthly investor report periods** when all pipelines must be monitored closely

#### 3. Comprehensive Runbooks
Create detailed runbooks for all pipelines that report metrics to investors:
- **Pipeline details** (name, schedule, critical level)
- **Data types** and sources
- **Common issues** and troubleshooting steps
- **SLA requirements**
- **Monitoring and alerting** strategies

#### 4. Operational Excellence
- **Escalation matrix** with clear levels
- **Communication protocols** (daily, weekly, monthly)
- **Success metrics** and KPIs

### Submission Requirements
Create a comprehensive markdown file that covers all the above requirements. Your solution should demonstrate:

- **Clear ownership** and responsibility assignment
- **Fair workload distribution** among team members
- **Detailed troubleshooting** procedures for common issues
- **Professional documentation** standards
- **Business impact awareness** for investor-facing pipelines

### Reference Example
Use the Pacific Infra Group case study as inspiration for:
- Pipeline types and business context
- Common technical issues (Kafka outages, Spark OOM errors, etc.)
- SLA requirements and business priorities
- Team structure and communication patterns

Submit your solution as a markdown file! 