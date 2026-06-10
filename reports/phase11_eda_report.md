# Phase 11 - Exploratory Data Analysis Report

## Completion Summary

Phase 11 analyzed 85,907 processed service records using univariate distributions, bivariate comparisons, grouped CSAT rates, correlations, and exploratory driver measures. Source data was not modified.

## Main Findings

- Overall CSAT is high and concentrated at score 5: mean 4.2422, with 82.46% of records rated 4-5.
- Response time is strongly right-skewed. Among 82,779 valid durations, median response time is 6 minutes and mean response time is 176.06 minutes.
- Response time has the strongest observed relationship with CSAT. Average CSAT decreases from 4.4844 within 5 minutes to 3.3952 after 24 hours.
- Email has the lowest channel CSAT at 3.8991 and the highest channel low-CSAT rate at 23.16%.
- Cancellation is the lowest established category at 3.9905. Specific sub-categories such as Technician Visit, Seller Cancelled Order, and Installation/demo also underperform.
- On Job Training has the lowest tenure-group average at 4.1452.
- Morning has the lowest shift average at 4.1895, although the shift-level association is small.
- Numeric correlations with CSAT are weak. Response time has Pearson correlation -0.1493 and Spearman correlation -0.1854.

## Relative Driver Evidence

Response time and sub-category show the strongest relative associations. Category and channel are secondary operational signals. Tenure and shift differences are smaller. These are descriptive patterns and not causal conclusions.

## Data and Modeling Notes

- Exclude or resolve 3,128 negative response durations before response-time modeling.
- Use one response-time unit, not both minutes and hours.
- Consolidate highly redundant missingness indicators.
- Control for issue mix and case complexity when testing channel, tenure, and shift effects.
- Treat low-volume category averages cautiously.

## Figures

- [Univariate overview](figures/phase11_univariate_overview.png)
- [CSAT by channel](figures/channel_csat.png)
- [CSAT by category](figures/category_csat.png)
- [CSAT by response time](figures/response_time_csat.png)
- [CSAT by tenure](figures/tenure_csat.png)
- [CSAT by shift](figures/shift_csat.png)
- [Correlation heatmap](figures/correlation_heatmap.png)

## Phase 12 Readiness

Phase 11 provides documented candidate relationships and modeling cautions. The project is ready for Phase 12 statistical or predictive analysis, subject to validation of data preparation assumptions and explicit handling of invalid response durations.

