.PHONY: help install install-dev test test-cov lint format type-check clean build upload upload-test docs

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install the package
	pip install -e .

install-dev:  ## Install development dependencies
	pip install -r requirements-dev.txt
	pip install -e .
	pre-commit install

test:  ## Run tests
	pytest tests/

test-cov:  ## Run tests with coverage
	pytest tests/ --cov=py_dmm --cov-report=html --cov-report=term

lint:  ## Run linting
	pylint py_dmm

format:  ## Format code
	black py_dmm tests examples
	isort py_dmm tests examples

format-check:  ## Check code formatting
	black --check py_dmm tests examples
	isort --check-only py_dmm tests examples

type-check:  ## Run type checking
	mypy py_dmm

quality:  ## Run all quality checks
	$(MAKE) format-check
	$(MAKE) type-check
	$(MAKE) lint
	$(MAKE) test

clean:  ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build:  ## Build the package
	python -m build

upload-test:  ## Upload to Test PyPI
	twine upload --repository testpypi dist/*

upload:  ## Upload to PyPI
	twine upload dist/*

docs:  ## Generate documentation
	@echo "Documentation generation not implemented yet"

dev-setup:  ## Set up development environment
	python -m venv venv
	@echo "Activate the virtual environment with:"
	@echo "  source venv/bin/activate  # On Linux/macOS"
	@echo "  venv\\Scripts\\activate     # On Windows"
	@echo "Then run: make install-dev"