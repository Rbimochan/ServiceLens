# Phase 3 - Data Preparation Report

## Purpose

This report summarizes Phase 3 data preparation work for ServiceLens using verified outputs from V1-V9. It documents the preparation decisions applied before later EDA, modeling, and Tableau work. No new analysis beyond summarizing the existing preparation reports was performed for this final report.

## Source and Output Files

| Item | Path |
|---|---|
| Raw dataset | `data/raw/customer_support_tickets.csv` |
| Processed dataset | `data/processed/customer_support_tickets_prepared.csv` |
| Missing value strategy | `reports/phase3_missing_value_strategy.md` |
| Duplicate analysis | `reports/phase3_duplicate_analysis.md` |
| Datatype correction plan | `reports/phase3_datatype_correction.md` |
| Datetime engineering | `reports/phase3_datetime_engineering.md` |
| Ticket lifecycle features | `reports/phase3_ticket_lifecycle_features.md` |
| Text cleaning pipeline | `reports/phase3_text_cleaning_pipeline.md` |
| Categorical encoding plan | `reports/phase3_categorical_encoding_plan.md` |
| Feature engineering report | `reports/phase3_feature_engineering.md` |
| Processed dataset generation log | `reports/phase3_processed_dataset_generation.md` |

## V1-V9 Summary

| Version | Focus | Verified Outcome |
|---|---|---|
| V1 | Missing value strategy | Missing values and percentages documented; no imputation recommended at this stage. |
| V2 | Duplicate analysis | No full duplicate rows and no duplicate `Unique id` values found. |
| V3 | Datatype correction | Numeric, categorical, text, ID, and datetime roles documented. |
| V4 | Datetime engineering | Key datetime fields parsed successfully; negative response times identified. |
| V5 | Ticket lifecycle features | Safe lifecycle features planned from available timestamp columns only. |
| V6 | Text cleaning pipeline | `Customer Remarks` cleaning plan documented using basic whitespace/missing handling only. |
| V7 | Categorical encoding plan | Categorical fields grouped by cardinality and encoding recommendations documented. |
| V8 | Feature engineering | Safe engineered features and CSAT target variants documented. |
| V9 | Processed dataset generation | First prepared dataset generated with all rows retained and 32 new columns created. |

## Missing Value Strategy

The missing value assessment identified complete core operational and target fields, plus several sparse fields requiring caution.

| Strategy | Columns |
|---|---|
| Keep | Unique id, channel_name, category, Sub-category, Issue_reported at, issue_responded, Survey_response_Date, Agent_name, Supervisor, Manager, Tenure Bucket, Agent Shift, CSAT Score |
| Impute | None recommended at this stage |
| Drop later | order_date_time, Customer_City, Product_category, Item_price, connected_handling_time |
| Use with caution | Customer Remarks, Order_id |

High-missingness fields were not imputed in the prepared dataset. Instead, missingness flags were created for sparse fields to preserve information without fabricating values.

## Duplicate Findings

The duplicate analysis checked exact full-row duplicates and duplicate `Unique id` values.

| Check | Result |
|---|---:|
| Total rows checked | 85,907 |
| Full duplicate rows | 0 |
| Duplicate `Unique id` values | 0 |
| Blank `Unique id` values | 0 |

No duplicate rows were removed.

## Datatype Corrections

Datatype planning classified columns into numeric, categorical, text, ID, and datetime groups.

| Group | Columns |
|---|---|
| Numeric | Item_price, connected_handling_time, CSAT Score |
| Categorical | channel_name, category, Sub-category, Customer_City, Product_category, Agent_name, Supervisor, Manager, Tenure Bucket, Agent Shift |
| Text | Customer Remarks |
| ID | Unique id, Order_id |
| Datetime | order_date_time, Issue_reported at, issue_responded, Survey_response_Date |

In the prepared dataset, verified datetime fields were parsed into new parsed columns and `CSAT Score` was converted into the numeric target field `csat_score`. ID and name fields were preserved as text/categorical values.

## Datetime Issues

The datetime engineering step parsed the following fields successfully:

| Column | Parse Success | Parse Failed |
|---|---:|---:|
| Issue_reported at | 85,907 | 0 |
| issue_responded | 85,907 | 0 |
| Survey_response_Date | 85,907 | 0 |

`response_time_minutes` was calculated from `issue_responded - Issue_reported at`.

| Response Time Check | Value |
|---|---:|
| Valid response time values | 85,907 |
| Negative response times | 3,128 |
| Zero-minute response times | 2,448 |
| Positive response times | 80,331 |
| Median response time | 5.00 minutes |
| Mean response time | 136.89 minutes |

Negative response times were not removed. They were preserved and flagged using `is_negative_response_time`.

## Engineered Features

The prepared dataset includes safe engineered features derived only from verified available columns.

| Feature Type | Created Features |
|---|---|
| Parsed datetime fields | issue_reported_at_parsed, issue_responded_parsed, survey_response_date_parsed |
| Ticket lifecycle | response_time_minutes, response_time_bucket, issue_hour, issue_day, issue_weekday, survey_day, survey_weekday, is_negative_response_time |
| Missingness flags | is_customer_remarks_missing, is_order_id_missing, is_order_date_time_missing, is_customer_city_missing, is_product_category_missing, is_item_price_missing, is_connected_handling_time_missing |
| Text/categorical cleaning | customer_remarks_clean, channel_name_clean, category_clean, sub_category_clean, customer_city_clean, product_category_clean, agent_name_clean, supervisor_clean, manager_clean, tenure_bucket_clean, agent_shift_clean |
| CSAT target variants | csat_score, low_csat_flag, high_csat_flag |

No fake resolution time, priority, escalation flag, interaction count, or proposal-only variable was created.

## Processed Dataset Summary

| Metric | Value |
|---|---:|
| Processed dataset path | `data/processed/customer_support_tickets_prepared.csv` |
| Rows read from raw dataset | 85,907 |
| Rows written to processed dataset | 85,907 |
| Rows dropped | 0 |
| Original columns retained | 20 |
| New columns created | 32 |
| Final columns in processed dataset | 52 |

## Rows Flagged

| Flag / Issue | Count |
|---|---:|
| Negative response time rows | 3,128 |
| Customer Remarks missing | 57,234 |
| Order_id missing | 18,232 |
| order_date_time missing | 68,693 |
| Customer_City missing | 68,828 |
| Product_category missing | 68,711 |
| Item_price missing | 68,701 |
| connected_handling_time missing | 85,665 |
| Low CSAT flag rows | 15,071 |
| High CSAT flag rows | 70,836 |

## Limitations

- No rows were dropped, so invalid timestamp ordering remains present but flagged.
- Missing values were flagged but not imputed.
- Very sparse fields were retained for traceability, even if they may be excluded from later modeling.
- Response time features include negative and extreme values and should be used carefully.
- Categorical encoding was planned but not applied to the processed dataset.
- No model-specific transformations were applied.
- No fake resolution time, priority, escalation, interaction count, or unavailable proposal variables were created.

## Recommended Next Step

Use `data/processed/customer_support_tickets_prepared.csv` as the controlled input for the next phase after reviewing the schema. Any future row removal, imputation, feature exclusion, or model-specific encoding should be documented separately before EDA or modeling conclusions are reported.
