#!/usr/bin/env python3
"""Check ServiceLens Phase 3 Data Preparation completion.

This script verifies Phase 3 artifacts only. It does not perform new data
analysis, modify files, overwrite datasets, or commit anything.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DATASET = PROJECT_ROOT / "data" / "raw" / "customer_support_tickets.csv"
PROCESSED_DATASET = (
    PROJECT_ROOT / "data" / "processed" / "customer_support_tickets_prepared.csv"
)

REQUIRED_REPORTS = [
    PROJECT_ROOT / "reports" / "phase3_missing_value_strategy.md",
    PROJECT_ROOT / "reports" / "phase3_duplicate_analysis.md",
    PROJECT_ROOT / "reports" / "phase3_datatype_correction.md",
    PROJECT_ROOT / "reports" / "phase3_datetime_engineering.md",
    PROJECT_ROOT / "reports" / "phase3_ticket_lifecycle_features.md",
    PROJECT_ROOT / "reports" / "phase3_text_cleaning_pipeline.md",
    PROJECT_ROOT / "reports" / "phase3_categorical_encoding_plan.md",
    PROJECT_ROOT / "reports" / "phase3_feature_engineering.md",
    PROJECT_ROOT / "reports" / "phase3_processed_dataset_generation.md",
    PROJECT_ROOT / "reports" / "phase3_data_preparation_report.md",
]


def print_check(condition: bool, message: str) -> bool:
    status = "PASS" if condition else "FAIL"
    print(f"{status} {message}")
    return condition


def file_exists(path: Path) -> bool:
    return path.is_file()


def non_empty_file(path: Path) -> bool:
    return path.is_file() and path.stat().st_size > 0


def git_status_porcelain(path: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain", "--", str(path.relative_to(PROJECT_ROOT))],
            cwd=PROJECT_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    except (OSError, ValueError):
        return ""
    return result.stdout.strip()


def raw_dataset_not_modified_if_possible() -> bool:
    status = git_status_porcelain(RAW_DATASET)
    if not status:
        return True

    # Ignored raw files may appear as clean with --porcelain. If Git reports a
    # tracked modification, deletion, addition, rename, or copy, treat it as not
    # clean for Phase 3 completion.
    return False


def raw_csv_not_staged() -> bool:
    status = git_status_porcelain(RAW_DATASET)
    if not status:
        return True

    # In porcelain format, the first character is the index/staged status.
    return all(line[:1] in (" ", "?") for line in status.splitlines())


def main() -> int:
    print("ServiceLens Phase 3 Completion Check\n")

    checks: list[tuple[bool, str]] = [
        (file_exists(RAW_DATASET), "raw dataset exists"),
        (file_exists(PROCESSED_DATASET), "processed dataset exists"),
        (file_exists(REQUIRED_REPORTS[0]), "missing value report exists"),
        (file_exists(REQUIRED_REPORTS[1]), "duplicate analysis report exists"),
        (file_exists(REQUIRED_REPORTS[2]), "datatype correction report exists"),
        (file_exists(REQUIRED_REPORTS[3]), "datetime engineering report exists"),
        (file_exists(REQUIRED_REPORTS[4]), "ticket lifecycle feature report exists"),
        (file_exists(REQUIRED_REPORTS[5]), "text cleaning report exists"),
        (file_exists(REQUIRED_REPORTS[6]), "categorical encoding plan exists"),
        (file_exists(REQUIRED_REPORTS[7]), "feature engineering report exists"),
        (file_exists(REQUIRED_REPORTS[8]), "processed dataset generation report exists"),
        (file_exists(REQUIRED_REPORTS[9]), "final Phase 3 data preparation report exists"),
        (raw_dataset_not_modified_if_possible(), "raw dataset was not modified if Git can verify it"),
        (non_empty_file(PROCESSED_DATASET), "processed dataset is not empty"),
        (
            all(non_empty_file(path) for path in REQUIRED_REPORTS),
            "all Phase 3 report files are not empty",
        ),
        (raw_csv_not_staged(), "raw CSV is not staged for Git"),
    ]

    missing_items: list[str] = []
    passed = 0
    for condition, message in checks:
        if print_check(condition, message):
            passed += 1
        else:
            missing_items.append(message)

    total = len(checks)
    print(f"\nPhase 3 Completion: {passed}/{total} checks passed")
    print(f"Phase 3 Completion Percentage: {passed / total:.0%}")

    print("\nMissing Items")
    if missing_items:
        for item in missing_items:
            print(f"- {item}")
    else:
        print("- None")

    print("\nOverall Readiness for Phase 4:")
    if passed == total:
        print("READY — Phase 3 Data Preparation artifacts are complete.")
        return 0

    print("NOT READY — fix missing or failed items before Phase 4.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
