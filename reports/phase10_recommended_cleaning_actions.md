# Phase 10 - Recommended Cleaning Actions

## Timestamp Handling

1. Parse `Issue_reported at` and `issue_responded` with `%d-%m-%Y %H:%M`.
2. Parse `Survey_response_Date` with `%d-%b-%y`.
3. Parse ISO-derived datetime columns separately without forcing day-first interpretation.
4. Retain `is_negative_response_time` and exclude negative durations from valid timing models.
5. Review 0–1 minute and over-24-hour durations against operational rules before recoding.

## Sparse Column Handling

1. Exclude `connected_handling_time` from baseline models.
2. Exclude or separately justify city, product category, item price, and order timestamp.
3. Use customer remarks only in a dedicated NLP workflow with missingness-bias disclosure.
4. Keep missingness indicators where their use is methodologically justified.

## Category Standardization

1. Correct `Home Appliences` to `Home Appliances` through a documented mapping.
2. Prefer cleaned categorical columns for analysis while preserving original fields for audit.
3. Confirm intended ordering before encoding `Tenure Bucket` as ordinal.

## Modeling Exclusions And Controls

1. Exclude `Unique id` and `Order_id` from predictors.
2. Select one CSAT target and exclude every alternative target representation.
3. Avoid naive one-hot encoding for agent and city fields.
4. Treat survey-derived timing fields as potential leakage unless available at the prediction point.
5. Use stratified splits and class-sensitive metrics because of CSAT imbalance.
6. Do not use unadjusted personnel-level CSAT as a performance judgment.

## Recommended Baseline Feature Set

Start with cleaned channel, category, sub-category, manager/supervisor groupings where justified, tenure, shift, issue-hour/weekday, valid response-time features, and selected missingness indicators. Document every exclusion and transformation.
