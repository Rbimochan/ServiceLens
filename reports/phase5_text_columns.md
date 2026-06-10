# Phase 5 - Text Columns

| Column | Non-null | Missing | Missing % | Future NLP suitability |
|---|---:|---:|---:|---|
| Customer Remarks | 28,742 | 57,165 | 66.54% | Reference text; usable with substantial missingness caution |
| customer_remarks_clean | 28,673 | 57,234 | 66.62% | Preferred future NLP input after basic cleaning |

## Notes

- Other string columns represent identifiers, categories, or serialized datetimes rather than free text.
- Text coverage is limited to roughly one-third of records.
- No NLP, sentiment analysis, topic modeling, embeddings, or text imputation was performed.
