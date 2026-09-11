"""Verify that the workshop's required Python environment is available."""

from __future__ import annotations

import importlib.metadata
import sys


MINIMUM_PYTHON = (3, 10)
REQUIRED_PACKAGES = ("pandas", "scikit-learn", "pytest")


def main() -> int:
    """Print installed dependency versions and return a verification status."""
    errors: list[str] = []

    if sys.version_info < MINIMUM_PYTHON:
        errors.append(
            f"Python {MINIMUM_PYTHON[0]}.{MINIMUM_PYTHON[1]} or newer is required; "
            f"found {sys.version.split()[0]}."
        )
    else:
        print(f"Python {sys.version.split()[0]}")

    for package in REQUIRED_PACKAGES:
        try:
            version = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            errors.append(f"Required package is not installed: {package}")
        else:
            print(f"{package} {version}")

    if errors:
        print("\nEnvironment verification failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        print(
            "\nInstall the requirements with:\n"
            "python -m pip install pandas scikit-learn pytest",
            file=sys.stderr,
        )
        return 1

    print("\nEnvironment verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
