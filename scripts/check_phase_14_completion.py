"""Check whether ServiceLens Phase 14 clustering artifacts are complete."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
FIGURES = REPORTS / "figures"

REQUIRED_REPORTS = [
    "phase14_clustering_dataset.md",
    "phase14_feature_scaling.md",
    "phase14_k_selection.md",
    "phase14_kmeans_clustering.md",
    "phase14_bisecting_kmeans.md",
    "phase14_silhouette_evaluation.md",
    "phase14_davies_bouldin.md",
    "phase14_cluster_profiles.md",
    "phase14_interaction_profiles.md",
    "phase14_clustering_report.md",
]

REQUIRED_FIGURES = ["elbow_curve.png", "silhouette_scores.png"]


def nonempty(path: Path) -> bool:
    return path.is_file() and path.stat().st_size > 0


def main() -> int:
    checks: list[tuple[str, bool]] = []

    for filename in REQUIRED_REPORTS:
        checks.append((f"Report exists and is non-empty: {filename}", nonempty(REPORTS / filename)))

    for filename in REQUIRED_FIGURES:
        checks.append((f"Figure exists and is non-empty: {filename}", nonempty(FIGURES / filename)))

    metrics_report = REPORTS / "phase14_silhouette_evaluation.md"
    metrics_text = metrics_report.read_text(encoding="utf-8").lower() if nonempty(metrics_report) else ""
    checks.append(("Clustering metrics are documented", "silhouette" in metrics_text and "davies-bouldin" in metrics_text))

    profile_report = REPORTS / "phase14_cluster_profiles.md"
    profile_text = profile_report.read_text(encoding="utf-8").lower() if nonempty(profile_report) else ""
    checks.append(("Cluster profiles are documented", "avg csat" in profile_text and "dominant channel" in profile_text))

    interaction_report = REPORTS / "phase14_interaction_profiles.md"
    interaction_text = (
        interaction_report.read_text(encoding="utf-8").lower()
        if nonempty(interaction_report)
        else ""
    )
    checks.append(("Interaction profiles are documented", "business profile" in profile_text and "rq3" in interaction_text))

    final_report = REPORTS / "phase14_clustering_report.md"
    final_text = final_report.read_text(encoding="utf-8").lower() if nonempty(final_report) else ""
    checks.append(("Final report answers RQ3", "rq3 answer" in final_text and "what support interaction profiles emerge" in final_text))

    passed = sum(result for _, result in checks)
    total = len(checks)

    print("ServiceLens Phase 14 Completion Checker")
    print("=" * 43)
    for description, result in checks:
        print(f"{'PASS' if result else 'FAIL'}: {description}")

    print()
    print(f"Phase 14 Completion: {passed}/{total} checks passed")
    print(f"Phase 14 Completion Percentage: {(passed / total) * 100:.0f}%")

    failed = [description for description, result in checks if not result]
    if failed:
        print("Missing or incomplete items:")
        for description in failed:
            print(f"- {description}")
        print("Overall Readiness for Phase 15: NOT READY")
        return 1

    print("Missing items: None")
    print("Overall Readiness for Phase 15: READY")
    return 0


if __name__ == "__main__":
    sys.exit(main())
