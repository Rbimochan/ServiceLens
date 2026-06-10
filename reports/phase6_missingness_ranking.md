# Phase 6 - Missingness Ranking

| Rank | Column | Missing count | Missing % | Primary-analysis assessment |
|---:|---|---:|---:|---|
| 1 | connected_handling_time | 85,665 | 99.72% | Unsuitable by default |
| 2 | Customer_City | 68,828 | 80.12% | Unsuitable by default |
| 2 | customer_city_clean | 68,828 | 80.12% | Unsuitable by default |
| 4 | Product_category | 68,711 | 79.98% | Unsuitable by default |
| 4 | product_category_clean | 68,711 | 79.98% | Unsuitable by default |
| 6 | Item_price | 68,701 | 79.97% | Unsuitable by default |
| 7 | order_date_time | 68,693 | 79.96% | Unsuitable by default |
| 8 | customer_remarks_clean | 57,234 | 66.62% | Text-specific use only |
| 9 | Customer Remarks | 57,165 | 66.54% | Text-specific use only |
| 10 | Order_id | 18,232 | 21.22% | Reference field; not a predictor |

The remaining 42 columns are tied with 0 missing values and are complete from a missingness perspective. Completeness alone does not make identifiers, targets, leakage fields, or redundant fields safe predictors.

## Modeling Guidance

- Structurally complete candidate features include cleaned channel, category, sub-category, manager, supervisor, tenure, shift, issue timing, response-time fields, and missingness flags.
- Critical-missingness fields should be excluded from a primary baseline unless a later methodology explicitly justifies their use.
- Text fields require a separate NLP methodology and missingness-bias assessment.
- Target variants and identifiers remain unsuitable as predictors despite complete values.
