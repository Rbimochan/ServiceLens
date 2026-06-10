# Phase 12 - Modeling Dataset

## Source and Eligibility

- Source: `data/processed/customer_support_tickets_prepared.csv`
- Source rows: 85,907
- Final modeling rows: 80,301
- Neutral CSAT score 3 excluded: 2,558
- Negative response durations excluded: 3,128

Only records with CSAT 1, 2, 4, or 5 and a non-negative response duration were eligible.

## Target

`low_csat_binary` is defined as:

- `0`: high CSAT, scores 4-5
- `1`: low CSAT, scores 1-2

Final target distribution:

- High CSAT (`0`): 68,126 (84.84%)
- Low CSAT (`1`): 12,175 (15.16%)

## Features

| Feature | Type | Purpose |
|---|---|---|
| channel_name | Categorical | Support interaction channel |
| category | Categorical | Main issue category |
| Sub-category | Categorical | Detailed issue type |
| response_time_minutes | Numeric | Valid response delay |
| Tenure Bucket | Categorical | Agent tenure group |
| Agent Shift | Categorical | Operating shift |
| issue_hour | Numeric | Hour the issue was reported |
| issue_weekday | Categorical | Weekday the issue was reported |
| issue_month | Numeric | Month extracted from issue report timestamp |

## Exclusions

Identifiers, customer remarks, agent/supervisor/manager names, sparse order and product fields, survey-response timing, CSAT-derived flags, and other leakage or duplicate fields were excluded. Survey date features were excluded because they occur after the support interaction and may not be available at prediction time.
