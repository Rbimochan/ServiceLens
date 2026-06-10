# Phase 6 - Data Quality Report

## Dataset

The assessment covers 85,907 rows and 52 columns in `data/processed/customer_support_tickets_prepared.csv`. The dataset was read only; neither raw nor processed data was overwritten.

## Missing Values

Forty-two columns are complete and ten contain missing values. `connected_handling_time` is critical at 99.72% missing. City, product category, item price, and order timestamp fields are approximately 80% missing. Customer remarks are approximately 66.5% missing, while `Order_id` is 21.22% missing.

## Duplicates

There are no exact duplicate rows, duplicate `Unique id` values, or missing ticket IDs. `Unique id` is reliable for record identification.

## Invalid Values

CSAT values, issue hours, dates, and binary flags pass their domain checks. The significant invalid-value issue is 3,128 negative response times (3.64%), ranging from -1,437 to -20 minutes. The existing negative-response flag identifies all affected rows without mismatch.

## Empty Strings

No non-null exact empty strings or whitespace-only strings were detected. Original `Customer Remarks` contains 13,499 values with leading or trailing whitespace; the cleaned remarks field resolves that formatting issue. Blank CSV cells are represented as missing values.

## Label Consistency

No case-only or whitespace-only duplicate categorical labels were detected. The verified spelling issue `Home Appliences` appears in 1,300 rows in both the original and cleaned product-category columns. The correctly spelled alternative is absent.

## Recommended Cleaning Actions

1. Exclude `connected_handling_time` from primary analysis unless a better source is obtained.
2. Define explicit inclusion and missingness rules for city, product, price, order timestamp, and remarks fields.
3. Investigate negative response times before using raw response duration.
4. Standardize `Home Appliences` to `Home Appliances` in a controlled future cleaning step.
5. Prefer cleaned categorical/text fields and parsed datetime fields while retaining originals for audit.
6. Select one CSAT target per task and block all alternative target representations from predictors.
7. Treat agent and city fields carefully because of high cardinality and potential leakage.

## Limitations

- This phase checks structural and rule-based quality; it does not establish causal validity or business correctness for every record.
- Spelling detection combines normalization checks with a verified known label issue; it is not a general dictionary-based language audit.
- Negative response times were identified but not corrected because the correct source timestamp cannot be inferred safely.
- Missingness suitability depends on the later analytical objective.

No imputation, deletion, label correction, or other cleaning was performed.
