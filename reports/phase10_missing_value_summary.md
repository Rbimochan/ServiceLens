# Phase 10 - Missing Value Summary

Forty-two columns are complete and ten contain missing values.

| Field | Missing count | Missing % | Severity |
|---|---:|---:|---|
| connected_handling_time | 85,665 | 99.72% | Critical |
| Customer_City | 68,828 | 80.12% | Critical |
| customer_city_clean | 68,828 | 80.12% | Critical |
| Product_category | 68,711 | 79.98% | Critical |
| product_category_clean | 68,711 | 79.98% | Critical |
| Item_price | 68,701 | 79.97% | Critical |
| order_date_time | 68,693 | 79.96% | Critical |
| customer_remarks_clean | 57,234 | 66.62% | High |
| Customer Remarks | 57,165 | 66.54% | High |
| Order_id | 18,232 | 21.22% | Moderate |

## Recommended Handling

- Exclude `connected_handling_time` from baseline analysis unless a better source becomes available.
- Require an explicit missingness strategy before using city, product, price, or order timestamp.
- Reserve customer remarks for optional text analysis with missingness-bias disclosure.
- Preserve missingness indicators where they provide documented context.
- Do not impute identifiers merely to make them complete.
