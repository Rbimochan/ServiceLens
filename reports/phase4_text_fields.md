# Phase 4 - Text Fields

## Purpose

This report documents text variables in the processed ServiceLens dataset, including missingness, future NLP suitability, and risks. No NLP modeling, summarization, translation, sentiment analysis, topic modeling, or embeddings were performed.

## Dataset

`data/processed/customer_support_tickets_prepared.csv`

## Text Field Inventory

| Text Field | Source | Description |
|---|---|---|
| `Customer Remarks` | Original dataset column | Original free-text customer comment field, when available. |
| `customer_remarks_clean` | Generated during Phase 3 | Basic cleaned version of customer remarks after whitespace cleanup and missing-value standardization. |

Other string-like fields such as support channel, category, agent, supervisor, manager, tenure bucket, and shift are treated as categorical fields rather than free-text variables.

## Missingness Assessment

| Field | Missing / Empty Values | Non-Missing Values | Notes |
|---|---:|---:|---|
| `Customer Remarks` | 57,165 | 28,742 | Substantial missingness; use with caution. |
| `customer_remarks_clean` | 57,234 | 28,673 | Cleaning standardizes blank or whitespace-only remarks as missing. |

Phase 3 text preparation also found:

- Values changed by whitespace stripping: 13,499
- Empty values after stripping: 0
- No invented text was created
- No translation or summarization was performed

## Future NLP Suitability

| Field | Suitability | Reason |
|---|---|---|
| `Customer Remarks` | Limited / use with caution | Original text is useful for audit and reference, but missingness is high. |
| `customer_remarks_clean` | Best candidate for future NLP | Basic cleaning has been applied while preserving the original meaning. |

Potential future NLP tasks, if explicitly approved later:

- sentiment analysis
- keyword extraction
- topic modeling
- text classification
- embeddings for customer remark patterns

These tasks should be documented separately and should not be mixed with the current data dictionary step.

## Risks

- High missingness can bias text-based analysis toward customers who wrote remarks.
- Customer remarks may contain informal language, abbreviations, spelling variation, or incomplete comments.
- Text features may introduce noise if used in baseline models without careful preprocessing.
- NLP-derived features may be harder to interpret than structured support fields.
- Customer remarks should not be translated, summarized, rewritten, or filled with generated text unless a later approved methodology explicitly allows it.

## Recommended Handling

- Use `customer_remarks_clean` instead of `Customer Remarks` for any future text analysis.
- Keep `is_customer_remarks_missing` as a supporting missingness flag.
- Exclude text fields from baseline structured ML unless a text-specific modeling phase is approved.
- Preserve original `Customer Remarks` for traceability.
