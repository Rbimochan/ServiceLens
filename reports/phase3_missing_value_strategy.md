# Phase 3 - Missing Value Strategy

## Purpose

This report documents the missing value profile of the raw customer support ticket dataset and recommends a handling strategy for later data preparation. The raw dataset was read for assessment only and was not modified.

## Dataset Location

`data/raw/customer_support_tickets.csv`

## Missing Value Table

| Column | Missing Values | Missing % | Recommended Strategy | Rationale |
|---|---:|---:|---|---|
| Unique id | 0 | 0.00% | Keep | Complete identifier field. |
| channel_name | 0 | 0.00% | Keep | Complete support channel feature. |
| category | 0 | 0.00% | Keep | Complete issue category feature. |
| Sub-category | 0 | 0.00% | Keep | Complete detailed issue category feature. |
| Customer Remarks | 57,234 | 66.62% | Use with caution | High missingness; may still provide useful text where available but should not be required for core models. |
| Order_id | 18,232 | 21.22% | Use with caution | Moderate missingness; useful as an identifier but not suitable as a direct predictive feature without review. |
| order_date_time | 68,693 | 79.96% | Drop later | Very high missingness; weak candidate for reliable datetime-derived features unless a clear business need is found. |
| Issue_reported at | 0 | 0.00% | Keep | Complete timestamp for issue reporting. |
| issue_responded | 0 | 0.00% | Keep | Complete timestamp for issue response. |
| Survey_response_Date | 0 | 0.00% | Keep | Complete survey response date. |
| Customer_City | 68,828 | 80.12% | Drop later | Very high missingness; likely unreliable for location-based analysis. |
| Product_category | 68,711 | 79.98% | Drop later | Very high missingness; likely unreliable for product-based segmentation. |
| Item_price | 68,701 | 79.97% | Drop later | Very high missingness; imputation would risk distorting price-related analysis. |
| connected_handling_time | 85,665 | 99.72% | Drop later | Almost entirely missing; not reliable for analysis. |
| Agent_name | 0 | 0.00% | Keep | Complete agent field; may support later operational analysis. |
| Supervisor | 0 | 0.00% | Keep | Complete supervisor field. |
| Manager | 0 | 0.00% | Keep | Complete manager field. |
| Tenure Bucket | 0 | 0.00% | Keep | Complete tenure grouping field. |
| Agent Shift | 0 | 0.00% | Keep | Complete shift field. |
| CSAT Score | 0 | 0.00% | Keep | Complete expected target variable for later analysis. |

## Recommended Handling Strategy

| Strategy | Columns |
|---|---|
| Keep | Unique id, channel_name, category, Sub-category, Issue_reported at, issue_responded, Survey_response_Date, Agent_name, Supervisor, Manager, Tenure Bucket, Agent Shift, CSAT Score |
| Impute | None recommended at this stage |
| Drop later | order_date_time, Customer_City, Product_category, Item_price, connected_handling_time |
| Use with caution | Customer Remarks, Order_id |

## Risks

- High-missingness fields may reduce reliability if used without careful justification.
- Imputing fields with around 80% or higher missingness could create misleading patterns.
- `Customer Remarks` may be useful for text analysis, but the high missing rate means it should not be required for baseline models.
- `Order_id` is an identifier-like field and should not be treated as a predictive feature without further review.
- Dropping fields should happen later in the data preparation workflow, after confirming modeling and reporting requirements.

## Next Step

Proceed to Phase 3 data preparation planning by documenting which fields will be retained for initial structure analysis. Do not create a processed dataset until the full preparation strategy is approved.
