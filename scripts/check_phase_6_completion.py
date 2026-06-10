"""Verify ServiceLens Phase 6 reports and Git staging safety."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
REQUIRED = [
    "phase6_missing_values.md",
    "phase6_missing_percentages.md",
    "phase6_missingness_ranking.md",
    "phase6_duplicate_rows.md",
    "phase6_duplicate_ids.md",
    "phase6_invalid_values.md",
    "phase6_empty_strings.md",
    "phase6_label_consistency.md",
    "phase6_quality_issues_summary.md",
    "phase6_data_quality_report.md",
]
TOPICS = {
    "Final report mentions missing values": "missing value",
    "Final report mentions duplicates": "duplicate",
    "Final report mentions invalid values": "invalid value",
    "Final report mentions empty strings": "empty string",
    "Final report mentions label consistency": "label consistency",
    "Final report mentions recommended cleaning actions": "recommended cleaning action",
}


def read_report(name):
    try:
        return (REPORTS / name).read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return ""


def staged_paths():
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return [path for path in result.stdout.splitlines() if path]


def main():
    contents = {name: read_report(name) for name in REQUIRED}
    checks = [(f"{name} exists", (REPORTS / name).is_file()) for name in REQUIRED]
    checks.append(
        ("All required reports are non-empty", all(text.strip() for text in contents.values()))
    )
    final_report = contents["phase6_data_quality_report.md"].lower()
    checks.extend((label, phrase in final_report) for label, phrase in TOPICS.items())
    staged = staged_paths()
    checks.append(
        ("Raw dataset is not staged", staged is not None and not any(
            path.startswith("data/raw/") for path in staged
        ))
    )
    checks.append(
        ("Processed dataset is not staged", staged is not None and not any(
            path.startswith("data/processed/") and not path.endswith(".gitkeep")
            for path in staged
        ))
    )
    checks.append(
        ("Notebook checkpoints are not staged", staged is not None and not any(
            ".ipynb_checkpoints/" in path for path in staged
        ))
    )
    passed = sum(result for _, result in checks)
    total = len(checks)
    missing = [name for name, result in checks if not result]
    print("ServiceLens Phase 6 Completion Checker")
    print("=" * 42)
    for number, (name, result) in enumerate(checks, start=1):
        print(f"{number:02d}. {'PASS' if result else 'FAIL'}: {name}")
    print()
    print(f"Phase 6 Completion: {passed}/{total} checks passed")
    print(f"Phase 6 Completion Percentage: {(passed / total) * 100:.0f}%")
    if missing:
        print("Missing or incomplete items:")
        for item in missing:
            print(f"- {item}")
        print("Overall Readiness for Phase 7: NOT READY")
        return 1
    print("Missing items: None")
    print("Overall Readiness for Phase 7: READY")
    return 0


sys.exit(main())
