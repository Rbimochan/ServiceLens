"""Check whether ServiceLens Phase 15 regression artifacts are complete."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
FIGURES = REPORTS / "figures"

REQUIRED_REPORTS = [
    "phase15_regression_dataset.md",
    "phase15_feature_preparation.md",
    "phase15_linear_regression.md",
    "phase15_random_forest_regression.md",
    "phase15_regression_metrics.md",
    "phase15_feature_importance.md",
    "phase15_effect_size_analysis.md",
    "phase15_partial_dependence.md",
    "phase15_driver_quantification.md",
    "phase15_regression_report.md",
]

REQUIRED_FIGURES = [
    "regression_metrics.png",
    "regression_feature_importance.png",
    "partial_dependence_response_time.png",
]


def nonempty(path: Path) -> bool:
    return path.is_file() and path.stat().st_size > 0


def main() -> int:
    checks: list[tuple[str, bool]] = []

    for filename in REQUIRED_REPORTS:
        checks.append((f"Report exists and is non-empty: {filename}", nonempty(REPORTS / filename)))

    for filename in REQUIRED_FIGURES:
        checks.append((f"Figure exists and is non-empty: {filename}", nonempty(FIGURES / filename)))

    metrics_report = REPORTS / "phase15_regression_metrics.md"
    metrics_text = metrics_report.read_text(encoding="utf-8").lower() if nonempty(metrics_report) else ""
    checks.append(("Regression metrics are documented", "r-squared" in metrics_text and "mae" in metrics_text and "rmse" in metrics_text))

    importance_report = REPORTS / "phase15_feature_importance.md"
    importance_text = (
        importance_report.read_text(encoding="utf-8").lower()
        if nonempty(importance_report)
        else ""
    )
    checks.append(("Feature importance is documented", "permutation importance" in importance_text))

    effects_report = REPORTS / "phase15_effect_size_analysis.md"
    effects_text = effects_report.read_text(encoding="utf-8").lower() if nonempty(effects_report) else ""
    checks.append(("Effect sizes are documented", "csat points" in effects_text and "response time" in effects_text))

    final_report = REPORTS / "phase15_regression_report.md"
    final_text = final_report.read_text(encoding="utf-8").lower() if nonempty(final_report) else ""
    checks.append(("Final report answers RQ1", "rq1 answer" in final_text))
    checks.append(("Final report answers RQ4", "rq4 answer" in final_text))

    passed = sum(result for _, result in checks)
    total = len(checks)

    print("ServiceLens Phase 15 Completion Checker")
    print("=" * 43)
    for description, result in checks:
        print(f"{'PASS' if result else 'FAIL'}: {description}")

    print()
    print(f"Phase 15 Completion: {passed}/{total} checks passed")
    print(f"Phase 15 Completion Percentage: {(passed / total) * 100:.0f}%")

    failed = [description for description, result in checks if not result]
    if failed:
        print("Missing or incomplete items:")
        for description in failed:
            print(f"- {description}")
        print("Overall Readiness for Phase 16: NOT READY")
        return 1

    print("Missing items: None")
    print("Overall Readiness for Phase 16: READY")
    return 0


if __name__ == "__main__":
    sys.exit(main())
