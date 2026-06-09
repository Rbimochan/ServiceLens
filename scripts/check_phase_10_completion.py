"""Verify completion of ServiceLens Phase 10 and Milestone 1."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
REQUIRED = [
    "phase10_dataset_overview.md",
    "phase10_data_dictionary_summary.md",
    "phase10_structure_summary.md",
    "phase10_missing_value_summary.md",
    "phase10_duplicate_summary.md",
    "phase10_datetime_summary.md",
    "phase10_csat_summary.md",
    "phase10_quality_findings.md",
    "phase10_recommended_cleaning_actions.md",
    "milestone1_data_understanding_report.md",
]
FINAL_TOPICS = [
    "dataset",
    "data dictionary",
    "data structure",
    "data quality",
    "datetime",
    "csat",
    "exploratory profiling",
    "recommendations",
]


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

    final = contents["milestone1_data_understanding_report.md"].lower()
    checks.extend(
        (f"Final report references {topic}", topic in final)
        for topic in FINAL_TOPICS
    )
    checks.extend(
        [
            (
                "Final report includes executive summary",
                "executive summary" in final,
            ),
            (
                "Final report includes major risks",
                "major risks" in final,
            ),
            (
                "Final report includes modeling readiness",
                "readiness for modeling" in final,
            ),
        ]
    )

    passed = sum(result for _, result in checks)
    total = len(checks)
    missing = [name for name, result in checks if not result]

    print("ServiceLens Phase 10 Completion Checker")
    print("=" * 43)
    for number, (name, result) in enumerate(checks, start=1):
        print(f"{number:02d}. {'PASS' if result else 'FAIL'}: {name}")
    print()
    print(f"Phase 10 Completion: {passed}/{total} checks passed")
    print(f"Phase 10 Completion Percentage: {(passed / total) * 100:.0f}%")
    if missing:
        print("Missing or incomplete items:")
        for item in missing:
            print(f"- {item}")
        print("Milestone 1 Readiness: NOT READY")
        return 1
    print("Missing items: None")
    print("Milestone 1 Readiness: COMPLETE")
    return 0


sys.exit(main())
