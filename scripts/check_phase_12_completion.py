"""Check whether ServiceLens Phase 12 classification artifacts are complete."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
FIGURES = REPORTS / "figures"

REQUIRED_REPORTS = [
    "phase12_modeling_dataset.md",
    "phase12_train_test_split.md",
    "phase12_logistic_regression.md",
    "phase12_random_forest.md",
    "phase12_gradient_boosting.md",
    "phase12_accuracy_evaluation.md",
    "phase12_precision_recall_f1.md",
    "phase12_roc_auc.md",
    "phase12_model_comparison.md",
    "phase12_classification_report.md",
]

REQUIRED_FIGURES = [
    "accuracy_comparison.png",
    "prf1_comparison.png",
    "roc_auc_comparison.png",
]

FINAL_REPORT_TERMS = [
    "accuracy",
    "precision",
    "recall",
    "f1",
    "roc-auc",
    "best model",
    "rq2",
]


def nonempty(path: Path) -> bool:
    return path.is_file() and path.stat().st_size > 0


def main() -> int:
    checks: list[tuple[str, bool]] = []

    for filename in REQUIRED_REPORTS:
        checks.append((f"Report exists and is non-empty: {filename}", nonempty(REPORTS / filename)))

    for filename in REQUIRED_FIGURES:
        checks.append((f"Chart exists and is non-empty: {filename}", nonempty(FIGURES / filename)))

    final_report = REPORTS / "phase12_classification_report.md"
    final_text = final_report.read_text(encoding="utf-8").lower() if nonempty(final_report) else ""
    for term in FINAL_REPORT_TERMS:
        checks.append((f"Final report includes {term}", term in final_text))

    passed = sum(result for _, result in checks)
    total = len(checks)

    print("ServiceLens Phase 12 Completion Checker")
    print("=" * 43)
    for description, result in checks:
        print(f"{'PASS' if result else 'FAIL'}: {description}")

    print()
    print(f"Phase 12 Completion: {passed}/{total} checks passed")
    print(f"Phase 12 Completion Percentage: {(passed / total) * 100:.0f}%")

    failed = [description for description, result in checks if not result]
    if failed:
        print("Missing or incomplete items:")
        for description in failed:
            print(f"- {description}")
        print("Overall Readiness for Phase 13: NOT READY")
        return 1

    print("Missing items: None")
    print("Overall Readiness for Phase 13: READY")
    return 0


if __name__ == "__main__":
    sys.exit(main())
