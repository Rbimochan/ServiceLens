"""Verify completion of ServiceLens Phase 5 structure-analysis artifacts."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
REQUIRED = [
    "phase5_dataframe_info.md",
    "phase5_numeric_columns.md",
    "phase5_categorical_columns.md",
    "phase5_datetime_columns.md",
    "phase5_text_columns.md",
    "phase5_datatype_verification.md",
    "phase5_type_mismatches.md",
    "phase5_structural_issues.md",
    "phase5_schema_summary.md",
    "phase5_data_structure_report.md",
]


def read_report(name: str) -> str:
    try:
        return (REPORTS / name).read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return ""


def main() -> int:
    contents = {name: read_report(name) for name in REQUIRED}
    checks: list[tuple[str, bool]] = [
        (f"{name} exists", (REPORTS / name).is_file()) for name in REQUIRED
    ]
    checks.append(
        ("All required reports are non-empty", all(text.strip() for text in contents.values()))
    )

    schema = contents["phase5_schema_summary.md"].lower()
    checks.extend(
        [
            ("Schema summary exists and is non-empty", bool(schema.strip())),
            (
                "Numeric section exists",
                "numeric" in contents["phase5_numeric_columns.md"].lower(),
            ),
            (
                "Categorical section exists",
                "categorical" in contents["phase5_categorical_columns.md"].lower(),
            ),
            (
                "Datetime section exists",
                "datetime" in contents["phase5_datetime_columns.md"].lower(),
            ),
            (
                "Schema summary contains required structure fields",
                all(
                    term in schema
                    for term in ["column", "actual dtype", "expected type", "role", "missing"]
                ),
            ),
        ]
    )

    passed = sum(result for _, result in checks)
    total = len(checks)
    missing = [name for name, result in checks if not result]

    print("ServiceLens Phase 5 Completion Checker")
    print("=" * 42)
    for number, (name, result) in enumerate(checks, start=1):
        print(f"{number:02d}. {'PASS' if result else 'FAIL'}: {name}")

    print()
    print(f"Phase 5 Completion: {passed}/{total} checks passed")
    print(f"Phase 5 Completion Percentage: {(passed / total) * 100:.0f}%")
    if missing:
        print("Missing or incomplete items:")
        for item in missing:
            print(f"- {item}")
        print("Overall Readiness for Phase 6: NOT READY")
        return 1

    print("Missing items: None")
    print("Overall Readiness for Phase 6: READY")
    return 0


if __name__ == "__main__":
    sys.exit(main())
