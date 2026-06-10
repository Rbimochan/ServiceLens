"""Generate ServiceLens Phase 16 Tableau-ready data and dashboard previews."""

from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/servicelens-matplotlib")
os.environ.setdefault("LOKY_MAX_CPU_COUNT", "8")

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.gridspec import GridSpec
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "data" / "processed" / "customer_support_tickets_prepared.csv"
TABLEAU_PATH = ROOT / "data" / "processed" / "servicelens_tableau_source.csv"
REPORTS = ROOT / "reports"
FIGURES = REPORTS / "figures"
RANDOM_STATE = 42

BLUE = "#16697A"
TEAL = "#2A9D8F"
ORANGE = "#E76F51"
GOLD = "#E9C46A"
NAVY = "#264653"
GRAY = "#64748B"
LIGHT = "#F4F7F9"
RED = "#C44536"


def write_report(filename: str, content: str) -> None:
    (REPORTS / filename).write_text(content.strip() + "\n", encoding="utf-8")


def style_dashboard(fig: plt.Figure, title: str, subtitle: str) -> None:
    fig.patch.set_facecolor(LIGHT)
    fig.text(0.035, 0.965, title, fontsize=23, fontweight="bold", color=NAVY, va="top")
    fig.text(0.035, 0.925, subtitle, fontsize=10.5, color=GRAY, va="top")


def style_axis(ax: plt.Axes, title: str) -> None:
    ax.set_facecolor("white")
    ax.set_title(title, loc="left", fontsize=12, fontweight="bold", color=NAVY, pad=10)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#CBD5E1")
    ax.grid(axis="y", alpha=0.18)


def kpi_card(
    fig: plt.Figure,
    box: tuple[float, float, float, float],
    label: str,
    value: str,
    color: str,
    value_size: int = 23,
) -> None:
    ax = fig.add_axes(box)
    ax.set_facecolor("white")
    for spine in ax.spines.values():
        spine.set_color("#DCE4E8")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.text(0.06, 0.72, label.upper(), fontsize=9, color=GRAY, fontweight="bold", transform=ax.transAxes)
    ax.text(0.06, 0.25, value, fontsize=value_size, color=color, fontweight="bold", transform=ax.transAxes)


def save(fig: plt.Figure, filename: str) -> None:
    fig.savefig(FIGURES / filename, dpi=160, facecolor=fig.get_facecolor())
    plt.close(fig)


def build_cluster_labels(frame: pd.DataFrame) -> np.ndarray:
    categorical = ["channel_name", "category", "Sub-category", "Tenure Bucket", "Agent Shift"]
    cluster_frame = frame[categorical + ["response_time_minutes", "CSAT Score"]].copy()
    cluster_frame["response_time_log1p"] = np.log1p(cluster_frame["response_time_minutes"])
    preprocessor = ColumnTransformer(
        [
            ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical),
            (
                "numeric",
                Pipeline([("scaler", StandardScaler())]),
                ["response_time_log1p", "CSAT Score"],
            ),
        ],
        sparse_threshold=1.0,
    )
    matrix = preprocessor.fit_transform(cluster_frame)
    model = KMeans(n_clusters=2, n_init=10, random_state=RANDOM_STATE)
    raw_labels = model.fit_predict(matrix)
    means = pd.DataFrame(
        {
            "label": raw_labels,
            "csat": frame["CSAT Score"].to_numpy(),
            "response": frame["response_time_minutes"].to_numpy(),
        }
    ).groupby("label").mean()
    efficient_label = int(means.sort_values(["csat", "response"], ascending=[False, True]).index[0])
    return np.where(
        raw_labels == efficient_label,
        "Efficient Resolution Interactions",
        "Dissatisfied High-Effort Interactions",
    )


