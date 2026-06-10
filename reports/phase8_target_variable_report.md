# Phase 8 - Target Variable Report

## Target Variable

`CSAT Score` is the ServiceLens target variable. It contains 85,907 valid observations on a 1–5 scale and no missing values.

## Distribution Summary

Score 5 dominates with 59,617 records (69.40%). Scores 1, 2, 3, and 4 represent 13.07%, 1.49%, 2.98%, and 13.06%, respectively.

## Mean, Median, And Mode

- Mean: 4.2422
- Median: 5
- Mode: 5, occurring in 69.40% of records
- Skewness: -1.6708

## Class Imbalance

The largest-to-smallest class ratio is 46.47:1. This class imbalance means later classification should use stratification and class-sensitive evaluation rather than overall accuracy alone.

## Low CSAT

Using the Phase 8 definition of scores 1–2, low CSAT includes 12,513 responses, or 14.57%. This definition is calculated directly because the existing `low_csat_flag` includes score 3.

## High CSAT

Scores 4–5 include 70,836 responses, or 82.46%.

## Visualization Summary

The histogram, frequency bar chart, and percentage chart in `reports/figures/` consistently show the concentration at score 5 and the smaller minority classes.

## Business Interpretation

The survey population is predominantly satisfied, but 14.57% of responses are clearly low satisfaction. The concentration at score 5 creates a modeling challenge and can obscure minority outcomes when using aggregate statistics.

No models, class balancing, predictive analysis, or dataset modifications were performed.
