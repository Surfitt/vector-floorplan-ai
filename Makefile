.PHONY: install install-dev lint format test test-cov pre-commit clean

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"
	pre-commit install

lint:
	ruff check src tests
	ruff format --check src tests

format:
	ruff check --fix src tests
	ruff format src tests

test:
	pytest

test-cov:
	pytest --cov=vector_floorplan_ai --cov-report=term-missing

pre-commit:
	pre-commit run --all-files

clean:
	rm -rf build dist .pytest_cache .ruff_cache .coverage htmlcov
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
