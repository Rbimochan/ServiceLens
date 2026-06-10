"""Check whether ServiceLens Phase 13 refinement artifacts are complete."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
FIGURES = REPORTS / "figures"

REQUIRED_REPORTS = [
    "phase13_confusion_matrix.md",
    "phase13_error_analysis.md",
    "phase13_false_positive_analysis.md",
    "phase13_false_negative_analysis.md",
    "phase13_feature_importance.md",
    "phase13_hyperparameter_tuning.md",
    "phase13_class_imbalance.md",
    "phase13_threshold_optimization.md",
    "phase13_refined_model_comparison.md",
    "phase13_model_evaluation_report.md",
]

REQUIRED_FIGURES = ["confusion_matrix.png", "feature_importance.png"]

FINAL_REPORT_TERMS = [
    "driver importance",
    "model improvement",
    "recommended model",
    "final roc-auc",
    "final f1",
]


def nonempty(path: Path) -> bool:
    return path.is_file() and path.stat().st_size > 0


def main() -> int:
    checks: list[tuple[str, bool]] = []

    for filename in REQUIRED_REPORTS:
        checks.append((f"Report exists and is non-empty: {filename}", nonempty(REPORTS / filename)))

    for filename in REQUIRED_FIGURES:
        checks.append((f"Figure exists and is non-empty: {filename}", nonempty(FIGURES / filename)))

    feature_report = REPORTS / "phase13_feature_importance.md"
    feature_text = feature_report.read_text(encoding="utf-8").lower() if nonempty(feature_report) else ""
    checks.append(("Feature importance is documented", "permutation importance" in feature_text))

    tuning_report = REPORTS / "phase13_hyperparameter_tuning.md"
    tuning_text = tuning_report.read_text(encoding="utf-8").lower() if nonempty(tuning_report) else ""
    checks.append(("Hyperparameter tuning is documented", "randomizedsearchcv" in tuning_text))

    imbalance_report = REPORTS / "phase13_class_imbalance.md"
    imbalance_text = (
        imbalance_report.read_text(encoding="utf-8").lower()
        if nonempty(imbalance_report)
        else ""
    )
    checks.append(("Imbalance handling is documented", "oversampling" in imbalance_text))

    final_report = REPORTS / "phase13_model_evaluation_report.md"
    final_text = final_report.read_text(encoding="utf-8").lower() if nonempty(final_report) else ""
    for term in FINAL_REPORT_TERMS:
        checks.append((f"Final report includes {term}", term in final_text))

    passed = sum(result for _, result in checks)
    total = len(checks)

    print("ServiceLens Phase 13 Completion Checker")
    print("=" * 43)
    for description, result in checks:
        print(f"{'PASS' if result else 'FAIL'}: {description}")

    print()
    print(f"Phase 13 Completion: {passed}/{total} checks passed")
    print(f"Phase 13 Completion Percentage: {(passed / total) * 100:.0f}%")

    failed = [description for description, result in checks if not result]
    if failed:
        print("Missing or incomplete items:")
        for description in failed:
            print(f"- {description}")
        print("Overall Readiness for Phase 14: NOT READY")
        return 1

    print("Missing items: None")
    print("Overall Readiness for Phase 14: READY")
    return 0


if __name__ == "__main__":
    sys.exit(main())
