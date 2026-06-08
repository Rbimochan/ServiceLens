#!/usr/bin/env python3
"""Check ServiceLens Phase 1 and Phase 2 completion readiness.

This script performs setup and acquisition checks only. It does not load,
parse, or analyze the raw dataset.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = PROJECT_ROOT / "data" / "raw" / "customer_support_tickets.csv"
PHASE_3_NOTEBOOK = PROJECT_ROOT / "notebooks" / "03_dataset_loading.ipynb"

REQUIRED_PACKAGES = {
    "pandas",
    "numpy",
    "matplotlib",
    "seaborn",
    "scikit-learn",
    "pyspark",
    "jupyter",
    "ipykernel",
    "pyarrow",
    "openpyxl",
}


def pass_fail(condition: bool, message: str) -> bool:
    status = "PASS" if condition else "FAIL"
    print(f"{status} {message}")
    return condition


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def package_names_from_requirements(path: Path) -> set[str]:
    names: set[str] = set()
    for raw_line in read_text(path).splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        for separator in ("==", ">=", "<=", "~=", "!=", ">", "<"):
            if separator in line:
                line = line.split(separator, 1)[0].strip()
                break
        if line:
            names.add(line.lower())
    return names


def is_git_ignored(path: Path) -> bool:
    try:
        result = subprocess.run(
            ["git", "check-ignore", "-q", str(path.relative_to(PROJECT_ROOT))],
            cwd=PROJECT_ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    except (OSError, ValueError):
        return False
    return result.returncode == 0


def notebook_text(path: Path) -> str:
    try:
        notebook = json.loads(read_text(path))
    except json.JSONDecodeError:
        return ""

    parts: list[str] = []
    for cell in notebook.get("cells", []):
        source = cell.get("source", [])
        if isinstance(source, list):
            parts.append("".join(source))
        elif isinstance(source, str):
            parts.append(source)
    return "\n".join(parts)


def notebook_has_analysis_results(path: Path) -> bool:
    """Detect executed notebook outputs without inspecting dataset contents."""
    try:
        notebook = json.loads(read_text(path))
    except json.JSONDecodeError:
        return True

    for cell in notebook.get("cells", []):
        if cell.get("cell_type") == "code":
            if cell.get("execution_count") is not None:
                return True
            if cell.get("outputs"):
                return True
    return False


def run_phase_1_checks() -> tuple[int, int, list[str]]:
    print("\nPHASE 1 — Environment & Project Setup")

    requirements_path = PROJECT_ROOT / "requirements.txt"
    listed_packages = package_names_from_requirements(requirements_path)
    missing_packages = sorted(REQUIRED_PACKAGES - listed_packages)

    checks = [
        (PROJECT_ROOT / ".git").is_dir(),
        (PROJECT_ROOT / "README.md").is_file(),
        requirements_path.is_file(),
        (PROJECT_ROOT / ".gitignore").is_file(),
        (PROJECT_ROOT / "verify_setup.py").is_file(),
        (PROJECT_ROOT / "src" / "__init__.py").is_file(),
        (PROJECT_ROOT / "notebooks").is_dir(),
        (PROJECT_ROOT / "notebooks" / "01_data_understanding.ipynb").is_file(),
        (PROJECT_ROOT / "data" / "raw").is_dir(),
        (PROJECT_ROOT / "data" / "processed").is_dir(),
        (PROJECT_ROOT / "reports").is_dir(),
        not missing_packages,
    ]

    messages = [
        "Git repository exists",
        "README.md exists",
        "requirements.txt exists",
        ".gitignore exists",
        "verify_setup.py exists",
        "src/__init__.py exists",
        "notebooks folder exists",
        "notebooks/01_data_understanding.ipynb exists",
        "data/raw folder exists",
        "data/processed folder exists",
        "reports folder exists",
        "required packages are listed in requirements.txt",
    ]

    missing_items: list[str] = []
    for condition, message in zip(checks, messages):
        if not pass_fail(condition, message):
            if message == "required packages are listed in requirements.txt":
                missing_items.append(
                    f"{message}: missing {', '.join(missing_packages)}"
                )
            else:
                missing_items.append(message)

    passed = sum(checks)
    total = len(checks)
    print(f"\nPhase 1 Completion: {passed}/{total} checks passed")
    print(f"Phase 1 Completion Percentage: {passed / total:.0%}")
    return passed, total, missing_items


def run_phase_2_checks() -> tuple[int, int, list[str]]:
    print("\nPHASE 2 — Dataset Acquisition")

    readme_text = read_text(PROJECT_ROOT / "README.md").lower()
    phase_3_text = notebook_text(PHASE_3_NOTEBOOK).lower()
    file_size_bytes = DATASET_PATH.stat().st_size if DATASET_PATH.is_file() else 0

    checks = [
        DATASET_PATH.is_file(),
        file_size_bytes > 0,
        DATASET_PATH.suffix.lower() == ".csv",
        (PROJECT_ROOT / "data" / "raw" / ".gitkeep").is_file(),
        (PROJECT_ROOT / "data" / "processed" / ".gitkeep").is_file(),
        is_git_ignored(DATASET_PATH),
        ("dataset" in readme_text or "source" in readme_text or "data/raw" in readme_text),
        PHASE_3_NOTEBOOK.is_file(),
        "data/raw/customer_support_tickets.csv" in phase_3_text,
        PHASE_3_NOTEBOOK.is_file() and not notebook_has_analysis_results(PHASE_3_NOTEBOOK),
    ]

    messages = [
        "dataset exists in data/raw",
        "file size greater than 0 bytes",
        "file extension is .csv",
        "data/raw/.gitkeep exists",
        "data/processed/.gitkeep exists",
        "raw CSV is ignored by Git",
        "README mentions dataset/source or data/raw",
        "Phase 3 notebook exists",
        "Phase 3 notebook documents dataset location",
        "Phase 3 notebook does not contain analysis results",
    ]

    missing_items: list[str] = []
    for condition, message in zip(checks, messages):
        if not pass_fail(condition, message):
            missing_items.append(message)

    passed = sum(checks)
    total = len(checks)
    print(f"\nPhase 2 Completion: {passed}/{total} checks passed")
    print(f"Phase 2 Completion Percentage: {passed / total:.0%}")
    return passed, total, missing_items


def main() -> int:
    print("ServiceLens Phase 1 & Phase 2 Completion Check")

    phase_1_passed, phase_1_total, phase_1_missing = run_phase_1_checks()
    phase_2_passed, phase_2_total, phase_2_missing = run_phase_2_checks()

    missing_items = phase_1_missing + phase_2_missing
    ready = phase_1_passed == phase_1_total and phase_2_passed == phase_2_total

    print("\nMissing Items")
    if missing_items:
        for item in missing_items:
            print(f"- {item}")
    else:
        print("- None")

    print("\nOverall Status:")
    if ready:
        print("READY — Phase 1 and Phase 2 required checks are complete.")
        return 0

    print("NOT READY — fix missing items before Phase 3.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
