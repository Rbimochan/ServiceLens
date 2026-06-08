# Phase 3 - Datatype Correction Plan

## Purpose

This report identifies current datatype expectations and planned datatype corrections for the raw customer support ticket dataset. The raw dataset was inspected for planning only and was not modified.

## Dataset Location

`data/raw/customer_support_tickets.csv`

## Datatype Classification

| Column | Observed/Inferred Type | Intended Type | Column Role | Planned Correction |
|---|---|---|---|---|
| Unique id | Text/categorical | String or categorical | ID | Keep as identifier text; do not convert to numeric. |
| channel_name | Text/categorical | Categorical | Categorical | Keep as categorical feature. |
| category | Text/categorical | Categorical | Categorical | Keep as categorical feature. |
| Sub-category | Text/categorical | Categorical | Categorical | Keep as categorical feature. |
| Customer Remarks | Text/categorical | Text | Text | Keep as text; use only if later text analysis is justified. |
| Order_id | Text/categorical | String or categorical | ID | Keep as identifier text; do not use as numeric feature. |
| order_date_time | Text/categorical | Datetime | Datetime | Convert to datetime later if retained after missing value review. |
| Issue_reported at | Text/categorical | Datetime | Datetime | Convert to datetime during cleaning. |
| issue_responded | Text/categorical | Datetime | Datetime | Convert to datetime during cleaning. |
| Survey_response_Date | Text/categorical | Datetime | Datetime | Convert to datetime during cleaning. |
| Customer_City | Text/categorical | Categorical | Categorical | Keep as categorical if retained after missing value review. |
| Product_category | Text/categorical | Categorical | Categorical | Keep as categorical if retained after missing value review. |
| Item_price | Numeric-like | Numeric | Numeric | Convert to numeric if retained after missing value review. |
| connected_handling_time | Numeric-like | Numeric | Numeric | Convert to numeric only if retained; high missingness requires caution. |
| Agent_name | Text/categorical | Categorical | Name/category | Keep as categorical/text. |
| Supervisor | Text/categorical | Categorical | Name/category | Keep as categorical/text. |
| Manager | Text/categorical | Categorical | Name/category | Keep as categorical/text. |
| Tenure Bucket | Text/categorical | Ordered categorical | Categorical | Keep as categorical; consider ordering only if category meaning is confirmed. |
| Agent Shift | Text/categorical | Categorical | Categorical | Keep as categorical feature. |
| CSAT Score | Numeric-like | Numeric | Target variable | Convert to numeric for later analysis and modeling. |

## Recommended Datatype Groups

| Group | Columns |
|---|---|
| Numeric | Item_price, connected_handling_time, CSAT Score |
| Categorical | channel_name, category, Sub-category, Customer_City, Product_category, Agent_name, Supervisor, Manager, Tenure Bucket, Agent Shift |
| Text | Customer Remarks |
| ID | Unique id, Order_id |
| Datetime | order_date_time, Issue_reported at, issue_responded, Survey_response_Date |

## Correction Plan

1. Convert `CSAT Score` to numeric before target analysis.
2. Convert `Item_price` and `connected_handling_time` to numeric only if they are retained after missing value handling decisions.
3. Convert `Issue_reported at`, `issue_responded`, and `Survey_response_Date` to datetime during cleaning.
4. Convert `order_date_time` to datetime only if it is retained after missing value review.
5. Keep IDs, names, categories, and free-text fields as string/categorical values.
6. Do not permanently modify the raw dataset; apply conversions only in a future prepared working copy.

## Risks

- Date parsing may require explicit format handling because date columns are currently text-like.
- High-missingness numeric and datetime fields should not be converted and used blindly.
- ID fields may look structured but should not be treated as numeric predictors.
- `Tenure Bucket` may be ordinal, but ordering should be confirmed before encoding.

## Next Step

Use this datatype plan during the later cleaning workflow. Do not create a processed dataset until missing value, duplicate, and datatype handling rules are combined into a final preparation plan.