def main() -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(SOURCE_PATH, low_memory=False)
    data["issue_datetime"] = pd.to_datetime(data["issue_reported_at_parsed"], errors="coerce")
    data["survey_date"] = pd.to_datetime(data["survey_response_date_parsed"], errors="coerce")
    data["low_csat_binary"] = data["CSAT Score"].isin([1, 2]).astype(int)
    data["high_csat_binary"] = data["CSAT Score"].isin([4, 5]).astype(int)
    data["valid_response_time"] = data["response_time_minutes"].ge(0)

    valid = data[data["valid_response_time"]].copy()
    valid["interaction_profile"] = build_cluster_labels(valid)

    export_columns = [
        "Unique id",
        "issue_datetime",
        "survey_date",
        "channel_name",
        "category",
        "Sub-category",
        "Tenure Bucket",
        "Agent Shift",
        "CSAT Score",
        "low_csat_binary",
        "high_csat_binary",
        "response_time_minutes",
        "response_time_bucket",
        "issue_hour",
        "issue_weekday",
        "interaction_profile",
    ]
    tableau_source = valid[export_columns].copy()
    tableau_source.to_csv(TABLEAU_PATH, index=False, date_format="%Y-%m-%d %H:%M:%S")

    average_csat = data["CSAT Score"].mean()
    low_rate = data["low_csat_binary"].mean()
    high_rate = data["high_csat_binary"].mean()
    ticket_volume = len(data)
    median_response = valid["response_time_minutes"].median()

    monthly = (
        data.dropna(subset=["issue_datetime"])
        .set_index("issue_datetime")
        .resample("MS")
        .agg(
            average_csat=("CSAT Score", "mean"),
            tickets=("CSAT Score", "size"),
            low_rate=("low_csat_binary", "mean"),
            high_rate=("high_csat_binary", "mean"),
        )
        .reset_index()
    )

    # Executive dashboard preview
    fig = plt.figure(figsize=(14, 8), constrained_layout=False)
    style_dashboard(fig, "ServiceLens | Executive Overview", "Customer satisfaction and service operations summary")
    card_width = 0.172
    card_lefts = [0.035, 0.228, 0.421, 0.614, 0.807]
    cards = [
        ("Average CSAT", f"{average_csat:.3f}", BLUE),
        ("Low CSAT", f"{low_rate:.2%}", RED),
        ("High CSAT", f"{high_rate:.2%}", TEAL),
        ("Ticket Volume", f"{ticket_volume:,}", NAVY),
        ("Median Response", f"{median_response:.0f} min", ORANGE),
    ]
    for left, (label, value, color) in zip(card_lefts, cards):
        kpi_card(fig, (left, 0.75, card_width, 0.13), label, value, color)
    ax1 = fig.add_axes((0.05, 0.39, 0.57, 0.28))
    style_axis(ax1, "Monthly CSAT Trend")
    ax1.plot(monthly["issue_datetime"], monthly["average_csat"], marker="o", color=BLUE, linewidth=2)
    ax1.xaxis.set_major_locator(mdates.MonthLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax1.set_ylabel("Average CSAT")
    ax1.set_ylim(1, 5)
    category_summary = data.groupby("category").agg(Tickets=("CSAT Score", "size"), CSAT=("CSAT Score", "mean"))
    category_summary = category_summary.sort_values("Tickets", ascending=False).head(7).sort_values("Tickets")
    ax2 = fig.add_axes((0.68, 0.39, 0.28, 0.28))
    style_axis(ax2, "Highest-Volume Categories")
    ax2.barh(category_summary.index, category_summary["Tickets"], color=TEAL)
    ax2.tick_params(axis="y", labelsize=8)
    ax3 = fig.add_axes((0.05, 0.08, 0.91, 0.23))
    style_axis(ax3, "Executive Priority Indicators")
    priorities = ["Email CSAT", "OJT CSAT", "Morning CSAT", ">24h Response CSAT"]
    email_csat = data.groupby("channel_name")["CSAT Score"].mean().get("Email", np.nan)
    ojt_csat = data.groupby("Tenure Bucket")["CSAT Score"].mean().get("On Job Training", np.nan)
    morning_csat = data.groupby("Agent Shift")["CSAT Score"].mean().get("Morning", np.nan)
    long_csat = valid.loc[valid["response_time_minutes"] > 1_440, "CSAT Score"].mean()
    values = [email_csat, ojt_csat, morning_csat, long_csat]
    bars = ax3.bar(priorities, values, color=[ORANGE, GOLD, BLUE, RED])
    ax3.bar_label(bars, fmt="%.2f", padding=3)
    ax3.set_ylim(0, 5)
    ax3.set_ylabel("Average CSAT")
    save(fig, "executive_dashboard.png")

    # CSAT dashboard preview
    fig = plt.figure(figsize=(14, 8))
    style_dashboard(fig, "ServiceLens | CSAT Performance", "Distribution, trends, channels, and issue categories")
    gs = GridSpec(2, 2, figure=fig, left=0.06, right=0.97, bottom=0.08, top=0.86, hspace=0.38, wspace=0.28)
    ax = fig.add_subplot(gs[0, 0])
    style_axis(ax, "CSAT Distribution")
    distribution = data["CSAT Score"].value_counts().sort_index()
    bars = ax.bar(distribution.index.astype(str), distribution.values, color=[RED, ORANGE, GOLD, BLUE, TEAL])
    ax.bar_label(bars, labels=[f"{value / len(data):.1%}" for value in distribution.values], padding=3)
    ax.set_xlabel("CSAT Score")
    ax.set_ylabel("Tickets")
    ax = fig.add_subplot(gs[0, 1])
    style_axis(ax, "Monthly Low and High CSAT Rates")
    ax.plot(monthly["issue_datetime"], monthly["low_rate"] * 100, color=RED, marker="o", label="Low CSAT")
    ax.plot(monthly["issue_datetime"], monthly["high_rate"] * 100, color=TEAL, marker="o", label="High CSAT")
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.set_ylabel("Rate (%)")
    ax.legend(frameon=False)
    ax = fig.add_subplot(gs[1, 0])
    style_axis(ax, "Average CSAT by Channel")
    channel = data.groupby("channel_name")["CSAT Score"].mean().sort_values()
    bars = ax.barh(channel.index, channel.values, color=[ORANGE, BLUE, TEAL])
    ax.bar_label(bars, fmt="%.2f", padding=3)
    ax.set_xlim(0, 5)
    ax = fig.add_subplot(gs[1, 1])
    style_axis(ax, "Average CSAT by Category")
    category = data.groupby("category").agg(csat=("CSAT Score", "mean"), volume=("CSAT Score", "size"))
    category = category[category["volume"] >= 100].sort_values("csat").head(8)
    ax.barh(category.index, category["csat"], color=BLUE)
    ax.set_xlim(0, 5)
    ax.tick_params(axis="y", labelsize=8)
    save(fig, "csat_dashboard.png")

    # Operational dashboard preview
    fig = plt.figure(figsize=(14, 8))
    style_dashboard(fig, "ServiceLens | Operational Performance", "Response effort, tenure, and shift performance")
    gs = GridSpec(2, 2, figure=fig, left=0.09, right=0.97, bottom=0.08, top=0.86, hspace=0.38, wspace=0.3)
    ax = fig.add_subplot(gs[0, 0])
    style_axis(ax, "Response Time Distribution")
    clipped = valid["response_time_minutes"].clip(upper=valid["response_time_minutes"].quantile(0.98))
    ax.hist(clipped, bins=40, color=BLUE, alpha=0.9)
    ax.set_xlabel("Response minutes (98th percentile cap)")
    ax.set_ylabel("Tickets")
    ax = fig.add_subplot(gs[0, 1])
    style_axis(ax, "CSAT by Response-Time Bucket")
    bucket_order = [
        "0-5 min", "5-15 min", "15-30 min", "30-60 min", "1-2h", "2-4h", "4-24h", ">24h"
    ]
    response_buckets = pd.cut(
        valid["response_time_minutes"],
        bins=[-0.001, 5, 15, 30, 60, 120, 240, 1_440, np.inf],
        labels=bucket_order,
    )
    bucket_csat = valid.assign(display_bucket=response_buckets).groupby(
        "display_bucket", observed=True
    )["CSAT Score"].mean()
    bars = ax.bar(bucket_csat.index.astype(str), bucket_csat.values, color=ORANGE)
    ax.bar_label(bars, fmt="%.2f", padding=3, fontsize=8)
    ax.tick_params(axis="x", rotation=30)
    ax.set_ylim(0, 5)
    ax = fig.add_subplot(gs[1, 0])
    style_axis(ax, "CSAT by Agent Tenure")
    tenure = data.groupby("Tenure Bucket")["CSAT Score"].mean().sort_values()
    bars = ax.barh(tenure.index, tenure.values, color=TEAL)
    ax.bar_label(bars, fmt="%.2f", padding=3)
    ax.set_xlim(0, 5)
    ax = fig.add_subplot(gs[1, 1])
    style_axis(ax, "CSAT by Shift")
    shifts = data.groupby("Agent Shift")["CSAT Score"].mean().sort_values()
    bars = ax.barh(shifts.index, shifts.values, color=GOLD)
    ax.bar_label(bars, fmt="%.2f", padding=3)
    ax.set_xlim(0, 5)
    save(fig, "operational_dashboard.png")

    # Cluster dashboard preview
    cluster_summary = valid.groupby("interaction_profile").agg(
        Tickets=("CSAT Score", "size"),
        Average_CSAT=("CSAT Score", "mean"),
        Average_Response=("response_time_minutes", "mean"),
        Median_Response=("response_time_minutes", "median"),
    )
    cluster_order = [
        "Efficient Resolution Interactions",
        "Dissatisfied High-Effort Interactions",
    ]
    cluster_summary = cluster_summary.reindex(cluster_order)
    fig = plt.figure(figsize=(14, 8))
    style_dashboard(fig, "ServiceLens | Interaction Profiles", "K-Means profiles from Phase 14")
    gs = GridSpec(2, 3, figure=fig, left=0.06, right=0.97, bottom=0.09, top=0.84, hspace=0.42, wspace=0.35)
    ax = fig.add_subplot(gs[:, 0])
    style_axis(ax, "Cluster Share")
    ax.pie(
        cluster_summary["Tickets"],
        labels=["Efficient Resolution", "Dissatisfied High-Effort"],
        autopct="%1.1f%%",
        colors=[TEAL, ORANGE],
        startangle=90,
        wedgeprops={"linewidth": 1, "edgecolor": "white"},
    )
    ax = fig.add_subplot(gs[0, 1:])
    style_axis(ax, "Average CSAT by Profile")
    bars = ax.bar(cluster_summary.index, cluster_summary["Average_CSAT"], color=[TEAL, ORANGE])
    ax.bar_label(bars, fmt="%.3f", padding=3)
    ax.set_ylim(0, 5)
    ax.tick_params(axis="x", labelsize=8)
    ax = fig.add_subplot(gs[1, 1:])
    style_axis(ax, "Response Time by Profile")
    x_pos = np.arange(len(cluster_summary))
    width = 0.36
    ax.bar(x_pos - width / 2, cluster_summary["Average_Response"], width, label="Average", color=BLUE)
    ax.bar(x_pos + width / 2, cluster_summary["Median_Response"], width, label="Median", color=GOLD)
    ax.set_xticks(x_pos, ["Efficient Resolution", "Dissatisfied High-Effort"])
    ax.set_ylabel("Minutes")
    ax.legend(frameon=False)
    save(fig, "cluster_dashboard.png")

    # Predictive dashboard preview
    model_results = pd.DataFrame(
        {
            "Model": ["Logistic Regression", "Random Forest", "Gradient Boosting", "Threshold Optimized"],
            "ROC_AUC": [0.6660, 0.6958, 0.7038, 0.7045],
            "F1": [0.3254, 0.3601, 0.3626, 0.3662],
            "Precision": [0.2179, 0.2605, 0.2531, 0.2905],
            "Recall": [0.6423, 0.5832, 0.6394, 0.4953],
        }
    )
    drivers = pd.Series(
        [0.10195, 0.03631, 0.00623, 0.00265, 0.00199],
        index=["Response Time", "Sub-category", "Tenure Bucket", "Issue Weekday", "Channel"],
    )
    fig = plt.figure(figsize=(14, 8))
    style_dashboard(fig, "ServiceLens | Predictive Analytics", "Classification performance and operational drivers")
    kpi_card(fig, (0.055, 0.73, 0.27, 0.14), "Best Classification Model", "Optimized GB", NAVY, 20)
    kpi_card(fig, (0.365, 0.73, 0.18, 0.14), "ROC-AUC", "0.7045", BLUE)
    kpi_card(fig, (0.585, 0.73, 0.18, 0.14), "F1 Score", "0.3662", TEAL)
    kpi_card(fig, (0.805, 0.73, 0.14, 0.14), "Threshold", "0.60", ORANGE)
    ax = fig.add_axes((0.14, 0.38, 0.47, 0.27))
    style_axis(ax, "Model ROC-AUC Comparison")
    bars = ax.barh(model_results["Model"], model_results["ROC_AUC"], color=[GRAY, BLUE, TEAL, ORANGE])
    ax.bar_label(bars, fmt="%.3f", padding=3)
    ax.set_xlim(0, 1)
    ax = fig.add_axes((0.68, 0.38, 0.27, 0.27))
    style_axis(ax, "Top Operational Drivers")
    drivers.sort_values().plot.barh(ax=ax, color=BLUE)
    ax.set_xlabel("Permutation importance")
    ax = fig.add_axes((0.06, 0.08, 0.89, 0.22))
    style_axis(ax, "Low-CSAT Detection Tradeoff")
    x_pos = np.arange(len(model_results))
    width = 0.25
    ax.bar(x_pos - width, model_results["Precision"], width, label="Precision", color=BLUE)
    ax.bar(x_pos, model_results["Recall"], width, label="Recall", color=ORANGE)
    ax.bar(x_pos + width, model_results["F1"], width, label="F1", color=TEAL)
    ax.set_xticks(x_pos, model_results["Model"])
    ax.set_ylim(0, 0.8)
    ax.legend(frameon=False, ncol=3)
    save(fig, "predictive_dashboard.png")

    write_report(
        "phase16_dashboard_planning.md",
        """
# Phase 16 - Dashboard Planning

| Dashboard | Purpose | Core KPIs/Visuals | Filters | Audience |
|---|---|---|---|---|
| Executive Overview | Summarize satisfaction and operational health | Average CSAT, low/high CSAT, volume, median response, trend, priority indicators | Channel, category, date | Executives and service leaders |
| CSAT Performance | Explain satisfaction outcomes | Distribution, low/high trends, channel CSAT, category CSAT | Channel, category, sub-category, date | CX and quality teams |
| Operational Performance | Monitor controllable service factors | Response distribution/buckets, tenure, shift | Category, shift, tenure, channel | Operations managers |
| Interaction Profiles | Explain Phase 14 segments | Cluster share, CSAT, response time, characteristics | Profile, channel, category | Strategy and operations |
| Predictive Analytics | Present model capability and drivers | ROC-AUC, F1, precision/recall, feature importance | Model, metric | Analytics and governance |

The five dashboards form a Tableau Story ordered from executive outcomes to operational diagnosis and predictive evidence.
""",
    )

    field_rows = [
        ("Unique id", "String", "Dimension", "Ticket identifier"),
        ("issue_datetime", "Date & Time", "Dimension", "Primary time axis"),
        ("survey_date", "Date", "Dimension", "Survey response date"),
        ("channel_name", "String", "Dimension", "Support channel"),
        ("category", "String", "Dimension", "Issue category"),
        ("Sub-category", "String", "Dimension", "Detailed issue type"),
        ("Tenure Bucket", "String", "Dimension", "Agent tenure group"),
        ("Agent Shift", "String", "Dimension", "Shift"),
        ("CSAT Score", "Number (whole)", "Measure", "Satisfaction score"),
        ("low_csat_binary", "Number (whole)", "Measure", "1 for CSAT 1-2"),
        ("high_csat_binary", "Number (whole)", "Measure", "1 for CSAT 4-5"),
        ("response_time_minutes", "Number (whole)", "Measure", "Non-negative response duration"),
        ("response_time_bucket", "String", "Dimension", "Prepared duration bucket"),
        ("issue_hour", "Number (whole)", "Dimension", "Hour of issue"),
        ("issue_weekday", "String", "Dimension", "Weekday"),
        ("interaction_profile", "String", "Dimension", "Phase 14 K-Means profile"),
    ]
    field_table = "\n".join(
        ["| Field | Tableau Type | Role | Meaning |", "|---|---|---|---|"]
        + [f"| {a} | {b} | {c} | {d} |" for a, b, c, d in field_rows]
    )
    write_report(
        "phase16_tableau_data_source.md",
        f"""
# Phase 16 - Tableau Data Source

- CSV: `data/processed/servicelens_tableau_source.csv`
- Rows: {len(tableau_source):,}
- Columns: {len(tableau_source.columns)}
- Excluded records: negative response durations
- Dates exported in ISO-compatible format

{field_table}

## Calculated Fields

```text
Average CSAT = AVG([CSAT Score])
Low CSAT % = AVG([low_csat_binary])
High CSAT % = AVG([high_csat_binary])
Ticket Volume = COUNTD([Unique id])
Median Response Time = MEDIAN([response_time_minutes])
```

The CSV is intentionally stored under ignored `data/processed/`; it should be refreshed by running the Phase 16 generator rather than committed as a large derived dataset. Tableau Desktop can connect directly to the CSV and optionally create a local `.hyper` extract.
""",
    )

    dashboard_notes = {
        "phase16_executive_dashboard.md": (
            "Executive Overview Dashboard",
            "executive_dashboard.png",
            "Five KPI tiles, monthly CSAT trend, category volume, and priority indicators. Use Channel, Category, and Issue Date as global filters.",
        ),
        "phase16_csat_dashboard.md": (
            "CSAT Performance Dashboard",
            "csat_dashboard.png",
            "CSAT distribution, monthly low/high rates, channel comparison, and established category comparison. Verified headline values are mean CSAT 4.242, low CSAT 14.57%, and high CSAT 82.46%.",
        ),
        "phase16_operational_dashboard.md": (
            "Operational Performance Dashboard",
            "operational_dashboard.png",
            "Response-time distribution and buckets, tenure performance, and shift performance. Response time is the strongest measured driver; On Job Training and Morning are the weakest observed tenure and shift groups.",
        ),
        "phase16_cluster_dashboard.md": (
            "Customer Interaction Profiles Dashboard",
            "cluster_dashboard.png",
            "Cluster share, CSAT, and response-time comparison for Efficient Resolution Interactions (83.92%) and Dissatisfied High-Effort Interactions (16.08%).",
        ),
        "phase16_predictive_dashboard.md": (
            "Predictive Analytics Dashboard",
            "predictive_dashboard.png",
            "Model ROC-AUC comparison, precision/recall/F1 tradeoff, and driver ranking. The selected model is threshold-optimized Gradient Boosting with ROC-AUC 0.7045.",
        ),
    }
    for filename, (title, image, description) in dashboard_notes.items():
        write_report(
            filename,
            f"""
# Phase 16 - {title}

## Design

{description}

## Tableau Build Notes

- Use a fixed desktop layout near 1,400 x 800 pixels.
- Apply dashboard filter actions rather than duplicating controls per worksheet.
- Format CSAT to two or three decimals and rates as percentages.
- Preserve the response-time validity filter.
- Add source and refresh date in the dashboard footer.

## Preview

The image below is a reproducible design preview generated from the verified data. It is not represented as a native Tableau export.

![{title}](figures/{image})
""",
        )

    write_report(
        "phase16_tableau_story.md",
        """
# Phase 16 - Tableau Story

## Global Filters

- Channel
- Category
- Sub-category
- Agent Shift
- Tenure Bucket
- Issue date range

## Story Sequence

1. **Executive Summary** - Establish overall satisfaction, volume, and response performance.
2. **Satisfaction Drivers** - Move from CSAT distribution to channel, category, response time, tenure, and shift.
3. **Interaction Profiles** - Explain the two Phase 14 operational profiles.
4. **Predictive Analytics** - Present model discrimination, low-CSAT detection tradeoffs, and ranked variables.
5. **Recommendations** - Connect verified findings to operational actions.

Filter actions should preserve context between story points. Dashboard titles and annotations should state whether a metric is descriptive, predictive, or model-based.
""",
    )

    write_report(
        "phase16_dashboard_recommendations.md",
        """
# Phase 16 - Dashboard Recommendations

1. **Reduce response delay.** Response time is the strongest predictive variable and CSAT declines materially as delays increase.
2. **Improve Email support.** Email has average CSAT of approximately 3.90, below Inbound and Outcall.
3. **Strengthen On Job Training coaching.** The OJT tenure group has the lowest observed tenure-level average CSAT.
4. **Investigate Cancellation issues.** Cancellation is the weakest established category by average CSAT among categories with meaningful volume.
5. **Monitor Morning operations.** Morning has the lowest observed shift-level average and nearly half of ticket volume.
6. **Use predictive alerts as prioritization, not automation.** ROC-AUC is 0.7045 and precision remains limited.
7. **Track the dissatisfied high-effort profile.** This profile represents approximately 16.08% of valid interactions and combines lower satisfaction with longer response time.

These recommendations are based on verified descriptive and predictive findings. They do not claim causal effects.
""",
    )

    write_report(
        "phase16_tableau_dashboard_report.md",
        """
# Phase 16 - Tableau Dashboard Report

## Dashboard Inventory

| Dashboard | Preview | Business Value |
|---|---|---|
| Executive Overview | `figures/executive_dashboard.png` | Rapid service-health review |
| CSAT Performance | `figures/csat_dashboard.png` | Satisfaction trend and segment diagnosis |
| Operational Performance | `figures/operational_dashboard.png` | Response, tenure, and shift monitoring |
| Interaction Profiles | `figures/cluster_dashboard.png` | Explain the two unsupervised profiles |
| Predictive Analytics | `figures/predictive_dashboard.png` | Communicate model quality and limitations |

## Implementation Package

- Tableau-ready source: `data/processed/servicelens_tableau_source.csv`
- Field mapping and calculated fields: `phase16_tableau_data_source.md`
- Worksheet, filter, and story specifications: Phase 16 dashboard reports
- Five reproducible dashboard previews
- Recommendation narrative linked to verified findings

## Tableau Desktop Implementation Notes

Tableau Desktop 2026.1 is installed locally. Connect it to the generated CSV, set the documented field roles, create the five dashboard layouts from the previews, then save a `.twbx` after visual and interaction testing. A native Tableau workbook was not generated by this noninteractive Python workflow, and the preview PNGs are not claimed to be Tableau exports.

## Refresh Procedure

1. Run `conda run -n servicelens python scripts/run_phase_16_dashboard_assets.py`.
2. Refresh the CSV connection or Tableau extract.
3. Confirm KPI values and filters.
4. Export final Tableau screenshots after the `.twbx` is authored.

## Business Value

The package converts Phases 8-15 into a consistent executive narrative: current satisfaction, operational drivers, interaction profiles, predictive capability, and evidence-based actions.
""",
    )

    print(f"Tableau source: {TABLEAU_PATH}")
    print(f"Rows exported: {len(tableau_source):,}")
    print("Dashboard previews generated: 5")


if __name__ == "__main__":
    main()
