# Phase 4 - Metadata Fields

## Purpose

This report documents metadata, reference, and audit fields in the processed ServiceLens dataset. It classifies whether each field should be treated as a modeling feature, reference field, or audit field.

## Dataset

`data/processed/customer_support_tickets_prepared.csv`

## Classification Definitions

| Classification | Meaning |
|---|---|
| Modeling feature | Field may be considered as a future predictor if modeling assumptions and leakage risks are addressed. |
| Reference field | Field is mainly preserved for traceability, lookup, or record identification. |
| Audit field | Field supports quality checks, validation, or process auditing rather than direct baseline modeling. |

## Metadata Field Classification

| Field | Classification | Rationale |
|---|---|---|
| `Unique id` | Reference field | Unique ticket identifier used to trace records; should not be used as a modeling predictor. |
| `Order_id` | Reference field | Order identifier used to link ticket context; high cardinality and missingness make it unsuitable for baseline modeling. |
| `Agent_name` | Modeling feature | Agent assignment may reflect operational patterns, but high cardinality creates overfitting and fairness risks. |
| `Supervisor` | Modeling feature | Supervisor grouping may reflect team-level operational patterns. |
| `Manager` | Modeling feature | Manager grouping may reflect higher-level operational differences. |
| `Agent_name_clean` | Modeling feature | Cleaned agent name may be used only with caution because of high cardinality and identity leakage risk. |
| `supervisor_clean` | Modeling feature | Cleaned supervisor category can be considered for operational analysis or modeling. |
| `manager_clean` | Modeling feature | Cleaned manager category can be considered for operational analysis or modeling. |
| `Issue_reported at` | Reference field | Original raw issue timestamp retained for traceability; derived fields should be used for modeling. |
| `issue_responded` | Reference field | Original raw response timestamp retained for traceability; response-time features should be used for modeling. |
| `Survey_response_Date` | Reference field | Original survey response date retained for traceability. |
| `issue_reported_at_parsed` | Audit field | Parsed timestamp supports validation and derivation of timing features. |
| `issue_responded_parsed` | Audit field | Parsed response timestamp supports validation and response-time calculation. |
| `survey_response_date_parsed` | Audit field | Parsed survey date supports validation of survey timing. |
| `is_negative_response_time` | Audit field | Quality flag identifying invalid timestamp ordering. |
| `is_customer_remarks_missing` | Audit field | Missingness flag documenting whether customer remarks are absent. |
| `is_order_id_missing` | Audit field | Missingness flag documenting whether order ID is absent. |
| `is_order_date_time_missing` | Audit field | Missingness flag documenting whether order timestamp is absent. |
| `is_customer_city_missing` | Audit field | Missingness flag documenting whether customer city is absent. |
| `is_product_category_missing` | Audit field | Missingness flag documenting whether product category is absent. |
| `is_item_price_missing` | Audit field | Missingness flag documenting whether item price is absent. |
| `is_connected_handling_time_missing` | Audit field | Missingness flag documenting whether handling time is absent. |

## Recommended Handling

- Preserve reference fields for record traceability.
- Use audit fields to explain data quality conditions and preparation decisions.
- Treat agent, supervisor, and manager fields carefully because they can encode operational hierarchy and personnel-level effects.
- Exclude `Unique id` and `Order_id` from baseline modeling.
- Prefer derived timing fields over raw timestamp fields for analysis or modeling.

## Risks

- Personnel-related fields may create overfitting, identity leakage, or sensitive operational interpretations.
- Reference identifiers can create misleading model behavior if used as predictors.
- Audit flags may be useful, but their interpretation should be tied to data quality limitations rather than causal claims.
