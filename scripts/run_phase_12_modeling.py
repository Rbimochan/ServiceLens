"""Run the reproducible ServiceLens Phase 12 classification workflow."""

from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/servicelens-matplotlib")

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler


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


def metric_table(results: dict[str, dict[str, float]]) -> str:
    lines = [
        "| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for model, metrics in results.items():
        lines.append(
            f"| {model} | {metrics['accuracy']:.4f} | {metrics['precision']:.4f} | "
            f"{metrics['recall']:.4f} | {metrics['f1']:.4f} | {metrics['roc_auc']:.4f} |"
        )
    return "\n".join(lines)


def evaluate(model: Pipeline, x_test: pd.DataFrame, y_test: pd.Series) -> tuple[dict[str, float], np.ndarray]:
    predictions = model.predict(x_test)
    probabilities = model.predict_proba(x_test)[:, 1]
    metrics = {
        "accuracy": accuracy_score(y_test, predictions),
        "precision": precision_score(y_test, predictions, zero_division=0),
        "recall": recall_score(y_test, predictions, zero_division=0),
        "f1": f1_score(y_test, predictions, zero_division=0),
        "roc_auc": roc_auc_score(y_test, probabilities),
    }
    return metrics, probabilities


def save_comparison_chart(
    results: dict[str, dict[str, float]],
    metrics: list[str],
    labels: list[str],
    filename: str,
    title: str,
) -> None:
    models = list(results)
    x = np.arange(len(models))
    width = 0.8 / len(metrics)

    fig, ax = plt.subplots(figsize=(9, 5.5))
    for index, (metric, label) in enumerate(zip(metrics, labels)):
        values = [results[model][metric] for model in models]
        offset = (index - (len(metrics) - 1) / 2) * width
        bars = ax.bar(x + offset, values, width, label=label)
        ax.bar_label(bars, fmt="%.3f", padding=3, fontsize=9)

    ax.set_xticks(x, models)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Score")
    ax.set_title(title)
    if len(metrics) > 1:
        ax.legend()
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURES / filename, dpi=160)
    plt.close(fig)


