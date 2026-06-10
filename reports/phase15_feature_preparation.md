# Phase 15 - Feature Preparation

- Categorical encoding: one-hot encoding with the first sorted category dropped as the reference level
- Missing categorical values: most-frequent imputation
- Response time: `log1p` transformation followed by z-score standardization
- Issue hour and issue month: median imputation and z-score standardization
- Training matrix dimensions: 66,223 rows x 85 columns
- Unseen test categories: ignored safely by the encoder

Reference categories:

- `channel_name`: `Email`
- `category`: `App/website`
- `Sub-category`: `Account updation`
- `Tenure Bucket`: `0-30`
- `Agent Shift`: `Afternoon`
- `issue_weekday`: `Friday`
