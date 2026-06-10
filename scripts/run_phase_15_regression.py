"""Run the reproducible ServiceLens Phase 15 regression workflow."""

from __future__ import annotations

import os
import warnings
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/servicelens-matplotlib")
os.environ.setdefault("LOKY_MAX_CPU_COUNT", "8")

warnings.filterwarnings(
    "ignore",
    message="Found unknown categories in columns .* during transform.*",
    category=UserWarning,
)

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "processed" / "customer_support_tickets_prepared.csv"
REPORTS = ROOT / "reports"
FIGURES = REPORTS / "figures"
RANDOM_STATE = 42

CATEGORICAL_FEATURES = [
    "channel_name",
    "category",
    "Sub-category",
    "Tenure Bucket",
    "Agent Shift",
    "issue_weekday",
]
NUMERIC_FEATURES = ["response_time_minutes", "issue_hour", "issue_month"]
FEATURES = CATEGORICAL_FEATURES + NUMERIC_FEATURES


def write_report(filename: str, content: str) -> None:
    (REPORTS / filename).write_text(content.strip() + "\n", encoding="utf-8")


def build_preprocessor() -> ColumnTransformer:
    return ColumnTransformer(
        transformers=[
            (
                "categorical",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        (
                            "encoder",
                            OneHotEncoder(
                                handle_unknown="ignore",
                                drop="first",
                                sparse_output=True,
                            ),
                        ),
                    ]
                ),
                CATEGORICAL_FEATURES,
            ),
            (
                "response_time",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="median")),
                        (
                            "log1p",
                            FunctionTransformer(
                                np.log1p,
                                feature_names_out="one-to-one",
                            ),
                        ),
                        ("scaler", StandardScaler()),
                    ]
                ),
                ["response_time_minutes"],
            ),
            (
                "other_numeric",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="median")),
                        ("scaler", StandardScaler()),
                    ]
                ),
                ["issue_hour", "issue_month"],
            ),
        ],
        sparse_threshold=1.0,
    )


def metrics(y_true: pd.Series, predictions: np.ndarray) -> dict[str, float]:
    return {
        "r2": r2_score(y_true, predictions),
        "mae": mean_absolute_error(y_true, predictions),
        "rmse": mean_squared_error(y_true, predictions) ** 0.5,
    }


def metric_table(results: dict[str, dict[str, float]]) -> str:
    lines = [
        "| Model | R-squared | MAE | RMSE |",
        "|---|---:|---:|---:|",
    ]
    for name, result in results.items():
        lines.append(
            f"| {name} | {result['r2']:.4f} | {result['mae']:.4f} | {result['rmse']:.4f} |"
        )
    return "\n".join(lines)


def coefficient_table(coefficients: pd.DataFrame, limit: int = 30) -> str:
    selected = coefficients.reindex(
        coefficients["Coefficient"].abs().sort_values(ascending=False).index
    ).head(limit)
    lines = [
        "| Feature | Coefficient | Direction |",
        "|---|---:|---|",
    ]
    for _, row in selected.iterrows():
        direction = "Positive" if row["Coefficient"] > 0 else "Negative"
        lines.append(f"| {row['Feature']} | {row['Coefficient']:.4f} | {direction} |")
    return "\n".join(lines)


def importance_table(frame: pd.DataFrame, limit: int = 20) -> str:
    lines = [
        "| Rank | Feature | Importance |",
        "|---:|---|---:|",
    ]
    for rank, (_, row) in enumerate(frame.head(limit).iterrows(), start=1):
        lines.append(f"| {rank} | {row['Feature']} | {row['Importance']:.5f} |")
    return "\n".join(lines)


