"""Verify completion of ServiceLens Phase 9 exploratory profiling."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
REQUIRED = [
    "phase9_support_channels.md",
    "phase9_categories.md",
    "phase9_subcategories.md",
    "phase9_agent_performance.md",
    "phase9_supervisor_performance.md",
    "phase9_manager_performance.md",
    "phase9_tenure_buckets.md",
    "phase9_agent_shifts.md",
    "phase9_key_patterns.md",
    "phase9_exploratory_profiling_report.md",
]
FINAL_SECTIONS = [
    "channel analysis",
    "category analysis",
    "sub-category analysis",
    "agent findings",
    "supervisor findings",
    "manager findings",
    "tenure findings",
    "shift findings",
    "key patterns",
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
    final = contents["phase9_exploratory_profiling_report.md"].lower()
    checks.extend(
        (f"Final report references {section}", section in final)
        for section in FINAL_SECTIONS
    )
    checks.append(
        (
            "Key patterns report exists and is non-empty",
            bool(contents["phase9_key_patterns.md"].strip()),
        )
    )

    passed = sum(result for _, result in checks)
    total = len(checks)
    missing = [name for name, result in checks if not result]
    print("ServiceLens Phase 9 Completion Checker")
    print("=" * 42)
    for number, (name, result) in enumerate(checks, start=1):
        print(f"{number:02d}. {'PASS' if result else 'FAIL'}: {name}")
    print()
    print(f"Phase 9 Completion: {passed}/{total} checks passed")
    print(f"Phase 9 Completion Percentage: {(passed / total) * 100:.0f}%")
    if missing:
        print("Missing or incomplete items:")
        for item in missing:
            print(f"- {item}")
        print("Overall Readiness for Phase 10: NOT READY")
        return 1
    print("Missing items: None")
    print("Overall Readiness for Phase 10: READY")
    return 0


sys.exit(main())
