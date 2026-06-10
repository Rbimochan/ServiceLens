"""Check whether ServiceLens Phase 11 EDA artifacts are complete."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
FIGURES = REPORTS / "figures"

REQUIRED_REPORTS = [
    "phase11_univariate_analysis.md",
    "phase11_bivariate_analysis.md",
    "phase11_csat_vs_channel.md",
    "phase11_csat_vs_category.md",
    "phase11_csat_vs_response_time.md",
    "phase11_csat_vs_tenure.md",
    "phase11_csat_vs_shift.md",
    "phase11_correlation_analysis.md",
    "phase11_driver_analysis.md",
    "phase11_eda_report.md",
]

REQUIRED_FIGURES = [
    "phase11_univariate_overview.png",
    "channel_csat.png",
    "category_csat.png",
    "response_time_csat.png",
    "tenure_csat.png",
    "shift_csat.png",
    "correlation_heatmap.png",
]

FINAL_REPORT_TOPICS = [
    "channel",
    "category",
    "response time",
    "tenure",
    "shift",
    "correlation",
    "driver",
]


def nonempty(path: Path) -> bool:
    return path.is_file() and path.stat().st_size > 0


def main() -> int:
    checks: list[tuple[str, bool]] = []

    for filename in REQUIRED_REPORTS:
        checks.append((f"Report exists and is non-empty: {filename}", nonempty(REPORTS / filename)))

    for filename in REQUIRED_FIGURES:
        checks.append((f"Figure exists and is non-empty: {filename}", nonempty(FIGURES / filename)))

    final_report = REPORTS / "phase11_eda_report.md"
    final_text = final_report.read_text(encoding="utf-8").lower() if nonempty(final_report) else ""
    for topic in FINAL_REPORT_TOPICS:
        checks.append((f"Final report documents {topic}", topic in final_text))

    driver_report = REPORTS / "phase11_driver_analysis.md"
    driver_text = driver_report.read_text(encoding="utf-8").lower() if nonempty(driver_report) else ""
    checks.append(("Driver report contains association evidence", "eta-squared" in driver_text))

    correlation_report = REPORTS / "phase11_correlation_analysis.md"
    correlation_text = (
        correlation_report.read_text(encoding="utf-8").lower()
        if nonempty(correlation_report)
        else ""
    )
    checks.append(("Correlation report identifies redundancy", "redundan" in correlation_text))

    passed = sum(result for _, result in checks)
    total = len(checks)

    print("ServiceLens Phase 11 Completion Checker")
    print("=" * 43)
    for description, result in checks:
        print(f"{'PASS' if result else 'FAIL'}: {description}")

    print()
    print(f"Phase 11 Completion: {passed}/{total} checks passed")
    print(f"Phase 11 Completion Percentage: {(passed / total) * 100:.0f}%")

    failed = [description for description, result in checks if not result]
    if failed:
        print("Missing or incomplete items:")
        for description in failed:
            print(f"- {description}")
        print("Overall Readiness for Phase 12: NOT READY")
        return 1

    print("Missing items: None")
    print("Overall Readiness for Phase 12: READY")
    return 0


if __name__ == "__main__":
    sys.exit(main())
