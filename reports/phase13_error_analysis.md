# Phase 13 - Error Analysis

## Overall

- Correct predictions: 10,588 (65.92%)
- Incorrect predictions: 5,473 (34.08%)
- Median response time, correct: 3.0 minutes
- Median response time, incorrect: 22.0 minutes

Errors are concentrated in high-volume categories and channels. Counts therefore reflect both model weakness and exposure volume; error rates are included to avoid treating volume alone as evidence.

### category

| category | Records | Errors | Error Rate |
|---|---:|---:|---:|
| Returns | 8,210 | 2,340 | 28.50% |
| Order Related | 4,363 | 1,812 | 41.53% |
| Refund Related | 866 | 325 | 37.53% |
| Product Queries | 688 | 311 | 45.20% |
| Cancellation | 420 | 214 | 50.95% |
| Feedback | 449 | 161 | 35.86% |
| Shopzilla Related | 514 | 148 | 28.79% |
| Payments related | 408 | 106 | 25.98% |
### channel_name

| channel_name | Records | Errors | Error Rate |
|---|---:|---:|---:|
| Inbound | 12,814 | 4,347 | 33.92% |
| Outcall | 2,682 | 847 | 31.58% |
| Email | 565 | 279 | 49.38% |
### Tenure Bucket

| Tenure Bucket | Records | Errors | Error Rate |
|---|---:|---:|---:|
| >90 | 5,733 | 1,887 | 32.91% |
| On Job Training | 4,675 | 1,828 | 39.10% |
| 31-60 | 2,215 | 681 | 30.74% |
| 0-30 | 2,118 | 669 | 31.59% |
| 61-90 | 1,320 | 408 | 30.91% |
### Agent Shift

| Agent Shift | Records | Errors | Error Rate |
|---|---:|---:|---:|
| Morning | 7,710 | 2,843 | 36.87% |
| Evening | 6,273 | 2,007 | 31.99% |
| Afternoon | 1,093 | 356 | 32.57% |
| Split | 735 | 176 | 23.95% |
| Night | 250 | 91 | 36.40% |

The model has difficulty separating low- and high-CSAT outcomes within the same operational segments. This indicates that channel, category, response time, tenure, and shift do not fully capture customer-specific expectations or resolution quality.
