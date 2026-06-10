# Phase 8 - Low CSAT Rate

Phase 8 defines low CSAT as scores 1–2.

| Component | Count |
|---|---:|
| Score 1 | 11,230 |
| Score 2 | 1,283 |
| **Low CSAT total** | **12,513** |

- Low CSAT rate: **14.57%**
- Non-low records: 73,394

Approximately one in seven survey responses falls into the low-satisfaction group. Although this is a minority outcome, its business importance may be high because it represents clearly dissatisfied customers.

## Definition Note

The existing `low_csat_flag` created in Phase 3 uses `csat_score <= 3`. Phase 8 follows the current requested definition of scores 1–2 and therefore calculates this rate directly from `CSAT Score` rather than reusing that flag.
