# Phase 10 - Structure Summary

## Schema

The prepared dataset has 85,907 rows, 52 columns, and a deep pandas memory footprint of 67.66 MiB.

## Actual CSV Storage Types

| Pandas dtype | Columns |
|---|---:|
| String | 36 |
| Integer | 14 |
| Float | 2 |

## Conceptual Datatypes

| Business datatype | Columns |
|---|---:|
| Categorical | 33 |
| Datetime | 9 |
| Numeric | 6 |
| Text | 2 |
| Identifier | 2 |

## Structural Interpretation

- Numeric fields load with numeric pandas types.
- Binary quality, missingness, and target flags are stored as integers but are conceptually categorical.
- Datetime fields are serialized as strings in CSV and must be converted explicitly after loading.
- All nine conceptual datetime fields parse successfully.
- Agent and city fields are high-cardinality.
- Original/cleaned and raw/parsed pairs create intentional redundancy for auditability.

The master schema is documented in `reports/phase5_schema_summary.md`.
