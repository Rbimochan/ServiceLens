# Customer Support Tickets Analysis

Source: `data/raw/customer_support_tickets.csv`

## Dataset Overview

- Rows: 85,907 tickets
- Columns: 20
- Date range by `Issue_reported at`: 2023-07-28 20:42 to 2023-08-31 23:58
- Duplicate `Unique id` values: 0
- Overall average CSAT: 4.242 / 5
- Median CSAT: 5
- Low CSAT rate, scores 1-2: 14.57%
- High CSAT rate, scores 4-5: 82.46%

## Data Quality Notes

Several fields are too sparse for primary analysis:

| Field | Missing |
|---|---:|
| `connected_handling_time` | 99.72% |
| `Customer_City` | 80.12% |
| `Product_category` | 79.98% |
| `Item_price` | 79.97% |
| `order_date_time` | 79.96% |
| `Customer Remarks` | 66.54% |
| `Order_id` | 21.22% |

Timestamp fields `Issue_reported at`, `issue_responded`, and `Survey_response_Date` are complete and parse cleanly. However, 3,128 tickets have response timestamps earlier than issue timestamps, so response-time analysis should treat those rows as data-quality exceptions.

## Channel Performance

| Channel | Tickets | Avg CSAT | Low CSAT % | High CSAT % | Median Response Min |
|---|---:|---:|---:|---:|---:|
| Inbound | 68,142 | 4.251 | 14.32 | 82.70 | 5 |
| Outcall | 14,742 | 4.270 | 13.95 | 83.18 | 5 |
| Email | 3,023 | 3.899 | 23.16 | 73.47 | 6 |

Email is the weakest channel, with much higher low-CSAT share despite similar median response time.

## Category Performance

| Category | Tickets | Avg CSAT | Low CSAT % |
|---|---:|---:|---:|
| Returns | 44,097 | 4.346 | 12.18 |
| Order Related | 23,215 | 4.096 | 17.88 |
| Refund Related | 4,550 | 4.227 | 15.01 |
| Product Queries | 3,692 | 4.040 | 18.26 |
| Shopzilla Related | 2,792 | 4.307 | 13.32 |
| Payments related | 2,327 | 4.355 | 11.73 |
| Feedback | 2,294 | 4.159 | 16.83 |
| Cancellation | 2,212 | 3.991 | 21.47 |

Cancellation has the weakest CSAT among major categories. Order Related and Product Queries are also below the overall average and have elevated low-CSAT rates.

## Sub-category Watchlist

Lowest-performing sub-categories with at least 500 tickets:

| Sub-category | Tickets | Avg CSAT | Low CSAT % |
|---|---:|---:|---:|
| Seller Cancelled Order | 1,059 | 3.585 | 30.41 |
| Installation/demo | 4,116 | 3.883 | 22.67 |
| Not Needed | 1,920 | 3.922 | 23.07 |
| Delayed | 7,388 | 4.012 | 19.82 |
| Product Specific Information | 3,589 | 4.044 | 18.17 |
| Exchange / Replacement | 896 | 4.071 | 18.08 |
| Service Centres Related | 1,875 | 4.118 | 18.13 |

The highest-impact fixes are likely in `Delayed`, `Installation/demo`, and `Product Specific Information` because they combine high ticket volume with below-average CSAT.

## Response Time Impact

For non-negative response times:

- Median response time: 6 minutes
- 75th percentile: 39 minutes
- 90th percentile: 432 minutes
- 95th percentile: 1,124 minutes
- 99th percentile: 3,047 minutes

CSAT declines as response time increases:

| Response Bucket | Tickets | Avg CSAT | Low CSAT % |
|---|---:|---:|---:|
| 0-5 min | 38,038 | 4.485 | 8.81 |
| 5-15 min | 13,886 | 4.258 | 13.88 |
| 15-30 min | 5,864 | 4.020 | 19.63 |
| 30-60 min | 4,484 | 3.961 | 21.07 |
| 1-2h | 3,887 | 3.975 | 20.71 |
| 2-4h | 3,512 | 3.913 | 22.64 |
| 4-24h | 7,783 | 3.820 | 24.57 |
| >24h | 2,877 | 3.395 | 36.32 |

The strongest operational lever appears to be keeping responses under 15 minutes, and especially avoiding responses over 4 hours.

## Team and Staffing Signals

By tenure:

| Tenure Bucket | Tickets | Avg CSAT | Low CSAT % |
|---|---:|---:|---:|
| >90 | 30,660 | 4.273 | 14.00 |
| On Job Training | 25,523 | 4.145 | 16.64 |
| 31-60 | 11,665 | 4.296 | 13.37 |
| 0-30 | 11,318 | 4.259 | 14.07 |
| 61-90 | 6,741 | 4.347 | 12.16 |

On Job Training agents handle a large volume and have the weakest CSAT, suggesting training-stage coaching and routing rules may matter.

By shift:

| Shift | Tickets | Avg CSAT | Low CSAT % |
|---|---:|---:|---:|
| Morning | 41,426 | 4.189 | 15.75 |
| Evening | 33,677 | 4.276 | 13.73 |
| Afternoon | 5,840 | 4.292 | 13.66 |
| Split | 3,648 | 4.427 | 10.33 |
| Night | 1,316 | 4.289 | 14.44 |

Morning shift has the largest volume and the weakest shift-level CSAT.

## Product Category Caveat

`Product_category` is missing for about 80% of tickets, so these numbers should be treated as directional only. Among rows where product category exists, lower CSAT appears in:

| Product Category | Tickets | Avg CSAT | Low CSAT % |
|---|---:|---:|---:|
| GiftCard | 26 | 3.231 | 42.31 |
| Furniture | 471 | 3.620 | 30.36 |
| Mobile | 1,758 | 3.646 | 30.15 |
| Home Appliences | 1,300 | 3.702 | 28.62 |
| Home | 1,328 | 3.955 | 22.06 |

Mobile and Home Appliences are worth investigating because they have enough volume and weak CSAT. `Home Appliences` also appears misspelled and should likely be standardized to `Home Appliances`.

## Recommended Next Steps

1. Fix timestamp quality before using response time in modeling: flag or remove rows where `issue_responded` is earlier than `Issue_reported at`.
2. Prioritize root-cause analysis for `Seller Cancelled Order`, `Installation/demo`, `Delayed`, and `Product Specific Information`.
3. Investigate Email support separately because it has a much higher low-CSAT rate than Inbound and Outcall.
4. Segment On Job Training agents by category and supervisor to identify coaching or routing problems.
5. Improve completeness of product/order fields if future modeling depends on customer, order, product, or price signals.
6. For a predictive model, start with complete fields: channel, category, sub-category, parsed response time, agent/supervisor/manager, tenure bucket, shift, issue hour/day, and CSAT target.
