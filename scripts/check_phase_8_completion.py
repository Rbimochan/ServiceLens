"""Verify completion of ServiceLens Phase 8 target analysis."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
REQUIRED = [
    "phase8_csat_distribution.md",
    "phase8_mean_csat.md",
    "phase8_median_csat.md",
    "phase8_mode_csat.md",
    "phase8_class_imbalance.md",
    "phase8_low_csat_rate.md",
    "phase8_high_csat_rate.md",
    "phase8_csat_visualization.md",
    "phase8_business_interpretation.md",
    "phase8_target_variable_report.md",
]
FIGURES = [
    "phase8_csat_histogram.png",
    "phase8_csat_bar_chart.png",
    "phase8_csat_percentage_distribution.png",
]
FINAL_TOPICS = {
    "Final report includes mean": "mean",
    "Final report includes median": "median",
    "Final report includes mode": "mode",
    "Final report includes class imbalance": "class imbalance",
    "Final report includes low CSAT": "low csat",
    "Final report includes high CSAT": "high csat",
    "Final report includes interpretation": "interpretation",
}


def read_report(name):
    try:
        return (REPORTS / name).read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return ""


def main():
    contents = {name: read_report(name) for name in REQUIRED}
    checks = [(f"{name} exists", (REPORTS / name).is_file()) for name in REQUIRED]
    checks.append(
        ("All required reports are non-empty", all(text.strip() for text in contents.values()))
    )

    final_report = contents["phase8_target_variable_report.md"].lower()
    checks.extend(
        (description, phrase in final_report)
        for description, phrase in FINAL_TOPICS.items()
    )
    checks.extend(
        [
            (
                "CSAT Score is documented as the target variable",
                "csat score" in final_report and "target variable" in final_report,
            ),
            (
                "Visualization report exists and is non-empty",
                bool(contents["phase8_csat_visualization.md"].strip()),
            ),
            (
                "All three CSAT figures exist and are non-empty",
                all(
                    (REPORTS / "figures" / name).is_file()
                    and (REPORTS / "figures" / name).stat().st_size > 0
                    for name in FIGURES
                ),
            ),
            (
                "Class imbalance is documented",
                "46.47:1" in contents["phase8_class_imbalance.md"],
            ),
        ]
    )

    passed = sum(result for _, result in checks)
    total = len(checks)
    missing = [name for name, result in checks if not result]

    print("ServiceLens Phase 8 Completion Checker")
    print("=" * 42)
    for number, (name, result) in enumerate(checks, start=1):
        print(f"{number:02d}. {'PASS' if result else 'FAIL'}: {name}")
    print()
    print(f"Phase 8 Completion: {passed}/{total} checks passed")
    print(f"Phase 8 Completion Percentage: {(passed / total) * 100:.0f}%")
    if missing:
        print("Missing or incomplete items:")
        for item in missing:
            print(f"- {item}")
        print("Overall Readiness for Phase 9: NOT READY")
        return 1
    print("Missing items: None")
    print("Overall Readiness for Phase 9: READY")
    return 0


sys.exit(main())
