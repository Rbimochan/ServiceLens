# Phase 3 - Text Cleaning Pipeline

## Purpose

This report documents a safe basic text cleaning pipeline for available text fields in the raw customer support ticket dataset. The raw dataset was inspected for planning only and was not modified. No NLP modeling, translation, summarization, or invented text was created.

## Dataset Location

`data/raw/customer_support_tickets.csv`

## Text Column Identification

| Column | Role | Available | Recommended Treatment |
|---|---|---|---|
| Customer Remarks | Free-text customer comment field | Yes | Apply basic text cleaning only if used later. |

Other string-like columns such as `channel_name`, `category`, `Sub-category`, `Agent_name`, `Supervisor`, `Manager`, `Tenure Bucket`, and `Agent Shift` should be treated as categorical fields rather than free-text fields.

## Basic Cleaning Rules

| Rule | Description |
|---|---|
| Preserve original meaning | Do not translate, summarize, rewrite, or infer missing remarks. |
| Strip whitespace | Remove leading and trailing whitespace from available text values. |
| Standardize empty strings | Treat empty strings after stripping as missing values. |
| Preserve missing values | Keep missing customer remarks as missing; do not fill with invented text. |
| No NLP modeling | Do not perform sentiment analysis, topic modeling, embeddings, or text classification in this step. |

## Customer Remarks Cleaning Assessment

| Check | Result |
|---|---:|
| Rows assessed | 85,907 |
| Raw missing `Customer Remarks` values | 57,151 |
| Values changed by whitespace stripping | 13,499 |
| Empty values after stripping | 0 |
| Non-missing values after basic cleaning | 28,756 |

## Proposed Pipeline

1. Select `Customer Remarks` only if text analysis or reporting requires it.
2. Convert the field to string only for non-missing values.
3. Strip leading and trailing whitespace.
4. Convert empty strings to missing values.
5. Preserve the cleaned text without translation, summarization, or generated content.
6. Keep a missingness indicator if later modeling uses this text field.

## Recommended Treatment

- Use `Customer Remarks` with caution because it has substantial missingness.
- Do not make it mandatory for baseline EDA or modeling.
- Keep basic cleaned text separate from raw data in any future processed dataset.
- Do not use NLP-derived features until a later, explicitly approved text analysis phase.

## Risks

- High missingness may bias any later text-based analysis.
- Whitespace cleaning improves consistency but does not solve missing text.
- Customer remarks may contain inconsistent spelling, abbreviations, or informal language that should not be over-cleaned at this stage.
- Any later NLP work should document its assumptions separately.

## Next Step

Combine this text cleaning plan with the missing value, duplicate, datatype, datetime, and lifecycle feature reports before creating a final processed dataset.
