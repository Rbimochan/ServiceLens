# Phase 5 - Structural Issue Analysis

## Structural Risks

| Risk | Affected fields | Evidence | Recommended handling |
|---|---|---|---|
| Extreme sparsity | connected_handling_time | 99.72% missing | Exclude from baseline use unless completeness improves |
| High sparsity | order_date_time, Customer_City, Product_category, Item_price and cleaned counterparts | About 79.96%-80.12% missing | Require explicit missingness strategy; avoid default baseline use |
| Sparse text | Customer Remarks, customer_remarks_clean | 66.54%-66.62% missing | Reserve for a separate text methodology |
| High-cardinality identifiers | Unique id, Order_id | 85,907 and 67,675 unique values | Preserve for traceability; exclude from predictors |
| High-cardinality categories | Agent_name/agent_name_clean; Customer_City/customer_city_clean | 1,371 and 1,782 unique values | Avoid naive one-hot encoding; assess leakage and generalization |
| Potential target leakage | CSAT Score, csat_score, low_csat_flag, high_csat_flag | Four representations of the same outcome | Select one target and exclude all other target variants |
| Potential temporal leakage | Survey_response_Date, survey_response_date_parsed, survey_day, survey_weekday | Survey timing follows the support interaction | Exclude from predictive inputs unless the prediction point permits them |
| Redundant raw/clean pairs | channel, category, sub-category, city, product, agent, supervisor, manager, tenure, shift, remarks | Original and cleaned versions coexist | Prefer cleaned fields for modeling and retain originals for audit |
| Redundant raw/parsed dates | Issue_reported at, issue_responded, Survey_response_Date and parsed versions | Same events represented twice | Use parsed/derived values operationally; preserve raw fields for traceability |
| Response-time quality risk | response_time_minutes, response_time_bucket, is_negative_response_time | Negative response durations are explicitly flagged | Filter or model with the quality flag according to later methodology |
| Serialized datetime dtype | Nine datetime/date columns | Stored as strings in CSV | Convert explicitly on every load |

## Readiness

The schema is usable for later EDA and modeling once target selection, datetime conversion, sparse-field handling, and redundant-field selection are made explicitly. No columns were removed in Phase 5.
