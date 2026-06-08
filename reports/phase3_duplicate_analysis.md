# Phase 3 - Duplicate Analysis

## Purpose

This report checks for duplicate records in the raw customer support ticket dataset before any cleaning is performed. The raw dataset was read for assessment only and was not modified.

## Dataset Location

`data/raw/customer_support_tickets.csv`

## Duplicate Check Summary

| Check | Result |
|---|---:|
| Total rows checked | 85,907 |
| Total columns checked | 20 |
| Full duplicate rows | 0 |
| Full duplicate row groups | 0 |
| Duplicate `Unique id` values | 0 |
| Duplicate `Unique id` groups | 0 |
| Blank `Unique id` values | 0 |

## Recommendation

No duplicate removal is recommended at this stage because no full duplicate rows or duplicate `Unique id` values were found.

The raw dataset should remain unchanged. If duplicates are introduced or detected in later processing steps, duplicate handling should be documented before creating any processed dataset.

## Risks

- This check identifies exact full-row duplicates and repeated `Unique id` values only.
- Near-duplicates, inconsistent text entries, or repeated business events with different identifiers are not evaluated in this step.
- Any future duplicate removal should be performed only after confirming the business meaning of repeated records.

## Next Step

Proceed to the next Phase 3 data preparation check. Do not create a final processed dataset until all cleaning rules are reviewed and approved.
