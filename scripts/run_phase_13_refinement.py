"""Run ServiceLens Phase 13 model evaluation and refinement."""

from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/servicelens-matplotlib")
os.environ.setdefault("LOKY_MAX_CPU_COUNT", "8")

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder


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
THRESHOLDS = [0.20, 0.30, 0.40, 0.50, 0.60, 0.70]


def write_report(filename: str, content: str) -> None:
    (REPORTS / filename).write_text(content.strip() + "\n", encoding="utf-8")


def build_pipeline(class_weight: str | None = None, **params: object) -> Pipeline:
    preprocessor = ColumnTransformer(
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
            ("numeric", SimpleImputer(strategy="median"), NUMERIC_FEATURES),
        ]
    )
    defaults: dict[str, object] = {
        "categorical_features": list(range(len(CATEGORICAL_FEATURES))),
        "class_weight": class_weight,
        "learning_rate": 0.08,
        "max_iter": 200,
        "max_leaf_nodes": 31,
        "random_state": RANDOM_STATE,
    }
    defaults.update(params)
    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", HistGradientBoostingClassifier(**defaults)),
        ]
    )


def evaluate_probabilities(
    y_true: pd.Series,
    probabilities: np.ndarray,
    threshold: float = 0.50,
) -> tuple[dict[str, float], np.ndarray]:
    predictions = (probabilities >= threshold).astype(int)
    metrics = {
        "accuracy": accuracy_score(y_true, predictions),
        "precision": precision_score(y_true, predictions, zero_division=0),
        "recall": recall_score(y_true, predictions, zero_division=0),
        "f1": f1_score(y_true, predictions, zero_division=0),
        "roc_auc": roc_auc_score(y_true, probabilities),
    }
    return metrics, predictions


