# ServiceLens Project Objective Summary

## What the Project Is Proposing

ServiceLens is a customer satisfaction analytics project focused on understanding what drives customer satisfaction in support ticket interactions.

The project proposes to use Python, PySpark, machine learning, and Tableau to analyze customer support ticket data and turn it into practical business insights.

## Main Aim

To investigate the drivers of customer satisfaction and discover customer support interaction patterns through scalable analytics using PySpark and Tableau.

## Main Questions

The project is trying to answer:

1. Which operational factors have the strongest influence on customer satisfaction?
2. Can customer satisfaction be predicted using support interaction data?
3. What types of support interaction profiles exist in the ticket data?
4. How much do factors like response time, resolution efficiency, support channel, issue type, and customer effort affect satisfaction?

## Planned Outputs

The proposal expects the project to produce:

- Ranked satisfaction drivers
- Predictive CSAT models
- Customer support interaction clusters
- Tableau dashboards
- Evidence-based service improvement recommendations

## Proposed Analytics Work

### 1. Data Preparation

Clean the dataset, handle missing values, parse date/time fields, remove or flag bad records, and create useful features.

### 2. Exploratory Data Analysis

Analyze CSAT patterns by support channel, category, sub-category, response time, agent, supervisor, manager, tenure bucket, and shift.

### 3. Classification

Build models to predict customer satisfaction outcomes.

Possible algorithms:

- Logistic Regression
- Random Forest
- Gradient Boosted Trees

Possible metrics:

- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC

### 4. Clustering

Group tickets into support interaction profiles.

Possible profiles:

- Efficient resolution customers
- Communication-intensive customers
- Dissatisfied high-effort customers

### 5. Regression and Feature Importance

Estimate which variables have the strongest relationship with CSAT and rank their relative importance.

## How the Actual CSV Fits the Proposal

The provided CSV supports the project, but the available columns are not exactly the same as the proposal describes.

Strong usable fields in the CSV include:

- `channel_name`
- `category`
- `Sub-category`
- `Issue_reported at`
- `issue_responded`
- `Agent_name`
- `Supervisor`
- `Manager`
- `Tenure Bucket`
- `Agent Shift`
- `CSAT Score`

Fields mentioned in the proposal but not clearly available in the CSV include:

- `Resolution Time`
- `Ticket Priority`
- `Interaction Count`
- `Ticket Status`
- `Escalation`

Because of this, the project should be adjusted to focus on the fields that actually exist in the dataset.

## Recommended Practical Direction

The project is still achievable if the methodology is aligned with the real dataset.

The strongest practical version of the project is:

Analyze and predict CSAT using support channel, category, sub-category, response time, agent/team hierarchy, tenure bucket, shift, and date/time features.

## Suggested Project Deliverables

1. Cleaned and feature-engineered dataset
2. Exploratory data analysis report
3. CSAT classification model
4. Customer support interaction clustering analysis
5. Regression or feature-importance analysis
6. Tableau dashboard
7. Final report with recommendations

## Key Business Value

ServiceLens can help identify where customer dissatisfaction is coming from and what operational changes may improve customer experience.

Based on the initial CSV analysis, likely areas of focus include:

- Email support performance
- Cancellation-related issues
- Seller cancelled orders
- Installation/demo issues
- Delayed orders
- Long response times
- On Job Training agent performance
- Morning shift workload and CSAT
