# Phase 4 - Business Meaning

## Purpose

This report defines the plain-English business meaning of each column in the processed ServiceLens dataset. It maps each field to customer support operations context only. Variable roles, modeling use, and statistical interpretation are not classified in this step.

## Dataset

`data/processed/customer_support_tickets_prepared.csv`

## Business Meaning Dictionary

| Column | Business Meaning |
|---|---|
| `Unique id` | Unique ticket record identifier assigned to each support interaction. |
| `channel_name` | Support channel used by the customer to contact support. |
| `category` | Main issue category assigned to the customer support ticket. |
| `Sub-category` | More detailed issue category within the main support category. |
| `Customer Remarks` | Original free-text comment or remark provided by the customer, when available. |
| `Order_id` | Identifier for the customer order associated with the support ticket, when available. |
| `order_date_time` | Original date and time associated with the customer order, when available. |
| `Issue_reported at` | Original timestamp when the customer support issue was reported. |
| `issue_responded` | Original timestamp when the support team responded to the issue. |
| `Survey_response_Date` | Original date when the customer submitted the satisfaction survey response. |
| `Customer_City` | Customer city associated with the support ticket, when available. |
| `Product_category` | Product category linked to the customer order or support issue, when available. |
| `Item_price` | Price of the item associated with the support ticket, when available. |
| `connected_handling_time` | Recorded support handling duration, when available. |
| `Agent_name` | Name of the support agent associated with the ticket. |
| `Supervisor` | Supervisor responsible for the support agent or ticket handling team. |
| `Manager` | Manager responsible for the supervisor, support agent, or operational team. |
| `Tenure Bucket` | Grouping that describes the support agent's experience or tenure range. |
| `Agent Shift` | Work shift during which the support agent handled or was assigned the ticket. |
| `CSAT Score` | Original customer satisfaction rating recorded from the survey. |
| `issue_reported_at_parsed` | Standardized parsed version of the issue reported timestamp. |
| `issue_responded_parsed` | Standardized parsed version of the issue response timestamp. |
| `survey_response_date_parsed` | Standardized parsed version of the survey response date. |
| `response_time_minutes` | Time difference in minutes between issue reporting and support response. |
| `response_time_bucket` | Grouped response time band used to make response timing easier to review. |
| `issue_hour` | Hour of day when the support issue was reported. |
| `issue_day` | Calendar date when the support issue was reported. |
| `issue_weekday` | Day of week when the support issue was reported. |
| `survey_day` | Calendar date when the customer survey response was submitted. |
| `survey_weekday` | Day of week when the customer survey response was submitted. |
| `is_negative_response_time` | Flag showing whether the response timestamp appears earlier than the issue reported timestamp. |
| `is_customer_remarks_missing` | Flag showing whether customer remarks are missing for the ticket. |
| `is_order_id_missing` | Flag showing whether the order identifier is missing for the ticket. |
| `is_order_date_time_missing` | Flag showing whether the order date/time is missing for the ticket. |
| `is_customer_city_missing` | Flag showing whether customer city information is missing. |
| `is_product_category_missing` | Flag showing whether product category information is missing. |
| `is_item_price_missing` | Flag showing whether item price information is missing. |
| `is_connected_handling_time_missing` | Flag showing whether connected handling time information is missing. |
| `customer_remarks_clean` | Basic cleaned version of customer remarks after whitespace cleanup and missing-value standardization. |
| `channel_name_clean` | Basic cleaned version of support channel name. |
| `category_clean` | Basic cleaned version of the main issue category. |
| `sub_category_clean` | Basic cleaned version of the detailed issue sub-category. |
| `customer_city_clean` | Basic cleaned version of customer city information. |
| `product_category_clean` | Basic cleaned version of product category information. |
| `agent_name_clean` | Basic cleaned version of support agent name. |
| `supervisor_clean` | Basic cleaned version of supervisor name. |
| `manager_clean` | Basic cleaned version of manager name. |
| `tenure_bucket_clean` | Basic cleaned version of the agent tenure grouping. |
| `agent_shift_clean` | Basic cleaned version of the agent shift grouping. |
| `csat_score` | Numeric standardized version of the customer satisfaction score. |
| `low_csat_flag` | Flag identifying tickets with lower customer satisfaction scores. |
| `high_csat_flag` | Flag identifying tickets with higher customer satisfaction scores. |

## Notes

- This document explains operational meaning only.
- Variable roles and modeling decisions will be documented in a later Phase 4 step.
- Generated fields are explained based on the Phase 3 preparation reports.