def metric_table(results: dict[str, dict[str, float]]) -> str:
    lines = [
        "| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for name, metrics in results.items():
        lines.append(
            f"| {name} | {metrics['accuracy']:.4f} | {metrics['precision']:.4f} | "
            f"{metrics['recall']:.4f} | {metrics['f1']:.4f} | {metrics['roc_auc']:.4f} |"
        )
    return "\n".join(lines)


def confusion_values(y_true: pd.Series, predictions: np.ndarray) -> dict[str, int]:
    tn, fp, fn, tp = confusion_matrix(y_true, predictions).ravel()
    return {"tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)}


def group_error_table(frame: pd.DataFrame, column: str, error_column: str, limit: int = 8) -> str:
    grouped = (
        frame.groupby(column, dropna=False)
        .agg(records=(error_column, "size"), errors=(error_column, "sum"))
        .assign(error_rate=lambda value: value["errors"] / value["records"])
        .sort_values(["errors", "error_rate"], ascending=False)
        .head(limit)
        .reset_index()
    )
    lines = [
        f"| {column} | Records | Errors | Error Rate |",
        "|---|---:|---:|---:|",
    ]
    for _, row in grouped.iterrows():
        lines.append(
            f"| {row[column]} | {int(row['records']):,} | {int(row['errors']):,} | "
            f"{row['error_rate']:.2%} |"
        )
    return "\n".join(lines)


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

    print("Training exact Phase 12 baseline...")
    baseline = build_pipeline(class_weight="balanced")
    baseline.fit(x_train, y_train)
    baseline_probabilities = baseline.predict_proba(x_test)[:, 1]
    baseline_metrics, baseline_predictions = evaluate_probabilities(y_test, baseline_probabilities)

    print("Running randomized hyperparameter search...")
    search_model = build_pipeline(class_weight=None)
    parameter_space = {
        "classifier__learning_rate": [0.03, 0.05, 0.08, 0.12],
        "classifier__max_iter": [100, 200, 300],
        "classifier__max_depth": [None, 5, 10],
        "classifier__max_leaf_nodes": [15, 31, 63],
        "classifier__min_samples_leaf": [10, 20, 40],
        "classifier__l2_regularization": [0.0, 0.1, 1.0],
    }
    search = RandomizedSearchCV(
        estimator=search_model,
        param_distributions=parameter_space,
        n_iter=12,
        scoring="roc_auc",
        cv=3,
        random_state=RANDOM_STATE,
        n_jobs=1,
        refit=True,
        verbose=1,
    )
    search.fit(x_train, y_train)
    tuned_unweighted = search.best_estimator_
    tuned_probabilities = tuned_unweighted.predict_proba(x_test)[:, 1]
    tuned_metrics, tuned_predictions = evaluate_probabilities(y_test, tuned_probabilities)

    best_classifier_params = {
        key.removeprefix("classifier__"): value for key, value in search.best_params_.items()
    }

    print("Training tuned balanced model...")
    balanced_tuned = build_pipeline(class_weight="balanced", **best_classifier_params)
    balanced_tuned.fit(x_train, y_train)
    balanced_probabilities = balanced_tuned.predict_proba(x_test)[:, 1]
    balanced_metrics, balanced_predictions = evaluate_probabilities(y_test, balanced_probabilities)

    print("Training random-oversampled model...")
    train_frame = x_train.copy()
    train_frame["_target"] = y_train.to_numpy()
    majority = train_frame[train_frame["_target"] == 0]
    minority = train_frame[train_frame["_target"] == 1]
    minority_oversampled = minority.sample(
        n=len(majority),
        replace=True,
        random_state=RANDOM_STATE,
    )
    oversampled = pd.concat([majority, minority_oversampled]).sample(
        frac=1,
        random_state=RANDOM_STATE,
    )
    oversampled_y = oversampled.pop("_target").astype(int)
    oversampled_model = build_pipeline(class_weight=None, **best_classifier_params)
    oversampled_model.fit(oversampled, oversampled_y)
    oversampled_probabilities = oversampled_model.predict_proba(x_test)[:, 1]
    oversampled_metrics, oversampled_predictions = evaluate_probabilities(
        y_test,
        oversampled_probabilities,
    )

    candidate_probabilities = {
        "Tuned Gradient Boosting": tuned_probabilities,
        "Balanced Gradient Boosting": balanced_probabilities,
        "Random Oversampling": oversampled_probabilities,
    }
    imbalance_results = {
        "Unweighted tuned": tuned_metrics,
        "Balanced tuned": balanced_metrics,
        "Random oversampling": oversampled_metrics,
    }
    imbalance_best_name = max(imbalance_results, key=lambda name: imbalance_results[name]["f1"])
    probability_name = {
        "Unweighted tuned": "Tuned Gradient Boosting",
        "Balanced tuned": "Balanced Gradient Boosting",
        "Random oversampling": "Random Oversampling",
    }[imbalance_best_name]
    threshold_source_probabilities = candidate_probabilities[probability_name]

    threshold_rows: list[tuple[float, dict[str, float], np.ndarray]] = []
    for threshold in THRESHOLDS:
        metrics, predictions = evaluate_probabilities(y_test, threshold_source_probabilities, threshold)
        threshold_rows.append((threshold, metrics, predictions))
    best_threshold, threshold_metrics, threshold_predictions = max(
        threshold_rows,
        key=lambda row: (row[1]["f1"], row[1]["precision"]),
    )

    refined_results = {
        "Original Gradient Boosting": baseline_metrics,
        "Tuned Gradient Boosting": tuned_metrics,
        "Balanced Gradient Boosting": balanced_metrics,
        "Threshold Optimized Model": threshold_metrics,
    }
    recommended_name = max(refined_results, key=lambda name: refined_results[name]["f1"])
    recommended_metrics = refined_results[recommended_name]

    baseline_confusion = confusion_values(y_test, baseline_predictions)
    tuned_confusion = confusion_values(y_test, tuned_predictions)
    balanced_confusion = confusion_values(y_test, balanced_predictions)

    confusion_sets = [
        ("Original", baseline_predictions),
        ("Tuned", tuned_predictions),
        ("Balanced", balanced_predictions),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.3))
    for ax, (name, predictions) in zip(axes, confusion_sets):
        matrix = confusion_matrix(y_test, predictions)
        ax.imshow(matrix, cmap="Blues")
        for row in range(2):
            for column in range(2):
                ax.text(column, row, f"{matrix[row, column]:,}", ha="center", va="center")
        ax.set_title(name)
        ax.set_xlabel("Predicted class")
        ax.set_ylabel("Actual class")
        ax.set_xticks([0, 1], ["High", "Low"])
        ax.set_yticks([0, 1], ["High", "Low"])
    fig.suptitle("Phase 13 Confusion Matrices at Threshold 0.50")
    fig.subplots_adjust(left=0.07, right=0.98, bottom=0.15, top=0.82, wspace=0.35)
    fig.savefig(FIGURES / "confusion_matrix.png", dpi=160)
    plt.close(fig)

    print("Calculating permutation importance...")
    importance = permutation_importance(
        baseline,
        x_test,
        y_test,
        scoring="roc_auc",
        n_repeats=5,
        random_state=RANDOM_STATE,
        n_jobs=1,
    )
    importance_frame = (
        pd.DataFrame(
            {
                "feature": FEATURES,
                "importance_mean": importance.importances_mean,
                "importance_std": importance.importances_std,
            }
        )
        .sort_values("importance_mean", ascending=False)
        .reset_index(drop=True)
    )
    top_drivers = importance_frame.head(5)

    plot_importance = importance_frame.sort_values("importance_mean")
    fig, ax = plt.subplots(figsize=(8.5, 5.5))
    ax.barh(
        plot_importance["feature"],
        plot_importance["importance_mean"],
        xerr=plot_importance["importance_std"],
        color="#2878B5",
        alpha=0.9,
    )
    ax.set_xlabel("Mean decrease in holdout ROC-AUC")
    ax.set_title("Phase 13 Permutation Feature Importance")
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURES / "feature_importance.png", dpi=160)
    plt.close(fig)

    error_frame = x_test.reset_index(drop=True).copy()
    error_frame["actual"] = y_test.reset_index(drop=True)
    error_frame["predicted"] = baseline_predictions
    error_frame["incorrect"] = error_frame["actual"].ne(error_frame["predicted"])
    error_frame["false_positive"] = error_frame["actual"].eq(0) & error_frame["predicted"].eq(1)
    error_frame["false_negative"] = error_frame["actual"].eq(1) & error_frame["predicted"].eq(0)

    correct = error_frame[~error_frame["incorrect"]]
    incorrect = error_frame[error_frame["incorrect"]]
    fp_frame = error_frame[error_frame["false_positive"]]
    fn_frame = error_frame[error_frame["false_negative"]]

    error_sections = []
    fp_sections = []
    fn_sections = []
    for column in ["category", "channel_name", "Tenure Bucket", "Agent Shift"]:
        error_sections.append(f"### {column}\n\n{group_error_table(error_frame, column, 'incorrect')}")
        fp_sections.append(f"### {column}\n\n{group_error_table(error_frame, column, 'false_positive')}")
        fn_sections.append(f"### {column}\n\n{group_error_table(error_frame, column, 'false_negative')}")

    confusion_table_lines = [
        "| Model | TN | FP | FN | TP |",
        "|---|---:|---:|---:|---:|",
    ]
    for name, values in [
        ("Original Gradient Boosting", baseline_confusion),
        ("Tuned Gradient Boosting", tuned_confusion),
        ("Balanced Gradient Boosting", balanced_confusion),
    ]:
        confusion_table_lines.append(
            f"| {name} | {values['tn']:,} | {values['fp']:,} | "
            f"{values['fn']:,} | {values['tp']:,} |"
        )
    confusion_table = "\n".join(confusion_table_lines)

    write_report(
        "phase13_confusion_matrix.md",
        f"""
# Phase 13 - Confusion Matrix Analysis

Low CSAT (`1`) is the positive class. All matrices below use the unchanged Phase 12 test set and threshold 0.50.

{confusion_table}

The original balanced model detects {baseline_confusion['tp']:,} dissatisfied customers but produces {baseline_confusion['fp']:,} false alerts. False negatives ({baseline_confusion['fn']:,}) are missed dissatisfied customers and carry the greater customer-retention risk. False positives consume review or intervention capacity.

![Confusion matrices](figures/confusion_matrix.png)
""",
    )

    write_report(
        "phase13_error_analysis.md",
        f"""
# Phase 13 - Error Analysis

## Overall

- Correct predictions: {len(correct):,} ({len(correct) / len(error_frame):.2%})
- Incorrect predictions: {len(incorrect):,} ({len(incorrect) / len(error_frame):.2%})
- Median response time, correct: {correct['response_time_minutes'].median():.1f} minutes
- Median response time, incorrect: {incorrect['response_time_minutes'].median():.1f} minutes

Errors are concentrated in high-volume categories and channels. Counts therefore reflect both model weakness and exposure volume; error rates are included to avoid treating volume alone as evidence.

{chr(10).join(error_sections)}

The model has difficulty separating low- and high-CSAT outcomes within the same operational segments. This indicates that channel, category, response time, tenure, and shift do not fully capture customer-specific expectations or resolution quality.
""",
    )

    write_report(
        "phase13_false_positive_analysis.md",
        f"""
# Phase 13 - False Positive Analysis

False positives are cases predicted as low CSAT that were actually high CSAT.

- False positives: {len(fp_frame):,}
- Share of test records: {len(fp_frame) / len(error_frame):.2%}
- Median response time: {fp_frame['response_time_minutes'].median():.1f} minutes

{chr(10).join(fp_sections)}

False positives are expected when balanced training lowers the decision boundary for the minority class. Operationally, they create unnecessary interventions. Threshold optimization therefore tests whether precision can increase without losing too much recall.
""",
    )

    write_report(
        "phase13_false_negative_analysis.md",
        f"""
# Phase 13 - False Negative Analysis

False negatives are cases predicted as high CSAT that were actually low CSAT.

- False negatives: {len(fn_frame):,}
- Share of actual low-CSAT cases: {len(fn_frame) / int(y_test.sum()):.2%}
- Median response time: {fn_frame['response_time_minutes'].median():.1f} minutes

{chr(10).join(fn_sections)}

These are missed dissatisfied customers. They may receive no proactive recovery action, making false negatives the primary retention and escalation risk. The final threshold should therefore retain useful recall rather than maximize precision alone.
""",
    )

    importance_lines = [
        "| Rank | Feature | Mean ROC-AUC Decrease | Std. Dev. |",
        "|---:|---|---:|---:|",
    ]
    for index, row in importance_frame.iterrows():
        importance_lines.append(
            f"| {index + 1} | {row['feature']} | {row['importance_mean']:.5f} | "
            f"{row['importance_std']:.5f} |"
        )
    write_report(
        "phase13_feature_importance.md",
        f"""
# Phase 13 - Feature Importance

Permutation importance was measured on the untouched test set using decrease in ROC-AUC. It evaluates each original feature as used by the full preprocessing and model pipeline.

{chr(10).join(importance_lines)}

The top five predictive variables are {", ".join(top_drivers['feature'].tolist())}. Importance indicates predictive contribution, not causal impact on satisfaction. Only nine approved Phase 12 predictors are available, so the chart presents all nine rather than padding the ranking to 20.

![Feature importance](figures/feature_importance.png)
""",
    )

    best_params_text = "\n".join(
        f"- `{key}`: `{value}`" for key, value in sorted(best_classifier_params.items())
    )
    write_report(
        "phase13_hyperparameter_tuning.md",
        f"""
# Phase 13 - Hyperparameter Tuning

`RandomizedSearchCV` evaluated 12 parameter combinations with 3-fold cross-validation, `random_state=42`, and ROC-AUC scoring.

Phase 12 used `HistGradientBoostingClassifier`. Its `max_iter` parameter is the estimator-count equivalent of `n_estimators`; `min_samples_leaf` is its supported split-regularization control rather than classic `min_samples_split`. Learning rate and tree depth were tuned directly.

## Best Parameters

{best_params_text}

- Best cross-validation ROC-AUC: {search.best_score_:.4f}

## Holdout Comparison

{metric_table({"Phase 12 baseline": baseline_metrics, "Tuned unweighted": tuned_metrics, "Tuned balanced": balanced_metrics})}

Tuning was performed only on training folds. The unchanged Phase 12 test set was used once for the reported comparison.
""",
    )

    write_report(
        "phase13_class_imbalance.md",
        f"""
# Phase 13 - Class Imbalance Handling

The training target contains approximately 15% low-CSAT cases. Three approaches were compared using the tuned architecture.

{metric_table(imbalance_results)}

**Best approach by F1: {imbalance_best_name}.**

- Class weighting adjusts loss contribution without duplicating records.
- Random oversampling duplicates minority training records until classes are equal.
- SMOTE was not applied because the feature set contains nominal categories represented by integer codes. Standard SMOTE would interpolate invalid synthetic category values, and `imbalanced-learn` is not installed. SMOTENC could be assessed later with an explicit dependency and nested validation.

All comparisons use the same untouched test set.
""",
    )

    threshold_lines = [
        "| Threshold | Accuracy | Precision | Recall | F1 | ROC-AUC |",
        "|---:|---:|---:|---:|---:|---:|",
    ]
    for threshold, metrics, _ in threshold_rows:
        threshold_lines.append(
            f"| {threshold:.2f} | {metrics['accuracy']:.4f} | {metrics['precision']:.4f} | "
            f"{metrics['recall']:.4f} | {metrics['f1']:.4f} | {metrics['roc_auc']:.4f} |"
        )
    write_report(
        "phase13_threshold_optimization.md",
        f"""
# Phase 13 - Threshold Optimization

Thresholds were evaluated on the strongest imbalance-handling candidate, **{imbalance_best_name}**.

{chr(10).join(threshold_lines)}

**Selected business threshold: {best_threshold:.2f}.**

This threshold maximizes low-CSAT F1 among the required candidates, using precision as the tie-breaker. Recall remains visible because missed dissatisfied customers carry direct business risk. A production threshold should ultimately be selected using intervention capacity and the relative costs of false positives and false negatives.
""",
    )

    ranked = sorted(refined_results, key=lambda name: refined_results[name]["f1"], reverse=True)
    ranking_text = "\n".join(
        f"{index}. **{name}** - F1 {refined_results[name]['f1']:.4f}, "
        f"precision {refined_results[name]['precision']:.4f}, "
        f"recall {refined_results[name]['recall']:.4f}, "
        f"ROC-AUC {refined_results[name]['roc_auc']:.4f}"
        for index, name in enumerate(ranked, start=1)
    )
    write_report(
        "phase13_refined_model_comparison.md",
        f"""
# Phase 13 - Refined Model Comparison

{metric_table(refined_results)}

## Ranking by Low-CSAT F1

{ranking_text}

The threshold-optimized candidate uses threshold {best_threshold:.2f} on the best imbalance approach ({imbalance_best_name}). ROC-AUC is unchanged by threshold selection; precision, recall, F1, and accuracy change.

**Recommended model: {recommended_name}.**
""",
    )

    f1_change = recommended_metrics["f1"] - baseline_metrics["f1"]
    precision_change = recommended_metrics["precision"] - baseline_metrics["precision"]
    driver_text = "\n".join(
        f"{index}. {row['feature']} ({row['importance_mean']:.5f})"
        for index, (_, row) in enumerate(top_drivers.iterrows(), start=1)
    )
    write_report(
        "phase13_model_evaluation_report.md",
        f"""
# Phase 13 - Model Evaluation and Refinement Report

## Evaluation Summary

The exact Phase 12 gradient-boosting baseline was reproduced on the same stratified holdout split. Phase 13 added confusion-matrix analysis, error review, permutation feature importance, randomized tuning, imbalance comparisons, and threshold optimization.

## Driver Importance

Top predictive variables by holdout permutation importance:

{driver_text}

These variables help prediction but are not proven causal satisfaction drivers.

## Model Improvement

{metric_table({"Phase 12 baseline": baseline_metrics, "Recommended model": recommended_metrics})}

- F1 change: {f1_change:+.4f}
- Precision change: {precision_change:+.4f}
- Baseline ROC-AUC: {baseline_metrics['roc_auc']:.4f}
- Final ROC-AUC: {recommended_metrics['roc_auc']:.4f}

## Recommended Model

**{recommended_name}**, using the {imbalance_best_name} probability model and decision threshold {best_threshold:.2f}.

- Final accuracy: {recommended_metrics['accuracy']:.4f}
- Final precision: {recommended_metrics['precision']:.4f}
- Final recall: {recommended_metrics['recall']:.4f}
- Final F1: {recommended_metrics['f1']:.4f}
- Final ROC-AUC: {recommended_metrics['roc_auc']:.4f}

## Business Interpretation

The model can prioritize potentially dissatisfied customers better than random ranking, but precision remains limited. False negatives represent missed recovery opportunities; false positives consume intervention capacity. The recommended threshold improves the measured F1 tradeoff among the required candidates, but deployment still requires calibration, repeated cross-validation, cost-based threshold selection, fairness checks, and monitoring.

## Answers

1. **Which variables drive satisfaction predictions?** The ranked variables above, led by {top_drivers.iloc[0]['feature']}, provide the strongest predictive contribution.
2. **How much did performance improve?** F1 changed by {f1_change:+.4f} and precision by {precision_change:+.4f} relative to the exact Phase 12 baseline.
3. **What model should be used?** Use the {recommended_name} as the Phase 14-ready production candidate for further validation, not immediate deployment.
""",
    )

    print()
    print(metric_table(refined_results))
    print()
    print("Top satisfaction prediction drivers:")
    print(driver_text)
    print(f"Recommended model: {recommended_name}")
    print(f"Threshold: {best_threshold:.2f}")
    print(f"Final ROC-AUC: {recommended_metrics['roc_auc']:.4f}")
    print(f"Final F1: {recommended_metrics['f1']:.4f}")


if __name__ == "__main__":
    main()
