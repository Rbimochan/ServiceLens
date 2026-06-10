"""Check whether ServiceLens Phase 16 dashboard package is complete."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
FIGURES = REPORTS / "figures"
TABLEAU_SOURCE = ROOT / "data" / "processed" / "servicelens_tableau_source.csv"

REQUIRED_REPORTS = [
    "phase16_dashboard_planning.md",
    "phase16_tableau_data_source.md",
    "phase16_executive_dashboard.md",
    "phase16_csat_dashboard.md",
    "phase16_operational_dashboard.md",
    "phase16_cluster_dashboard.md",
    "phase16_predictive_dashboard.md",
    "phase16_tableau_story.md",
    "phase16_dashboard_recommendations.md",
    "phase16_tableau_dashboard_report.md",
]

REQUIRED_SCREENSHOTS = [
    "executive_dashboard.png",
    "csat_dashboard.png",
    "operational_dashboard.png",
    "cluster_dashboard.png",
    "predictive_dashboard.png",
]


def nonempty(path: Path) -> bool:
    return path.is_file() and path.stat().st_size > 0


def main() -> int:
    checks: list[tuple[str, bool]] = []

    for filename in REQUIRED_REPORTS:
        checks.append((f"Report exists and is non-empty: {filename}", nonempty(REPORTS / filename)))

    for filename in REQUIRED_SCREENSHOTS:
        checks.append((f"Dashboard preview exists and is non-empty: {filename}", nonempty(FIGURES / filename)))

    checks.append(("Tableau-ready data source exists", nonempty(TABLEAU_SOURCE)))

    recommendations = REPORTS / "phase16_dashboard_recommendations.md"
    recommendations_text = recommendations.read_text(encoding="utf-8").lower() if nonempty(recommendations) else ""
    checks.append(("Recommendations are documented", "response delay" in recommendations_text and "email" in recommendations_text))

    final_report = REPORTS / "phase16_tableau_dashboard_report.md"
    final_text = final_report.read_text(encoding="utf-8").lower() if nonempty(final_report) else ""
    dashboard_terms = [
        "executive overview",
        "csat performance",
        "operational performance",
        "interaction profiles",
        "predictive analytics",
    ]
    checks.append(("Final report references all dashboards", all(term in final_text for term in dashboard_terms)))
    checks.append(("Tableau implementation status is explicit", "native tableau workbook was not generated" in final_text))

    passed = sum(result for _, result in checks)
    total = len(checks)

    print("ServiceLens Phase 16 Completion Checker")
    print("=" * 43)
    for description, result in checks:
        print(f"{'PASS' if result else 'FAIL'}: {description}")

    print()
    print(f"Phase 16 Completion: {passed}/{total} checks passed")
    print(f"Phase 16 Completion Percentage: {(passed / total) * 100:.0f}%")

    failed = [description for description, result in checks if not result]
    if failed:
        print("Missing or incomplete items:")
        for description in failed:
            print(f"- {description}")
        print("Overall Readiness for Phase 17: NOT READY")
        return 1

    print("Missing items: None")
    print("Dashboard package readiness for Tableau authoring: READY")
    print("Overall Readiness for Phase 17: READY WITH TABLEAU WORKBOOK AUTHORING NOTE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
