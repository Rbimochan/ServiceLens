"""Verify completion of ServiceLens Phase 7 datetime validation."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
REQUIRED = [
    "phase7_datetime_parsing.md",
    "phase7_parsing_success.md",
    "phase7_date_ranges.md",
    "phase7_future_dates.md",
    "phase7_invalid_dates.md",
    "phase7_response_time_calculation.md",
    "phase7_negative_response_times.md",
    "phase7_time_anomalies.md",
    "phase7_timestamp_issues_summary.md",
    "phase7_datetime_validation_report.md",
]
FINAL_TOPICS = {
    "Final report references parsing": "parsing",
    "Final report references date ranges": "date ranges",
    "Final report references future dates": "future dates",
    "Final report references invalid dates": "invalid dates",
    "Final report references response times": "response times",
    "Final report references negative response times": "negative response times",
    "Final report references anomalies": "anomalies",
    "Final report references recommendations": "recommendations",
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

    final_report = contents["phase7_datetime_validation_report.md"].lower()
    checks.extend(
        (description, phrase in final_report)
        for description, phrase in FINAL_TOPICS.items()
    )
    checks.extend(
        [
            (
                "Negative response time findings are documented",
                "3,128" in contents["phase7_negative_response_times.md"]
                and "negative" in contents["phase7_negative_response_times.md"].lower(),
            ),
            (
                "Response time statistics are documented",
                all(
                    term in contents["phase7_response_time_calculation.md"].lower()
                    for term in ["minimum", "maximum", "mean", "median", "percentile"]
                ),
            ),
            (
                "Timestamp issue summary exists and is non-empty",
                bool(contents["phase7_timestamp_issues_summary.md"].strip()),
            ),
        ]
    )

    passed = sum(result for _, result in checks)
    total = len(checks)
    missing = [name for name, result in checks if not result]

    print("ServiceLens Phase 7 Completion Checker")
    print("=" * 42)
    for number, (name, result) in enumerate(checks, start=1):
        print(f"{number:02d}. {'PASS' if result else 'FAIL'}: {name}")
    print()
    print(f"Phase 7 Completion: {passed}/{total} checks passed")
    print(f"Phase 7 Completion Percentage: {(passed / total) * 100:.0f}%")
    if missing:
        print("Missing or incomplete items:")
        for item in missing:
            print(f"- {item}")
        print("Overall Readiness for Phase 8: NOT READY")
        return 1
    print("Missing items: None")
    print("Overall Readiness for Phase 8: READY")
    return 0


sys.exit(main())
