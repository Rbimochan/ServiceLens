"""Verify completion of ServiceLens Phase 4 data dictionary artifacts."""

from __future__ import annotations

import csv
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT / "reports"
PROCESSED_DATASET = ROOT / "data" / "processed" / "customer_support_tickets_prepared.csv"

REQUIRED_REPORTS = [
    "phase4_column_inventory.md",
    "phase4_business_meaning.md",
    "phase4_datatype_documentation.md",
    "phase4_variable_roles.md",
    "phase4_target_variables.md",
    "phase4_feature_variables.md",
    "phase4_metadata_fields.md",
    "phase4_text_fields.md",
    "phase4_master_data_dictionary.md",
    "phase4_data_dictionary_report.md",
]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return ""


def processed_columns() -> list[str]:
    try:
        with PROCESSED_DATASET.open(encoding="utf-8-sig", newline="") as handle:
            return next(csv.reader(handle))
    except (OSError, StopIteration, csv.Error):
        return []


def main() -> int:
    checks: list[tuple[str, bool]] = []

    for report_name in REQUIRED_REPORTS:
        report_path = REPORTS_DIR / report_name
        checks.append((f"{report_name} exists", report_path.is_file()))

    report_contents = {
        report_name: read_text(REPORTS_DIR / report_name)
        for report_name in REQUIRED_REPORTS
    }
    checks.append(
        (
            "All required reports are non-empty",
            all(content.strip() for content in report_contents.values()),
        )
    )

    master = report_contents["phase4_master_data_dictionary.md"]
    master_lower = master.lower()
    required_master_headers = ["column name", "datatype", "variable role"]
    checks.append(
        (
            "Master dictionary contains column name, datatype, and variable role",
            all(header in master_lower for header in required_master_headers),
        )
    )

    dataset_columns = processed_columns()
    checks.append(
        (
            "Master dictionary documents every processed dataset column",
            bool(dataset_columns)
            and all(f"`{column}`" in master for column in dataset_columns),
        )
    )

    target_text = report_contents["phase4_target_variables.md"] + master
    checks.append(
        (
            "CSAT variable is documented",
            "CSAT Score" in target_text and "csat_score" in target_text,
        )
    )

    completion_report = REPORTS_DIR / "phase4_data_dictionary_report.md"
    checks.append(
        (
            "Phase 4 completion report exists and is non-empty",
            completion_report.is_file() and bool(read_text(completion_report).strip()),
        )
    )

    passed = sum(result for _, result in checks)
    total = len(checks)
    percentage = (passed / total) * 100
    missing_items = [name for name, result in checks if not result]

    print("ServiceLens Phase 4 Completion Checker")
    print("=" * 42)
    for index, (name, result) in enumerate(checks, start=1):
        status = "PASS" if result else "FAIL"
        print(f"{index:02d}. {status}: {name}")

    print()
    print(f"Phase 4 Completion: {passed}/{total} checks passed")
    print(f"Phase 4 Completion Percentage: {percentage:.0f}%")

    if missing_items:
        print("Missing or incomplete items:")
        for item in missing_items:
            print(f"- {item}")
        print("Overall Readiness for Phase 5: NOT READY")
        return 1

    print("Missing items: None")
    print("Overall Readiness for Phase 5: READY")
    return 0


if __name__ == "__main__":
    sys.exit(main())