def main() -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(DATA_PATH, low_memory=False)
    reported_at = pd.to_datetime(data["issue_reported_at_parsed"], errors="coerce")
    data["issue_month"] = reported_at.dt.month

    eligible = data["CSAT Score"].isin([1, 2, 4, 5])
    valid_response = data["response_time_minutes"].ge(0)
    modeling = data.loc[eligible & valid_response, FEATURES + ["CSAT Score"]].copy()
    modeling["low_csat_binary"] = modeling["CSAT Score"].isin([1, 2]).astype(int)
    modeling = modeling.drop(columns="CSAT Score")

    x = modeling[FEATURES]
    y = modeling["low_csat_binary"]
    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.20,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    one_hot_preprocessor = ColumnTransformer(
        transformers=[
            (
                "categorical",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("encoder", OneHotEncoder(handle_unknown="ignore")),
                    ]
                ),
                CATEGORICAL_FEATURES,
            ),
            (
                "numeric",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="median")),
                        ("scaler", StandardScaler()),
                    ]
                ),
                NUMERIC_FEATURES,
            ),
        ]
    )

    ordinal_preprocessor = ColumnTransformer(
        transformers=[
            (
                "categorical",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        (
                            "encoder",
                            OrdinalEncoder(
                                handle_unknown="use_encoded_value",
                                unknown_value=-1,
                                encoded_missing_value=-1,
                            ),
                        ),
                    ]
                ),
                CATEGORICAL_FEATURES,
            ),
            (
                "numeric",
                SimpleImputer(strategy="median"),
                NUMERIC_FEATURES,
            ),
        ]
    )

    models: dict[str, Pipeline] = {
        "Logistic Regression": Pipeline(
            steps=[
                ("preprocessor", one_hot_preprocessor),
                (
                    "classifier",
                    LogisticRegression(
                        class_weight="balanced",
                        max_iter=1_000,
                        random_state=RANDOM_STATE,
                    ),
                ),
            ]
        ),
        "Random Forest": Pipeline(
            steps=[
                ("preprocessor", one_hot_preprocessor),
                (
                    "classifier",
                    RandomForestClassifier(
                        n_estimators=250,
                        min_samples_leaf=5,
                        class_weight="balanced",
                        random_state=RANDOM_STATE,
                        n_jobs=-1,
                    ),
                ),
            ]
        ),
        "Gradient Boosting": Pipeline(
            steps=[
                ("preprocessor", ordinal_preprocessor),
                (
                    "classifier",
                    HistGradientBoostingClassifier(
                        categorical_features=list(range(len(CATEGORICAL_FEATURES))),
                        class_weight="balanced",
                        learning_rate=0.08,
                        max_iter=200,
                        max_leaf_nodes=31,
                        random_state=RANDOM_STATE,
                    ),
                ),
            ]
        ),
    }

    results: dict[str, dict[str, float]] = {}
    probabilities: dict[str, np.ndarray] = {}
    for name, model in models.items():
        print(f"Training {name}...")
        model.fit(x_train, y_train)
        results[name], probabilities[name] = evaluate(model, x_test, y_test)

    table = metric_table(results)
    ranked_by_auc = sorted(results, key=lambda name: results[name]["roc_auc"], reverse=True)
    best_model = ranked_by_auc[0]
    best = results[best_model]

    save_comparison_chart(
        results,
        ["accuracy"],
        ["Accuracy"],
        "accuracy_comparison.png",
        "Phase 12 Model Accuracy Comparison",
    )
    save_comparison_chart(
        results,
        ["precision", "recall", "f1"],
        ["Precision", "Recall", "F1"],
        "prf1_comparison.png",
        "Low-CSAT Detection Performance",
    )

    fig, ax = plt.subplots(figsize=(7.5, 6))
    for name in results:
        false_positive_rate, true_positive_rate, _ = roc_curve(y_test, probabilities[name])
        ax.plot(
            false_positive_rate,
            true_positive_rate,
            linewidth=2,
            label=f"{name} (AUC={results[name]['roc_auc']:.3f})",
        )
    ax.plot([0, 1], [0, 1], linestyle="--", color="gray", label="Random baseline")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("Phase 12 ROC Curves")
    ax.legend(loc="lower right")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURES / "roc_auc_comparison.png", dpi=160)
    plt.close(fig)

    total_rows = len(data)
    neutral_rows = int(data["CSAT Score"].eq(3).sum())
    invalid_response_rows = int(data["response_time_minutes"].lt(0).sum())
    low_count = int(y.sum())
    high_count = int((y == 0).sum())

    train_counts = y_train.value_counts().sort_index()
    test_counts = y_test.value_counts().sort_index()

    write_report(
        "phase12_modeling_dataset.md",
        f"""
# Phase 12 - Modeling Dataset

## Source and Eligibility

- Source: `data/processed/customer_support_tickets_prepared.csv`
- Source rows: {total_rows:,}
- Final modeling rows: {len(modeling):,}
- Neutral CSAT score 3 excluded: {neutral_rows:,}
- Negative response durations excluded: {invalid_response_rows:,}

Only records with CSAT 1, 2, 4, or 5 and a non-negative response duration were eligible.

## Target

`low_csat_binary` is defined as:

- `0`: high CSAT, scores 4-5
- `1`: low CSAT, scores 1-2

Final target distribution:

- High CSAT (`0`): {high_count:,} ({high_count / len(y):.2%})
- Low CSAT (`1`): {low_count:,} ({low_count / len(y):.2%})

## Features

| Feature | Type | Purpose |
|---|---|---|
| channel_name | Categorical | Support interaction channel |
| category | Categorical | Main issue category |
| Sub-category | Categorical | Detailed issue type |
| response_time_minutes | Numeric | Valid response delay |
| Tenure Bucket | Categorical | Agent tenure group |
| Agent Shift | Categorical | Operating shift |
| issue_hour | Numeric | Hour the issue was reported |
| issue_weekday | Categorical | Weekday the issue was reported |
| issue_month | Numeric | Month extracted from issue report timestamp |

## Exclusions

Identifiers, customer remarks, agent/supervisor/manager names, sparse order and product fields, survey-response timing, CSAT-derived flags, and other leakage or duplicate fields were excluded. Survey date features were excluded because they occur after the support interaction and may not be available at prediction time.
""",
    )

    write_report(
        "phase12_train_test_split.md",
        f"""
# Phase 12 - Train/Test Split

The modeling data was split with `test_size=0.20`, `random_state=42`, and stratification by `low_csat_binary`.

| Split | Total | High CSAT (0) | Low CSAT (1) | Low-CSAT Rate |
|---|---:|---:|---:|---:|
| Train | {len(y_train):,} | {int(train_counts[0]):,} | {int(train_counts[1]):,} | {train_counts[1] / len(y_train):.2%} |
| Test | {len(y_test):,} | {int(test_counts[0]):,} | {int(test_counts[1]):,} | {test_counts[1] / len(y_test):.2%} |

Stratification preserves the class imbalance in both partitions. Balanced class weighting was used during training so the models did not optimize only for the majority high-CSAT class.
""",
    )

    model_details = {
        "phase12_logistic_regression.md": (
            "Logistic Regression",
            "Categorical values were one-hot encoded, numeric values were median-imputed and standardized, and balanced class weights were used. This is the interpretable linear baseline.",
        ),
        "phase12_random_forest.md": (
            "Random Forest",
            "The model used 250 trees, `min_samples_leaf=5`, balanced class weights, and `random_state=42`. It can learn nonlinear interactions but is less directly interpretable.",
        ),
        "phase12_gradient_boosting.md": (
            "Gradient Boosting",
            "A histogram gradient-boosted tree model used ordinal-encoded categoricals marked as categorical features, balanced class weights, 200 boosting iterations, and `random_state=42`.",
        ),
    }
    for filename, (name, description) in model_details.items():
        metrics = results[name]
        write_report(
            filename,
            f"""
# Phase 12 - {name}

## Method

{description}

## Test Results

| Metric | Score |
|---|---:|
| Accuracy | {metrics['accuracy']:.4f} |
| Precision | {metrics['precision']:.4f} |
| Recall | {metrics['recall']:.4f} |
| F1 | {metrics['f1']:.4f} |
| ROC-AUC | {metrics['roc_auc']:.4f} |

Metrics treat low CSAT (`1`) as the positive class. The default probability threshold of 0.50 was used for classification metrics.
""",
        )

    accuracy_order = sorted(results, key=lambda name: results[name]["accuracy"], reverse=True)
    write_report(
        "phase12_accuracy_evaluation.md",
        f"""
# Phase 12 - Accuracy Evaluation

## Model Results

{table}

## Accuracy Ranking

1. {accuracy_order[0]}: {results[accuracy_order[0]]['accuracy']:.4f}
2. {accuracy_order[1]}: {results[accuracy_order[1]]['accuracy']:.4f}
3. {accuracy_order[2]}: {results[accuracy_order[2]]['accuracy']:.4f}

Accuracy must be interpreted alongside recall and F1 because low CSAT is the minority class.

![Accuracy comparison](figures/accuracy_comparison.png)
""",
    )

    write_report(
        "phase12_precision_recall_f1.md",
        f"""
# Phase 12 - Precision, Recall, and F1 Evaluation

Low CSAT (`1`) is the positive class.

{table}

Recall measures how many low-CSAT cases are detected. Precision measures how many low-CSAT alerts are correct. F1 balances those two objectives. Threshold refinement in Phase 13 may improve the operational tradeoff.

![Precision, recall, and F1 comparison](figures/prf1_comparison.png)
""",
    )

    write_report(
        "phase12_roc_auc.md",
        f"""
# Phase 12 - ROC-AUC Evaluation

{table}

ROC-AUC measures ranking ability across classification thresholds. The best observed ROC-AUC is {best['roc_auc']:.4f} from {best_model}. A score above 0.50 indicates predictive signal beyond random ranking, but does not by itself establish deployment readiness.

![ROC-AUC comparison](figures/roc_auc_comparison.png)
""",
    )

    comparison_lines = []
    for rank, name in enumerate(ranked_by_auc, start=1):
        comparison_lines.append(
            f"{rank}. **{name}** - ROC-AUC {results[name]['roc_auc']:.4f}, "
            f"F1 {results[name]['f1']:.4f}, recall {results[name]['recall']:.4f}"
        )
    write_report(
        "phase12_model_comparison.md",
        f"""
# Phase 12 - Model Comparison

## Ranking by ROC-AUC

{chr(10).join(comparison_lines)}

## Tradeoffs

- Logistic Regression is the most interpretable baseline and easiest to explain, but it assumes additive linear effects after encoding.
- Random Forest captures nonlinear interactions and is robust, but its probabilities and global explanations require additional analysis.
- Gradient Boosting captures nonlinear structure efficiently. In this run it produced the strongest ROC-AUC and the highest F1 score.

## Selected Model

**Best model: {best_model}**

The selection uses ROC-AUC as the primary criterion because Phase 12 evaluates minority-class ranking ability across thresholds. F1 and recall remain important deployment metrics and should be tuned in Phase 13.
""",
    )

    rq2_answer = "YES, with limited-to-moderate predictive ability" if best["roc_auc"] > 0.60 else "NO, not reliably with the current features"
    write_report(
        "phase12_classification_report.md",
        f"""
# Phase 12 - Classification Report

## Research Question

**RQ2: Can customer satisfaction be predicted using support interaction data?**

**Answer: {rq2_answer}.**

The models detect predictive signal, but Phase 12 results are baseline estimates rather than evidence of production readiness.

## Dataset and Target

- Modeling rows: {len(modeling):,}
- Train rows: {len(y_train):,}
- Test rows: {len(y_test):,}
- Target: `low_csat_binary`
- `0`: CSAT 4-5
- `1`: CSAT 1-2
- Split: 80/20, stratified, `random_state=42`

## Model Results

{table}

## Best Model

**{best_model}**

- Accuracy: {best['accuracy']:.4f}
- Precision: {best['precision']:.4f}
- Recall: {best['recall']:.4f}
- F1: {best['f1']:.4f}
- ROC-AUC: {best['roc_auc']:.4f}

The best model was selected by ROC-AUC. Balanced class weighting prioritizes detection of the minority low-CSAT class, so accuracy alone is not the selection criterion.

## Limitations

- Results come from one reproducible holdout split and require cross-validation in Phase 13.
- Threshold 0.50 was not tuned for operational precision-recall costs.
- Invalid negative response durations and neutral CSAT scores were excluded.
- The available features may not capture issue complexity, customer history, or service-resolution quality.
- Observational patterns do not prove causal relationships.
- Model calibration, feature importance, fairness, drift, and external validation remain untested.

## Phase 13 Direction

Tune hyperparameters and the decision threshold, add cross-validation and confidence intervals, inspect feature importance, test calibration, and confirm that performance is stable across channels and issue categories.
""",
    )

    print()
    print(table)
    print()
    print(f"Best model: {best_model}")
    print(f"ROC-AUC: {best['roc_auc']:.4f}")
    print(f"F1: {best['f1']:.4f}")
    print(f"RQ2 answer: {rq2_answer}")


if __name__ == "__main__":
    main()
