# Phase 5 - Data Structure Report

## Dataset Structure

The processed ServiceLens dataset contains 85,907 rows and 52 columns and uses 67.66 MiB of deep pandas memory. It loads from CSV with 36 string, 14 integer, and 2 float columns.

## Field Groups

- Numeric storage: 16 columns, including 14 integers and 2 floats.
- Conceptual categorical: 33 columns, including integer-encoded binary indicators.
- Datetime/date: 9 columns; all non-null values parse successfully.
- Free text: 2 columns, both more than 66% missing.
- Identifiers: 2 columns.

## Datatype Findings

Numeric fields and identifiers load with appropriate pandas types. Datetime fields load as strings because CSV does not retain datetime metadata, so explicit conversion is required after loading. No mixed-type columns or non-null datetime conversion failures were detected.

## Structural Risks

- `connected_handling_time` is 99.72% missing.
- Several order, city, product, and price fields are about 80% missing.
- Agent and city fields have high cardinality.
- Raw and cleaned columns, raw and parsed timestamps, and multiple CSAT target variants are intentionally redundant.
- Target variants and survey-timing fields present leakage risks if selected incorrectly.

## Schema Readiness

All 52 columns are documented in `reports/phase5_schema_summary.md` with actual dtype, expected type, role, missingness, and structural notes. The dataset is structurally ready for Phase 6 data-quality assessment, with explicit attention required for datetime conversion, sparse fields, high cardinality, redundancy, and leakage.

No EDA, modeling, NLP, column removal, or dataset modification was performed.
