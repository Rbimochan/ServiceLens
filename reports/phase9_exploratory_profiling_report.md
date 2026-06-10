# Phase 9 - Exploratory Profiling Report

## Method

The processed dataset was profiled using `CSAT Score`, with low CSAT defined as scores 1-2 and high CSAT as scores 4-5. Average response-time calculations exclude negative durations. Findings are descriptive and do not establish causality.

## Channel Analysis

Email is the weakest support channel with 3.8991 average CSAT and 23.16% low CSAT. Outcall is strongest at 4.2699 average CSAT.

## Category Analysis

Cancellation is the weakest category among groups with at least 100 tickets. The smaller `Others` group is lower but has only 99 records.

## Sub-Category Analysis

Technician Visit is the lowest-performing sub-category with at least 100 tickets, followed by Seller Cancelled Order. Both have low-CSAT rates above 30%.

## Agent Findings

The dataset contains 1,371 agents. Individual agents were not named or ranked. Median agent ticket volume is 57, median agent average CSAT is 4.2391, and median agent low-CSAT rate is 14.29%. Low-volume results are less stable.

## Supervisor Findings

Supervisor groups vary in volume and unadjusted CSAT. Established groups with lower averages also show higher low-CSAT rates, but workload and ticket-mix controls are required before performance interpretation.

## Manager Findings

Manager-group average CSAT ranges from 4.1122 to 4.3791. These differences are descriptive and may reflect organizational and assignment differences.

## Tenure Findings

On Job Training is the weakest tenure group, with 4.1452 average CSAT and 16.64% low CSAT.

## Shift Findings

Morning is the weakest and largest shift, with 4.1895 average CSAT and 15.75% low CSAT.

## Key Patterns

Valid response time has the clearest monotonic descriptive pattern: average CSAT falls from 4.4844 at 0-5 minutes to 4.0205 at 16-30 minutes and 3.3952 beyond 24 hours. Low-CSAT rate rises from 8.88% to 36.32%.

Phase 9 identifies candidate drivers for later controlled analysis. It does not prove that channel, staffing group, category, or response time causes changes in CSAT.
