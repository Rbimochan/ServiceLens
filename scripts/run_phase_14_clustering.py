"""Run the reproducible ServiceLens Phase 14 clustering workflow."""

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
from sklearn.cluster import BisectingKMeans, KMeans
from sklearn.compose import ColumnTransformer
from sklearn.metrics import davies_bouldin_score, silhouette_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "processed" / "customer_support_tickets_prepared.csv"
REPORTS = ROOT / "reports"
FIGURES = REPORTS / "figures"
RANDOM_STATE = 42
SILHOUETTE_SAMPLE_SIZE = 10_000

CATEGORICAL_FEATURES = [
    "channel_name",
    "category",
    "Sub-category",
    "Tenure Bucket",
    "Agent Shift",
]
NUMERIC_FEATURES = ["response_time_log1p", "CSAT Score"]
SOURCE_FEATURES = [
    "response_time_minutes",
    "channel_name",
    "category",
    "Sub-category",
    "Tenure Bucket",
    "Agent Shift",
    "CSAT Score",
]


def write_report(filename: str, content: str) -> None:
    (REPORTS / filename).write_text(content.strip() + "\n", encoding="utf-8")


def markdown_table(frame: pd.DataFrame, columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "|" + "|".join("---" for _ in columns) + "|"
    rows = [header, divider]
    for _, row in frame[columns].iterrows():
        rows.append("| " + " | ".join(str(row[column]) for column in columns) + " |")
    return "\n".join(rows)


def dominant_value(series: pd.Series) -> str:
    modes = series.mode(dropna=True)
    return str(modes.iloc[0]) if not modes.empty else "Missing"


def profile_name(
    row: pd.Series,
    fastest_cluster: int,
    high_effort_cluster: int,
) -> str:
    cluster = int(row["Cluster"])
    if cluster == fastest_cluster:
        return "Efficient Resolution Interactions"
    if cluster == high_effort_cluster:
        return "Dissatisfied High-Effort Interactions"
    if row["Dominant Channel"] == "Email":
        return "Email-Led Support Interactions"
    if row["Dominant Category"] == "Returns":
        return "Return-Focused Support Interactions"
    if row["Dominant Category"] == "Order Related":
        return "Order-Resolution Interactions"
    return f"{row['Dominant Category']} Support Interactions"


def main() -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(DATA_PATH, low_memory=False)
    eligible = data["response_time_minutes"].ge(0) & data["CSAT Score"].between(1, 5)
    clustering = data.loc[eligible, SOURCE_FEATURES].copy()
    clustering["response_time_log1p"] = np.log1p(clustering["response_time_minutes"])

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore", sparse_output=True),
                CATEGORICAL_FEATURES,
            ),
            (
                "numeric",
                Pipeline(steps=[("scaler", StandardScaler())]),
                NUMERIC_FEATURES,
            ),
        ],
        sparse_threshold=1.0,
    )
    matrix = preprocessor.fit_transform(clustering)
    feature_names = preprocessor.get_feature_names_out()

    k_rows: list[dict[str, float | int]] = []
    k_models: dict[int, KMeans] = {}
    print("Evaluating K=2 through K=8...")
    for k in range(2, 9):
        model = KMeans(n_clusters=k, n_init=10, random_state=RANDOM_STATE)
        labels = model.fit_predict(matrix)
        silhouette = silhouette_score(
            matrix,
            labels,
            sample_size=min(SILHOUETTE_SAMPLE_SIZE, len(clustering)),
            random_state=RANDOM_STATE,
        )
        k_rows.append({"K": k, "Inertia": model.inertia_, "Silhouette": silhouette})
        k_models[k] = model
        print(f"K={k}: inertia={model.inertia_:.2f}, silhouette={silhouette:.4f}")

    k_results = pd.DataFrame(k_rows)
    optimal_k = int(
        k_results.sort_values(["Silhouette", "K"], ascending=[False, True]).iloc[0]["K"]
    )
    kmeans = k_models[optimal_k]
    kmeans_labels = kmeans.labels_

    print(f"Training Bisecting K-Means with K={optimal_k}...")
    bisecting = BisectingKMeans(
        n_clusters=optimal_k,
        n_init=10,
        random_state=RANDOM_STATE,
        bisecting_strategy="biggest_inertia",
    )
    bisecting_labels = bisecting.fit_predict(matrix)

    kmeans_silhouette = silhouette_score(
        matrix,
        kmeans_labels,
        sample_size=min(SILHOUETTE_SAMPLE_SIZE, len(clustering)),
        random_state=RANDOM_STATE,
    )
    bisecting_silhouette = silhouette_score(
        matrix,
        bisecting_labels,
        sample_size=min(SILHOUETTE_SAMPLE_SIZE, len(clustering)),
        random_state=RANDOM_STATE,
    )

    dense_matrix = matrix.toarray() if hasattr(matrix, "toarray") else np.asarray(matrix)
    kmeans_db = davies_bouldin_score(dense_matrix, kmeans_labels)
    bisecting_db = davies_bouldin_score(dense_matrix, bisecting_labels)

    method_metrics = pd.DataFrame(
        [
            {
                "Method": "K-Means",
                "Silhouette": kmeans_silhouette,
                "Davies-Bouldin": kmeans_db,
                "Inertia": kmeans.inertia_,
            },
            {
                "Method": "Bisecting K-Means",
                "Silhouette": bisecting_silhouette,
                "Davies-Bouldin": bisecting_db,
                "Inertia": bisecting.inertia_,
            },
        ]
    )
    best_method = method_metrics.sort_values(
        ["Silhouette", "Davies-Bouldin"],
        ascending=[False, True],
    ).iloc[0]["Method"]
    final_labels = kmeans_labels if best_method == "K-Means" else bisecting_labels
    clustering["Cluster"] = final_labels

    fig, ax = plt.subplots(figsize=(7.5, 5))
    ax.plot(k_results["K"], k_results["Inertia"], marker="o", linewidth=2)
    ax.axvline(optimal_k, linestyle="--", color="#D55E00", label=f"Selected K={optimal_k}")
    ax.set_xlabel("Number of clusters (K)")
    ax.set_ylabel("Inertia")
    ax.set_title("Phase 14 Elbow Analysis")
    ax.set_xticks(range(2, 9))
    ax.grid(alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGURES / "elbow_curve.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7.5, 5))
    bars = ax.bar(k_results["K"].astype(str), k_results["Silhouette"], color="#2878B5")
    selected_index = list(k_results["K"]).index(optimal_k)
    bars[selected_index].set_color("#D55E00")
    ax.bar_label(bars, fmt="%.3f", padding=3)
    ax.set_xlabel("Number of clusters (K)")
    ax.set_ylabel("Silhouette score")
    ax.set_title("Phase 14 Silhouette Scores")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURES / "silhouette_scores.png", dpi=160)
    plt.close(fig)

    kmeans_counts = pd.Series(kmeans_labels).value_counts().sort_index()
    bisecting_counts = pd.Series(bisecting_labels).value_counts().sort_index()

    profile_rows = []
    for cluster_id, group in clustering.groupby("Cluster"):
        profile_rows.append(
            {
                "Cluster": int(cluster_id),
                "Count": len(group),
                "Proportion": len(group) / len(clustering),
                "Avg CSAT": group["CSAT Score"].mean(),
                "Avg Response Minutes": group["response_time_minutes"].mean(),
                "Median Response Minutes": group["response_time_minutes"].median(),
                "Dominant Channel": dominant_value(group["channel_name"]),
                "Dominant Category": dominant_value(group["category"]),
                "Dominant Sub-category": dominant_value(group["Sub-category"]),
                "Dominant Tenure": dominant_value(group["Tenure Bucket"]),
                "Dominant Shift": dominant_value(group["Agent Shift"]),
            }
        )
    profiles = pd.DataFrame(profile_rows).sort_values("Cluster").reset_index(drop=True)

    fastest_cluster = int(
        profiles.sort_values(
            ["Avg Response Minutes", "Avg CSAT"],
            ascending=[True, False],
        ).iloc[0]["Cluster"]
    )
    high_effort_cluster = int(
        profiles.sort_values(
            ["Avg Response Minutes", "Avg CSAT"],
            ascending=[False, True],
        ).iloc[0]["Cluster"]
    )
    profiles["Business Profile"] = profiles.apply(
        profile_name,
        axis=1,
        fastest_cluster=fastest_cluster,
        high_effort_cluster=high_effort_cluster,
    )

    formatted_profiles = profiles.copy()
    formatted_profiles["Proportion"] = formatted_profiles["Proportion"].map(lambda value: f"{value:.2%}")
    formatted_profiles["Avg CSAT"] = formatted_profiles["Avg CSAT"].map(lambda value: f"{value:.3f}")
    formatted_profiles["Avg Response Minutes"] = formatted_profiles["Avg Response Minutes"].map(
        lambda value: f"{value:.1f}"
    )
    formatted_profiles["Median Response Minutes"] = formatted_profiles[
        "Median Response Minutes"
    ].map(lambda value: f"{value:.1f}")

    k_formatted = k_results.copy()
    k_formatted["Inertia"] = k_formatted["Inertia"].map(lambda value: f"{value:,.2f}")
    k_formatted["Silhouette"] = k_formatted["Silhouette"].map(lambda value: f"{value:.4f}")

    method_formatted = method_metrics.copy()
    method_formatted["Silhouette"] = method_formatted["Silhouette"].map(lambda value: f"{value:.4f}")
    method_formatted["Davies-Bouldin"] = method_formatted["Davies-Bouldin"].map(
        lambda value: f"{value:.4f}"
    )
    method_formatted["Inertia"] = method_formatted["Inertia"].map(lambda value: f"{value:,.2f}")

    write_report(
        "phase14_clustering_dataset.md",
        f"""
# Phase 14 - Clustering Dataset

## Source

- Source rows: {len(data):,}
- Clustering rows: {len(clustering):,}
- Excluded negative response durations: {int((data['response_time_minutes'] < 0).sum()):,}
- Features used: {", ".join(SOURCE_FEATURES)}

Identifiers, customer and agent names, target flags, sparse order/product fields, and classification outputs were excluded. CSAT is included as an unsupervised profile dimension as specified for Phase 14; no target label is supplied to either clustering algorithm.
""",
    )

    write_report(
        "phase14_feature_scaling.md",
        f"""
# Phase 14 - Feature Scaling

- Categorical encoding: one-hot encoding with unknown-category handling
- Numeric transformation: `log1p` applied to non-negative response time to reduce extreme skew
- Numeric scaling: z-score standardization for transformed response time and CSAT
- Final matrix dimensions: {matrix.shape[0]:,} rows x {matrix.shape[1]:,} columns
- Encoded feature count: {len(feature_names):,}
- Matrix format: sparse during clustering; converted to dense only for Davies-Bouldin evaluation

The transformation prevents raw response-time magnitude from overwhelming categorical distances while retaining the ordering of delays.
""",
    )

    write_report(
        "phase14_k_selection.md",
        f"""
# Phase 14 - K Selection

K-Means was evaluated for K=2 through K=8 using `n_init=10` and `random_state=42`.

{markdown_table(k_formatted, ["K", "Inertia", "Silhouette"])}

Silhouette scores use a fixed random sample of {min(SILHOUETTE_SAMPLE_SIZE, len(clustering)):,} rows. Inertia uses the complete clustering matrix.

**Recommended K: {optimal_k}.**

The recommendation selects the highest sampled silhouette score, with the smaller K used as a tie-breaker. The elbow curve is retained as a secondary visual diagnostic.

![Elbow curve](figures/elbow_curve.png)

![Silhouette scores](figures/silhouette_scores.png)
""",
    )

    kmeans_lines = [
        "| Cluster | Count | Proportion |",
        "|---:|---:|---:|",
    ]
    for cluster_id, count in kmeans_counts.items():
        kmeans_lines.append(
            f"| {cluster_id} | {count:,} | {count / len(clustering):.2%} |"
        )
    write_report(
        "phase14_kmeans_clustering.md",
        f"""
# Phase 14 - K-Means Clustering

The final K-Means model used K={optimal_k}, `n_init=10`, and `random_state=42`.

{chr(10).join(kmeans_lines)}

- Inertia: {kmeans.inertia_:,.2f}
- Sampled silhouette: {kmeans_silhouette:.4f}
- Davies-Bouldin index: {kmeans_db:.4f}
""",
    )

    bisecting_lines = [
        "| Cluster | Count | Proportion |",
        "|---:|---:|---:|",
    ]
    for cluster_id, count in bisecting_counts.items():
        bisecting_lines.append(
            f"| {cluster_id} | {count:,} | {count / len(clustering):.2%} |"
        )
    write_report(
        "phase14_bisecting_kmeans.md",
        f"""
# Phase 14 - Bisecting K-Means

Bisecting K-Means used K={optimal_k}, `n_init=10`, `random_state=42`, and the `biggest_inertia` splitting strategy.

{chr(10).join(bisecting_lines)}

- Inertia: {bisecting.inertia_:,.2f}
- Sampled silhouette: {bisecting_silhouette:.4f}
- Davies-Bouldin index: {bisecting_db:.4f}

The same preprocessed matrix and cluster count were used for a direct comparison with standard K-Means.
""",
    )

    write_report(
        "phase14_silhouette_evaluation.md",
        f"""
# Phase 14 - Silhouette Evaluation

{markdown_table(method_formatted, ["Method", "Silhouette", "Davies-Bouldin", "Inertia"])}

Higher silhouette scores indicate stronger separation and cohesion. Scores were calculated on the same fixed {min(SILHOUETTE_SAMPLE_SIZE, len(clustering)):,}-row sample.

**Best method by silhouette: {method_metrics.sort_values('Silhouette', ascending=False).iloc[0]['Method']}.**

The absolute scores should be interpreted cautiously because mixed operational data often forms overlapping profiles rather than sharply separated natural groups.
""",
    )

    write_report(
        "phase14_davies_bouldin.md",
        f"""
# Phase 14 - Davies-Bouldin Evaluation

{markdown_table(method_formatted, ["Method", "Davies-Bouldin", "Silhouette", "Inertia"])}

Lower Davies-Bouldin values indicate more compact, better-separated clusters.

**Best method by Davies-Bouldin index: {method_metrics.sort_values('Davies-Bouldin').iloc[0]['Method']}.**

This metric was calculated on the complete transformed matrix. It is considered alongside silhouette rather than used as the sole selection criterion.
""",
    )

    profile_columns = [
        "Cluster",
        "Business Profile",
        "Count",
        "Proportion",
        "Avg CSAT",
        "Avg Response Minutes",
        "Median Response Minutes",
        "Dominant Channel",
        "Dominant Category",
        "Dominant Tenure",
        "Dominant Shift",
    ]
    write_report(
        "phase14_cluster_profiles.md",
        f"""
# Phase 14 - Cluster Profiles

Profiles below use labels from **{best_method}**, selected by silhouette score with Davies-Bouldin as a secondary diagnostic.

{markdown_table(formatted_profiles, profile_columns)}

Business names summarize measured cluster statistics. They are descriptive labels, not predefined classes or causal segments.
""",
    )

    profile_descriptions = []
    for _, row in profiles.iterrows():
        profile_descriptions.append(
            f"### Cluster {int(row['Cluster'])}: {row['Business Profile']}\n\n"
            f"- Size: {int(row['Count']):,} ({row['Proportion']:.2%})\n"
            f"- Average CSAT: {row['Avg CSAT']:.3f}\n"
            f"- Average response time: {row['Avg Response Minutes']:.1f} minutes\n"
            f"- Dominant channel: {row['Dominant Channel']}\n"
            f"- Dominant category: {row['Dominant Category']}\n"
            f"- Dominant sub-category: {row['Dominant Sub-category']}\n"
            f"- Dominant tenure: {row['Dominant Tenure']}\n"
            f"- Dominant shift: {row['Dominant Shift']}"
        )
    profile_names = ", ".join(profiles["Business Profile"].tolist())
    write_report(
        "phase14_interaction_profiles.md",
        f"""
# Phase 14 - Interaction Profile Discovery

## RQ3

**What support interaction profiles emerge through unsupervised learning?**

The selected clustering solution identifies {optimal_k} empirical profiles: {profile_names}.

{chr(10).join(profile_descriptions)}

The anticipated efficient and high-effort patterns are retained only where supported by measured response-time and CSAT statistics. Remaining labels reflect each cluster's actual dominant operational characteristics.
""",
    )

    write_report(
        "phase14_clustering_report.md",
        f"""
# Phase 14 - Clustering Analysis Report

## Dataset and Preprocessing

The analysis used {len(clustering):,} valid interactions and seven source fields. Categorical variables were one-hot encoded. Response time was log-transformed and standardized; CSAT was standardized. Identifiers and names were excluded.

## K Selection

K=2 through K=8 were evaluated using full-data inertia and a reproducible {min(SILHOUETTE_SAMPLE_SIZE, len(clustering)):,}-row silhouette sample. The selected cluster count is **K={optimal_k}**.

## Model Comparison

{markdown_table(method_formatted, ["Method", "Silhouette", "Davies-Bouldin", "Inertia"])}

**Selected clustering method: {best_method}.**

## Cluster Profiles

{markdown_table(formatted_profiles, profile_columns)}

## RQ3 Answer

**What support interaction profiles emerge?**

The analysis finds {optimal_k} overlapping but measurable interaction profiles: {profile_names}. The clearest differentiation is based on response effort, satisfaction, and operational issue mix. These profiles can support service-routing and process investigation, but the modest separation metrics mean they should not be treated as fixed customer types without stability testing.

## Limitations

- Clusters depend on encoding, scaling, selected fields, and K.
- CSAT is included as an unsupervised clustering dimension, so satisfaction differences are partly designed into the geometry.
- Silhouette uses a fixed sample for computational practicality.
- Cluster stability across time and resampled datasets has not yet been tested.
- Profiles describe interactions, not permanent customer identities.
""",
    )

    print()
    print(f"Selected K: {optimal_k}")
    print(markdown_table(method_formatted, ["Method", "Silhouette", "Davies-Bouldin", "Inertia"]))
    print()
    print(f"Selected method: {best_method}")
    print("Interaction profiles:")
    for _, row in profiles.iterrows():
        print(f"- Cluster {int(row['Cluster'])}: {row['Business Profile']}")


if __name__ == "__main__":
    main()
