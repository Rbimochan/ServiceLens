# Phase 13 - False Positive Analysis

False positives are cases predicted as low CSAT that were actually high CSAT.

- False positives: 4,595
- Share of test records: 28.61%
- Median response time: 34.0 minutes

### category

| category | Records | Errors | Error Rate |
|---|---:|---:|---:|
| Returns | 8,210 | 1,926 | 23.46% |
| Order Related | 4,363 | 1,547 | 35.46% |
| Refund Related | 866 | 284 | 32.79% |
| Product Queries | 688 | 277 | 40.26% |
| Cancellation | 420 | 190 | 45.24% |
| Feedback | 449 | 136 | 30.29% |
| Shopzilla Related | 514 | 125 | 24.32% |
| Payments related | 408 | 66 | 16.18% |
### channel_name

| channel_name | Records | Errors | Error Rate |
|---|---:|---:|---:|
| Inbound | 12,814 | 3,652 | 28.50% |
| Outcall | 2,682 | 686 | 25.58% |
| Email | 565 | 257 | 45.49% |
### Tenure Bucket

| Tenure Bucket | Records | Errors | Error Rate |
|---|---:|---:|---:|
| >90 | 5,733 | 1,604 | 27.98% |
| On Job Training | 4,675 | 1,561 | 33.39% |
| 31-60 | 2,215 | 573 | 25.87% |
| 0-30 | 2,118 | 540 | 25.50% |
| 61-90 | 1,320 | 317 | 24.02% |
### Agent Shift

| Agent Shift | Records | Errors | Error Rate |
|---|---:|---:|---:|
| Morning | 7,710 | 2,426 | 31.47% |
| Evening | 6,273 | 1,655 | 26.38% |
| Afternoon | 1,093 | 295 | 26.99% |
| Split | 735 | 139 | 18.91% |
| Night | 250 | 80 | 32.00% |

False positives are expected when balanced training lowers the decision boundary for the minority class. Operationally, they create unnecessary interventions. Threshold optimization therefore tests whether precision can increase without losing too much recall.
