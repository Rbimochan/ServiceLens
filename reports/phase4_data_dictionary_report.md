# Phase 4 - Data Dictionary Report

## Purpose

This report summarizes completion of the ServiceLens Phase 4 data dictionary. It consolidates the verified column inventory, business definitions, datatype classifications, variable roles, targets, candidate features, metadata, text fields, and master dictionary without performing new analysis.

## Dataset

`data/processed/customer_support_tickets_prepared.csv`

## Completion Summary

- Dataset rows documented: 85,907
- Dataset columns documented: 52
- Original retained columns: 20
- Engineered preparation columns: 32
- Required Phase 4 reports completed: 10

## Datatype Summary

| Datatype | Column Count |
|---|---:|
| Categorical | 33 |
| Datetime | 9 |
| Identifier | 2 |
| Numeric | 6 |
| Text | 2 |
| **Total** | **52** |

## Variable Role Summary

| Variable Role | Column Count |
|---|---:|
| Target | 4 |
| Predictor | 12 |
| Metadata | 5 |
| Identifier | 2 |
| Derived Feature | 29 |
| **Total** | **52** |

## Target Variables

- `CSAT Score`: original customer satisfaction rating.
- `csat_score`: standardized numeric CSAT target.
- `low_csat_flag`: binary target for CSAT scores from 1 through 3.
- `high_csat_flag`: binary target for CSAT scores from 4 through 5.

Only one target should be selected for an individual future model to prevent target leakage.

## Feature Documentation

The recommended baseline feature set uses fields actually present in the processed dataset, including cleaned support channel, issue category, sub-category, management grouping, tenure, shift, issue timing, response-time, and missingness flags. Sparse, high-cardinality, identifier, raw timestamp, target, and text fields are excluded from the baseline or marked for cautious use.

## Metadata And Audit Fields

Identifiers are preserved for traceability rather than modeling. Personnel and hierarchy fields are documented with overfitting, identity-leakage, and interpretation cautions. Parsed timestamps and missingness or timing-quality flags support auditability and later quality assessment.

## Text Fields

`Customer Remarks` and `customer_remarks_clean` are the two documented free-text fields. The cleaned field is the preferred future NLP input, but 66.62% of its values are missing. No NLP was performed in Phase 4.

## Master Dictionary

`reports/phase4_master_data_dictionary.md` documents all 52 processed columns with:

- column name
- business meaning
- datatype
- variable role
- missing percentage
- implementation or modeling notes

## Phase 5 Readiness

Phase 4 is ready for completion checking. The documented schema can support later structure analysis, data-quality review, CSAT modeling, and exploratory analysis. Readiness requires the Phase 4 completion checker to pass all required checks.
