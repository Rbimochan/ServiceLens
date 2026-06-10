# Phase 4 - Feature Variables

## Purpose

This report documents usable predictor variables for future ServiceLens modeling and analysis. It lists available features from the processed dataset, excludes sparse or problematic fields from the baseline feature set, and explains the expected relationship of each usable feature group to CSAT.

## Dataset

`data/processed/customer_support_tickets_prepared.csv`

## Recommended Baseline Feature Variables

| Feature | Type | Expected Relationship to CSAT | Notes |
|---|---|---|---|
| `channel_name_clean` | Categorical | Different support channels may be associated with different customer satisfaction patterns. | Low-cardinality cleaned channel field. |
| `category_clean` | Categorical | Main issue category may influence satisfaction because issue types can vary in complexity and urgency. | Low-cardinality cleaned issue category. |
| `sub_category_clean` | Categorical | Detailed issue type may explain more specific satisfaction differences. | Medium-cardinality; may require careful encoding. |
| `manager_clean` | Categorical | Management group may reflect operational process differences affecting CSAT. | Low-cardinality operational grouping. |
| `supervisor_clean` | Categorical | Supervisor grouping may reflect team-level service patterns. | Moderate-cardinality operational grouping. |
| `tenure_bucket_clean` | Categorical | Agent tenure group may relate to experience and service quality. | May be ordinal, but ordering should be confirmed before ordinal encoding. |
| `agent_shift_clean` | Categorical | Agent shift may reflect workload, timing, or staffing conditions that affect satisfaction. | Low-cardinality shift feature. |
| `issue_hour` | Numeric | Time of day may relate to customer demand, queue pressure, and response experience. | Derived from verified issue timestamp. |
| `issue_weekday` | Categorical | Day of week may capture operational demand or staffing patterns. | Derived from verified issue timestamp. |
| `response_time_minutes` | Numeric | Longer response times may be associated with lower satisfaction. | Use with `is_negative_response_time`; contains invalid negative values. |
| `response_time_bucket` | Categorical | Bucketed response time may capture service speed categories more safely than raw minutes. | Includes a `negative` bucket. |
| `is_negative_response_time` | Categorical | Flags timestamp-ordering problems that may indicate invalid operational timing data. | Quality flag; should be interpreted carefully. |
| `is_customer_remarks_missing` | Categorical | Missing remarks may reflect differences in survey behavior or ticket context. | Missingness flag, not text content. |
| `is_order_id_missing` | Categorical | Missing order identifiers may indicate tickets not tied to a specific order. | Missingness flag. |
| `is_order_date_time_missing` | Categorical | Missing order dates may signal incomplete order context. | Missingness flag. |
| `is_customer_city_missing` | Categorical | Missing customer city may reflect incomplete profile or order information. | Missingness flag. |
| `is_product_category_missing` | Categorical | Missing product category may reflect incomplete product context. | Missingness flag. |
| `is_item_price_missing` | Categorical | Missing item price may reflect incomplete order context. | Missingness flag. |
| `is_connected_handling_time_missing` | Categorical | Missing handling time may reflect incomplete operational logging. | Missingness flag. |

## Optional / Use With Caution Features

| Feature | Reason for Caution | Possible Use |
|---|---|---|
| `product_category_clean` | Very high missingness despite low cardinality. | Use only after documenting missingness impact. |
| `customer_city_clean` | Very high missingness and high cardinality. | Avoid baseline; possible later geographic analysis if justified. |
| `agent_name_clean` | High cardinality and possible overfitting or identity leakage. | Avoid baseline; possible later operational analysis with controls. |
| `customer_remarks_clean` | High missingness and free text requiring separate NLP assumptions. | Avoid baseline ML unless a later text-analysis phase is approved. |
| `Item_price` / cleaned numeric version if created later | Very high missingness. | Use only after missingness treatment is justified. |
| `connected_handling_time` / cleaned numeric version if created later | Almost entirely missing. | Generally exclude unless data completeness improves. |
| `survey_day` and `survey_weekday` | Survey timing may occur after the target outcome process. | Use cautiously to avoid temporal leakage in predictive modeling. |

## Excluded From Baseline Features

| Field | Exclusion Reason |
|---|---|
| `Unique id` | Identifier; not a meaningful predictor. |
| `Order_id` | Identifier-like field with high cardinality and missingness. |
| `CSAT Score` | Original target variable, not a predictor. |
| `csat_score` | Target variable, not a predictor. |
| `low_csat_flag` | Target variant, not a predictor. |
| `high_csat_flag` | Target variant, not a predictor. |
| `Issue_reported at` | Raw timestamp; derived features should be used instead. |
| `issue_responded` | Raw timestamp; response-time features should be used instead. |
| `Survey_response_Date` | Raw survey date; use cautiously through derived fields only if justified. |
| `issue_reported_at_parsed` | Parsed timestamp retained for traceability; use derived fields for modeling. |
| `issue_responded_parsed` | Parsed timestamp retained for traceability; use derived response-time features for modeling. |
| `survey_response_date_parsed` | Parsed survey date retained for traceability; avoid baseline predictive use unless justified. |

## Recommended Baseline Predictor Set

For an initial baseline model or analysis design, prefer:

- `channel_name_clean`
- `category_clean`
- `sub_category_clean`
- `manager_clean`
- `supervisor_clean`
- `tenure_bucket_clean`
- `agent_shift_clean`
- `issue_hour`
- `issue_weekday`
- `response_time_bucket`
- `is_negative_response_time`
- sparse-field missingness flags

Use `response_time_minutes` only with documented handling of negative response times and outliers.

## Notes

- Only fields actually available in the processed dataset are listed.
- No fake proposal variables were added.
- Encoding, feature selection, and model training will be handled in later phases.
- Target variables must be excluded from predictor inputs to avoid leakage.
