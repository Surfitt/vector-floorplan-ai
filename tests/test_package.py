"""Smoke tests — keep unit tests concise and focused."""

import vector_floorplan_ai


def test_package_imports() -> None:
    assert vector_floorplan_ai.__version__ == "0.1.0"


def test_version_format() -> None:
    parts = vector_floorplan_ai.__version__.split(".")
    assert len(parts) == 3
    assert all(part.isdigit() for part in parts)