def main() -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(DATA_PATH, low_memory=False)
    reported_at = pd.to_datetime(data["issue_reported_at_parsed"], errors="coerce")
    data["issue_month"] = reported_at.dt.month

    eligible = data["response_time_minutes"].ge(0) & data["CSAT Score"].between(1, 5)
    regression = data.loc[eligible, FEATURES + ["CSAT Score"]].copy()
    x = regression[FEATURES]
    y = regression["CSAT Score"].astype(float)
    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.20,
        random_state=RANDOM_STATE,
    )

    linear = Pipeline(
        steps=[
            ("preprocessor", build_preprocessor()),
            ("regressor", LinearRegression()),
        ]
    )
    forest = Pipeline(
        steps=[
            ("preprocessor", build_preprocessor()),
            (
                "regressor",
                RandomForestRegressor(
                    n_estimators=200,
                    min_samples_leaf=5,
                    max_features=0.7,
                    random_state=RANDOM_STATE,
                    n_jobs=1,
                ),
            ),
        ]
    )

    print("Training Linear Regression...")
    linear.fit(x_train, y_train)
    linear_predictions = linear.predict(x_test)
    linear_metrics = metrics(y_test, linear_predictions)

    print("Training Random Forest Regression...")
    forest.fit(x_train, y_train)
    forest_predictions = forest.predict(x_test)
    forest_metrics = metrics(y_test, forest_predictions)
    results = {
        "Linear Regression": linear_metrics,
        "Random Forest Regression": forest_metrics,
    }

    feature_names = linear.named_steps["preprocessor"].get_feature_names_out()
    clean_names = [
        name.replace("categorical__", "")
        .replace("response_time__", "")
        .replace("other_numeric__", "")
        for name in feature_names
    ]
    coefficients = pd.DataFrame(
        {
            "Feature": clean_names,
            "Coefficient": linear.named_steps["regressor"].coef_,
        }
    )

    rf_importance = pd.DataFrame(
        {
            "Feature": clean_names,
            "Importance": forest.named_steps["regressor"].feature_importances_,
        }
    ).sort_values("Importance", ascending=False)

    print("Calculating grouped permutation importance...")
    grouped_result = permutation_importance(
        forest,
        x_test,
        y_test,
        scoring="r2",
        n_repeats=5,
        random_state=RANDOM_STATE,
        n_jobs=1,
    )
    grouped_importance = pd.DataFrame(
        {
            "Feature": FEATURES,
            "Importance": grouped_result.importances_mean,
            "Std": grouped_result.importances_std,
        }
    ).sort_values("Importance", ascending=False)

    fig, axes = plt.subplots(1, 3, figsize=(12, 4.6))
    metric_specs = [("r2", "R-squared"), ("mae", "MAE"), ("rmse", "RMSE")]
    model_names = list(results)
    colors = ["#2878B5", "#D55E00"]
    for ax, (metric_key, title) in zip(axes, metric_specs):
        values = [results[name][metric_key] for name in model_names]
        bars = ax.bar(model_names, values, color=colors)
        ax.bar_label(bars, fmt="%.3f", padding=3)
        ax.set_title(title)
        ax.tick_params(axis="x", rotation=18)
        ax.grid(axis="y", alpha=0.25)
    fig.suptitle("Phase 15 Regression Metrics")
    fig.tight_layout()
    fig.savefig(FIGURES / "regression_metrics.png", dpi=160)
    plt.close(fig)

    top_rf = rf_importance.head(20).sort_values("Importance")
    fig, ax = plt.subplots(figsize=(9, 7))
    ax.barh(top_rf["Feature"], top_rf["Importance"], color="#2878B5")
    ax.set_xlabel("Random Forest impurity importance")
    ax.set_title("Phase 15 Top 20 Encoded Feature Importances")
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURES / "regression_feature_importance.png", dpi=160)
    plt.close(fig)

    response_grid = np.unique(
        np.concatenate(
            [
                np.linspace(0, 60, 25),
                np.geomspace(61, max(61, x["response_time_minutes"].quantile(0.99)), 35),
            ]
        )
    )
    pd_sample = x_test.sample(n=min(5_000, len(x_test)), random_state=RANDOM_STATE).copy()
    response_predictions = []
    for value in response_grid:
        modified = pd_sample.copy()
        modified["response_time_minutes"] = value
        response_predictions.append(forest.predict(modified).mean())

    fig, ax = plt.subplots(figsize=(8, 5.5))
    ax.plot(response_grid, response_predictions, linewidth=2.5, color="#D55E00")
    ax.set_xscale("symlog", linthresh=60)
    ax.set_xlabel("Response time (minutes, symlog scale)")
    ax.set_ylabel("Average predicted CSAT")
    ax.set_title("Partial Dependence of CSAT on Response Time")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURES / "partial_dependence_response_time.png", dpi=160)
    plt.close(fig)

    response_effect_points = [0, 5, 15, 30, 60, 240, 1_440]
    response_effect_rows = []
    for value in response_effect_points:
        modified = pd_sample.copy()
        modified["response_time_minutes"] = value
        response_effect_rows.append((value, forest.predict(modified).mean()))

    response_coefficient_row = coefficients[
        coefficients["Feature"].eq("response_time_minutes")
    ].iloc[0]
    encoded_categories = linear.named_steps["preprocessor"].named_transformers_[
        "categorical"
    ].named_steps["encoder"]
    reference_categories = {
        feature: str(categories[0])
        for feature, categories in zip(CATEGORICAL_FEATURES, encoded_categories.categories_)
    }

    coefficient_lookup = coefficients.set_index("Feature")["Coefficient"].to_dict()

    def category_coefficient(feature: str, level: str) -> float:
        if level == reference_categories[feature]:
            return 0.0
        return float(coefficient_lookup[f"{feature}_{level}"])

    channel_levels = [str(value) for value in encoded_categories.categories_[0]]
    inbound_level = next(value for value in channel_levels if value.lower().startswith("inbound"))
    selected_effects = [
        (
            f"Email vs {inbound_level}",
            category_coefficient("channel_name", "Email")
            - category_coefficient("channel_name", inbound_level),
        ),
        (
            "On Job Training vs 0-30 tenure",
            category_coefficient("Tenure Bucket", "On Job Training")
            - category_coefficient("Tenure Bucket", "0-30"),
        ),
        (
            "Morning vs Afternoon shift",
            category_coefficient("Agent Shift", "Morning")
            - category_coefficient("Agent Shift", "Afternoon"),
        ),
    ]

    driver_rows = grouped_importance.reset_index(drop=True).copy()
    positive_max = max(driver_rows["Importance"].max(), 1e-12)
    driver_rows["Relative"] = driver_rows["Importance"] / positive_max
    driver_rows["Influence"] = pd.cut(
        driver_rows["Relative"],
        bins=[-np.inf, 0.10, 0.40, np.inf],
        labels=["Low", "Medium", "High"],
    ).astype(str)

    driver_lines = [
        "| Rank | Operational Variable | Permutation Importance | Relative Influence | Class |",
        "|---:|---|---:|---:|---|",
    ]
    for rank, (_, row) in enumerate(driver_rows.head(10).iterrows(), start=1):
        driver_lines.append(
            f"| {rank} | {row['Feature']} | {row['Importance']:.5f} | "
            f"{row['Relative']:.1%} | {row['Influence']} |"
        )

    write_report(
        "phase15_regression_dataset.md",
        f"""
# Phase 15 - Regression Dataset

- Source: `data/processed/customer_support_tickets_prepared.csv`
- Source rows: {len(data):,}
- Regression rows: {len(regression):,}
- Target: `CSAT Score` (1-5)
- Train rows: {len(x_train):,}
- Test rows: {len(x_test):,}
- Split: 80/20 with `random_state=42`

Features: {", ".join(FEATURES)}.

Rows with negative response duration were excluded. Identifiers, names, sparse order/product fields, CSAT-derived flags, survey-time fields, and other leakage variables were excluded.
""",
    )

    final_matrix = linear.named_steps["preprocessor"].transform(x_train)
    write_report(
        "phase15_feature_preparation.md",
        f"""
# Phase 15 - Feature Preparation

- Categorical encoding: one-hot encoding with the first sorted category dropped as the reference level
- Missing categorical values: most-frequent imputation
- Response time: `log1p` transformation followed by z-score standardization
- Issue hour and issue month: median imputation and z-score standardization
- Training matrix dimensions: {final_matrix.shape[0]:,} rows x {final_matrix.shape[1]:,} columns
- Unseen test categories: ignored safely by the encoder

Reference categories:

{chr(10).join(f"- `{feature}`: `{value}`" for feature, value in reference_categories.items())}
""",
    )

    write_report(
        "phase15_linear_regression.md",
        f"""
# Phase 15 - Linear Regression

## Test Metrics

- R-squared: {linear_metrics['r2']:.4f}
- MAE: {linear_metrics['mae']:.4f}
- RMSE: {linear_metrics['rmse']:.4f}
- Intercept: {linear.named_steps['regressor'].intercept_:.4f}

## Largest Coefficients

{coefficient_table(coefficients)}

Categorical coefficients are CSAT-point differences from the documented reference category, holding encoded variables constant. Numeric coefficients represent a one-standard-deviation increase after transformation. Coefficients are associative, not causal.
""",
    )

    write_report(
        "phase15_random_forest_regression.md",
        f"""
# Phase 15 - Random Forest Regression

The model used 200 trees, `min_samples_leaf=5`, `max_features=0.7`, and `random_state=42`.

## Test Metrics

- R-squared: {forest_metrics['r2']:.4f}
- MAE: {forest_metrics['mae']:.4f}
- RMSE: {forest_metrics['rmse']:.4f}

## Top Encoded Feature Importances

{importance_table(rf_importance)}

Impurity importance captures nonlinear split usage but can favor variables with more possible splits. Grouped permutation importance is therefore used for the final operational-variable ranking.
""",
    )

    write_report(
        "phase15_regression_metrics.md",
        f"""
# Phase 15 - Regression Metrics

{metric_table(results)}

Higher R-squared and lower MAE/RMSE indicate better holdout performance. The stronger model is **{max(results, key=lambda name: results[name]['r2'])}** by R-squared.

![Regression metrics](figures/regression_metrics.png)
""",
    )

    write_report(
        "phase15_feature_importance.md",
        f"""
# Phase 15 - Feature Importance Ranking

## Top 20 Encoded Random Forest Features

{importance_table(rf_importance)}

## Grouped Operational-Variable Importance

{importance_table(grouped_importance, limit=10)}

Grouped values are holdout permutation importance measured as decrease in R-squared. Negative or near-zero values indicate no reliable incremental holdout contribution in this fitted model.

![Regression feature importance](figures/regression_feature_importance.png)
""",
    )

    response_lines = [
        "| Response Time | Average Predicted CSAT | Change from Immediate Response |",
        "|---:|---:|---:|",
    ]
    immediate_prediction = response_effect_rows[0][1]
    for value, prediction in response_effect_rows:
        response_lines.append(
            f"| {value:,} minutes | {prediction:.3f} | {prediction - immediate_prediction:+.3f} |"
        )
    categorical_effect_lines = [
        "| Variable Level | Linear Effect vs Reference |",
        "|---|---:|",
    ]
    for label, effect in selected_effects:
        categorical_effect_lines.append(f"| {label} | {effect:+.4f} CSAT points |")
    write_report(
        "phase15_effect_size_analysis.md",
        f"""
# Phase 15 - Effect Size Analysis

## Linear Response-Time Effect

A one-standard-deviation increase in log-transformed response time is associated with **{response_coefficient_row['Coefficient']:+.4f} CSAT points**, holding encoded predictors constant.

## Random Forest Response-Time Effects

{chr(10).join(response_lines)}

## Selected Categorical Effects

{chr(10).join(categorical_effect_lines)}

The Email contrast is derived from the fitted reference-coded coefficients because Email is the dropped channel reference. Effects are conditional associations in this specification and must not be interpreted as causal treatment effects.
""",
    )

    write_report(
        "phase15_partial_dependence.md",
        f"""
# Phase 15 - Partial Dependence Analysis

The response-time curve varies response time across a fixed 5,000-row holdout sample while retaining each record's other operational features. Predictions are averaged using the Random Forest model.

{chr(10).join(response_lines)}

The relationship is nonlinear: the largest deterioration occurs as response moves from immediate handling into longer delays, with additional decline at extended response times. The curve is model-based sensitivity analysis, not a causal estimate.

![Partial dependence of response time](figures/partial_dependence_response_time.png)
""",
    )

    write_report(
        "phase15_driver_quantification.md",
        f"""
# Phase 15 - Driver Quantification

## Joint RQ1 and RQ4 Ranking

{chr(10).join(driver_lines)}

Influence classes are relative to the strongest grouped permutation importance: High is above 40%, Medium is 10-40%, and Low is below 10%. This ranking quantifies predictive contribution to continuous CSAT, while the linear and partial-dependence reports provide direction and magnitude.
""",
    )

    top_driver = driver_rows.iloc[0]["Feature"]
    top_five = ", ".join(driver_rows.head(5)["Feature"].tolist())
    best_model = max(results, key=lambda name: results[name]["r2"])
    write_report(
        "phase15_regression_report.md",
        f"""
# Phase 15 - Regression Analysis Report

## Dataset and Models

The analysis used {len(regression):,} valid interactions to predict continuous CSAT scores from nine operational and date/time features. Linear Regression provides coefficient-based effect estimates; Random Forest Regression captures nonlinear structure.

## Performance

{metric_table(results)}

**Best predictive model: {best_model}.**

## Feature Importance

The leading grouped predictors are {top_five}. The strongest variable is **{top_driver}**.

## Effect Sizes

- A one-standard-deviation increase in log response time is associated with {response_coefficient_row['Coefficient']:+.4f} linear-model CSAT points.
- The Random Forest response-time sensitivity changes from {immediate_prediction:.3f} predicted CSAT at 0 minutes to {response_effect_rows[-1][1]:.3f} at 1,440 minutes, a difference of {response_effect_rows[-1][1] - immediate_prediction:+.3f}.
- Categorical coefficients in the detailed report quantify channel, issue, tenure, shift, and weekday levels relative to explicit references.

## RQ1 Answer

**Which operational factors matter most?**

The strongest predictive factors are {top_five}, with response time and detailed issue type expected to dominate when supported by the measured ranking. Importance describes predictive contribution, not causation.

## RQ4 Answer

**What is their relative contribution and effect size?**

Relative contribution is reported through grouped holdout permutation importance and encoded Random Forest importance. Effect magnitude is reported through linear CSAT-point coefficients and the nonlinear response-time sensitivity curve. The complete ranking is documented in `phase15_driver_quantification.md`.

## Limitations

- Regression estimates are observational and do not establish causal effects.
- R-squared quantifies explained holdout variation, not business impact by itself.
- Linear coefficients depend on reference categories and feature specification.
- Random Forest importance can distribute credit across correlated predictors.
- Temporal validation, confidence intervals, and causal controls remain future work.
""",
    )

    print()
    print(metric_table(results))
    print()
    print("Top grouped drivers:")
    for rank, (_, row) in enumerate(driver_rows.head(5).iterrows(), start=1):
        print(f"{rank}. {row['Feature']}: {row['Importance']:.5f}")
    print(f"Best model: {best_model}")


if __name__ == "__main__":
    main()
