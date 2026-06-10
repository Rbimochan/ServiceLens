# Phase 15 - Linear Regression

## Test Metrics

- R-squared: 0.0825
- MAE: 0.9981
- RMSE: 1.3329
- Intercept: 3.7685

## Largest Coefficients

| Feature | Coefficient | Direction |
|---|---:|---|
| Sub-category_Unable to Login | -1.6262 | Negative |
| Sub-category_Commission related | -1.2452 | Negative |
| Sub-category_Product related Issues | 1.1346 | Positive |
| Sub-category_Fraudulent User | 1.1179 | Positive |
| Sub-category_Damaged | 1.1029 | Positive |
| Sub-category_Return request | 1.0917 | Positive |
| Sub-category_Missing | 1.0877 | Positive |
| Sub-category_Wrong | 1.0159 | Positive |
| Sub-category_Customer Requested Modifications | 0.9168 | Positive |
| Sub-category_Policy Related | 0.9054 | Positive |
| Sub-category_Invoice request | 0.8706 | Positive |
| Sub-category_Signup Issues | 0.8705 | Positive |
| Sub-category_Priority delivery | 0.8436 | Positive |
| Sub-category_Unable to track | 0.8072 | Positive |
| Sub-category_Order Verification | 0.7144 | Positive |
| Sub-category_Reverse Pickup Enquiry | 0.6914 | Positive |
| Sub-category_Seller onboarding | 0.6674 | Positive |
| Sub-category_Self-Help | 0.6565 | Positive |
| Sub-category_Service Centres Related | 0.6475 | Positive |
| Sub-category_Shopzila Premium Related | 0.6463 | Positive |
| Sub-category_Order status enquiry | 0.6269 | Positive |
| Sub-category_Warranty related | -0.5965 | Negative |
| category_Onboarding related | -0.5778 | Negative |
| Sub-category_Exchange / Replacement | 0.5549 | Positive |
| category_Returns | -0.4992 | Negative |
| Sub-category_Delayed | 0.4582 | Positive |
| Sub-category_Card/EMI | -0.4512 | Negative |
| Sub-category_App/website Related | 0.4374 | Positive |
| category_Order Related | -0.4358 | Negative |
| Sub-category_Shopzilla Rewards | 0.4318 | Positive |

Categorical coefficients are CSAT-point differences from the documented reference category, holding encoded variables constant. Numeric coefficients represent a one-standard-deviation increase after transformation. Coefficients are associative, not causal.
