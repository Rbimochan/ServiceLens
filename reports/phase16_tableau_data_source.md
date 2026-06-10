# Phase 16 - Tableau Data Source

- CSV: `data/processed/servicelens_tableau_source.csv`
- Rows: 82,779
- Columns: 16
- Excluded records: negative response durations
- Dates exported in ISO-compatible format

| Field | Tableau Type | Role | Meaning |
|---|---|---|---|
| Unique id | String | Dimension | Ticket identifier |
| issue_datetime | Date & Time | Dimension | Primary time axis |
| survey_date | Date | Dimension | Survey response date |
| channel_name | String | Dimension | Support channel |
| category | String | Dimension | Issue category |
| Sub-category | String | Dimension | Detailed issue type |
| Tenure Bucket | String | Dimension | Agent tenure group |
| Agent Shift | String | Dimension | Shift |
| CSAT Score | Number (whole) | Measure | Satisfaction score |
| low_csat_binary | Number (whole) | Measure | 1 for CSAT 1-2 |
| high_csat_binary | Number (whole) | Measure | 1 for CSAT 4-5 |
| response_time_minutes | Number (whole) | Measure | Non-negative response duration |
| response_time_bucket | String | Dimension | Prepared duration bucket |
| issue_hour | Number (whole) | Dimension | Hour of issue |
| issue_weekday | String | Dimension | Weekday |
| interaction_profile | String | Dimension | Phase 14 K-Means profile |

## Calculated Fields

```text
Average CSAT = AVG([CSAT Score])
Low CSAT % = AVG([low_csat_binary])
High CSAT % = AVG([high_csat_binary])
Ticket Volume = COUNTD([Unique id])
Median Response Time = MEDIAN([response_time_minutes])
```

The CSV is intentionally stored under ignored `data/processed/`; it should be refreshed by running the Phase 16 generator rather than committed as a large derived dataset. Tableau Desktop can connect directly to the CSV and optionally create a local `.hyper` extract.
