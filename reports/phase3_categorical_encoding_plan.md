# Phase 3 - Categorical Encoding Plan

## Purpose

This report prepares a categorical encoding strategy for future machine learning work. The raw dataset was inspected for categorical cardinality only. No model was trained, no final encoding was applied, and no processed dataset was created.

## Dataset Location

`data/raw/customer_support_tickets.csv`

## Categorical Column Cardinality

| Column | Unique Non-Missing Values | Missing Values | Cardinality Group | Recommended Encoding | Rationale |
|---|---:|---:|---|---|---|
| Unique id | 85,907 | 0 | High-cardinality ID | Exclude from baseline | Unique identifier; not useful as a predictive category. |
| channel_name | 3 | 0 | Low-cardinality | One-hot encoding | Small number of support channels. |
| category | 12 | 0 | Low-cardinality | One-hot encoding | Manageable number of issue categories. |
| Sub-category | 57 | 0 | Medium-cardinality | Frequency encoding or label/index encoding | More detailed issue categories; one-hot may be possible but should be reviewed. |
| Order_id | 67,675 | 18,232 | High-cardinality ID | Exclude from baseline | Identifier-like field with high cardinality and missingness. |
| Customer_City | 1,782 | 68,828 | High-cardinality | Exclude from baseline | High cardinality and very high missingness. |
| Product_category | 9 | 68,711 | Low-cardinality with high missingness | Use with caution; one-hot only if retained | Low unique count but very high missingness limits reliability. |
| Agent_name | 1,371 | 0 | High-cardinality name field | Frequency encoding or exclude from baseline | May capture operational patterns but risks overfitting and identity leakage. |
| Supervisor | 40 | 0 | Medium-cardinality | One-hot or label/index encoding | Moderate cardinality; useful for operational analysis. |
| Manager | 6 | 0 | Low-cardinality | One-hot encoding | Small number of manager groups. |
| Tenure Bucket | 5 | 0 | Low-cardinality / possibly ordinal | Label/index encoding if order is confirmed; otherwise one-hot | Bucket order may be meaningful but should be confirmed before ordinal encoding. |
| Agent Shift | 5 | 0 | Low-cardinality | One-hot encoding | Small number of shift categories. |

## Cardinality Groups

| Group | Columns |
|---|---|
| Low-cardinality | channel_name, category, Product_category, Manager, Tenure Bucket, Agent Shift |
| Medium-cardinality | Sub-category, Supervisor |
| High-cardinality | Unique id, Order_id, Customer_City, Agent_name |

## Recommended Baseline Encoding Strategy

| Encoding Method | Recommended Columns |
|---|---|
| One-hot encoding | channel_name, category, Manager, Agent Shift; Product_category only if retained after missing value handling |
| Label/index encoding | Tenure Bucket if ordinal order is confirmed; Supervisor if required by the ML pipeline |
| Frequency encoding | Sub-category; Agent_name only in a later non-baseline experiment |
| Exclude from baseline | Unique id, Order_id, Customer_City, Agent_name |

## Recommended Treatment

- Use one-hot encoding for stable low-cardinality categorical fields.
- Exclude ID fields from baseline models.
- Avoid high-cardinality name and location fields in the first baseline model unless a clear research reason is documented.
- Treat `Tenure Bucket` carefully because it may be ordinal; confirm the order before label/index encoding.
- Treat `Product_category` with caution because it has high missingness despite low cardinality.
- Keep encoding decisions separate from the raw dataset and apply them only in a future modeling pipeline.

## Risks

- High-cardinality fields can cause overfitting or create sparse feature matrices.
- Agent- or manager-related fields may encode operational hierarchy effects and should be interpreted carefully.
- Label/index encoding can introduce false ordering if applied to unordered categories.
- Frequency encoding should be fitted only on training data in future modeling to avoid leakage.
- Categorical encoding decisions may need revision after final missing value and cleaning decisions.

## Next Step

Use this encoding plan during future ML pipeline design. Do not encode the final dataset until the processed dataset design and train/test workflow are approved.
