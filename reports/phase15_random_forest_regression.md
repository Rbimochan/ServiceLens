# Phase 15 - Random Forest Regression

The model used 200 trees, `min_samples_leaf=5`, `max_features=0.7`, and `random_state=42`.

## Test Metrics

- R-squared: 0.0600
- MAE: 1.0048
- RMSE: 1.3491

## Top Encoded Feature Importances

| Rank | Feature | Importance |
|---:|---|---:|
| 1 | response_time_minutes | 0.35743 |
| 2 | issue_hour | 0.20086 |
| 3 | Tenure Bucket_>90 | 0.02714 |
| 4 | Agent Shift_Morning | 0.02545 |
| 5 | Agent Shift_Evening | 0.02309 |
| 6 | issue_weekday_Tuesday | 0.02206 |
| 7 | Tenure Bucket_On Job Training | 0.02204 |
| 8 | issue_weekday_Wednesday | 0.02189 |
| 9 | issue_weekday_Thursday | 0.02184 |
| 10 | channel_name_Inbound | 0.01945 |
| 11 | issue_weekday_Sunday | 0.01765 |
| 12 | issue_weekday_Saturday | 0.01757 |
| 13 | Sub-category_Return request | 0.01656 |
| 14 | Tenure Bucket_31-60 | 0.01591 |
| 15 | issue_weekday_Monday | 0.01520 |
| 16 | channel_name_Outcall | 0.01475 |
| 17 | Sub-category_Reverse Pickup Enquiry | 0.01376 |
| 18 | category_Returns | 0.01235 |
| 19 | category_Order Related | 0.00998 |
| 20 | Sub-category_Fraudulent User | 0.00964 |

Impurity importance captures nonlinear split usage but can favor variables with more possible splits. Grouped permutation importance is therefore used for the final operational-variable ranking.
