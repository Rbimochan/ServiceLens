# Phase 15 - Regression Dataset

- Source: `data/processed/customer_support_tickets_prepared.csv`
- Source rows: 85,907
- Regression rows: 82,779
- Target: `CSAT Score` (1-5)
- Train rows: 66,223
- Test rows: 16,556
- Split: 80/20 with `random_state=42`

Features: channel_name, category, Sub-category, Tenure Bucket, Agent Shift, issue_weekday, response_time_minutes, issue_hour, issue_month.

Rows with negative response duration were excluded. Identifiers, names, sparse order/product fields, CSAT-derived flags, survey-time fields, and other leakage variables were excluded.
