# Phase 10 - Data Dictionary Summary

Phase 4 documented all 52 prepared columns.

## Variable Roles

| Role | Columns |
|---|---:|
| Target | 4 |
| Predictor | 12 |
| Metadata | 5 |
| Identifier | 2 |
| Derived Feature | 29 |

## Targets

- `CSAT Score`: original satisfaction rating.
- `csat_score`: standardized numeric form.
- `low_csat_flag`: engineered flag for scores 1–3.
- `high_csat_flag`: engineered flag for scores 4–5.

Only one target representation should be used in a model. Phase 8 defines true low CSAT separately as scores 1–2.

## Candidate Features

The most usable structured predictors include cleaned channel, category, sub-category, supervisor, manager, tenure bucket, shift, issue timing, response time, response-time bucket, and missingness indicators.

## Metadata And Identifiers

`Unique id` and `Order_id` support traceability and should not be predictors. Raw and parsed timestamps support audit and feature derivation. Personnel hierarchy fields require careful interpretation and leakage controls.

## Text Fields

`Customer Remarks` and `customer_remarks_clean` are the free-text fields. The cleaned field is preferred for future NLP, but 66.62% is missing.

The complete dictionary is available in `reports/phase4_master_data_dictionary.md`.
