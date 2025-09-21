# Makefile for YouTube Channel Scripts

.PHONY: help install install-dev test lint format type-check clean setup example

# Default target
help:
	@echo "Available commands:"
	@echo "  setup        - Set up the development environment"
	@echo "  install      - Install production dependencies"
	@echo "  install-dev  - Install development dependencies"
	@echo "  test         - Run tests"
	@echo "  lint         - Run linting (flake8)"
	@echo "  format       - Format code (black)"
	@echo "  type-check   - Run type checking (mypy)"
	@echo "  example      - Run example script"
	@echo "  clean        - Clean up temporary files"

# Set up development environment
setup:
	@echo "Setting up development environment..."
	python3 -m venv venv || python -m venv venv
	@echo "Activate virtual environment with: source venv/bin/activate"
	@echo "Then run: make install-dev"

# Install production dependencies
install:
	pip install -r requirements.txt

# Install development dependencies
install-dev:
	pip install -e ".[dev]"
	pip install -r requirements.txt

# Run tests
test:
	pytest tests/ -v

# Run tests with coverage
test-coverage:
	pytest --cov=scripts --cov=utils tests/ --cov-report=html

# Run linting
lint:
	flake8 scripts/ utils/ tests/ examples/

# Format code
format:
	black scripts/ utils/ tests/ examples/

# Run type checking
type-check:
	mypy scripts/ utils/

# Run all quality checks
check-all: lint type-check test

# Run example script
example:
	python examples/example_script.py --name "YouTube Creator" --verbose

# Clean up temporary files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache/ .coverage htmlcov/ .mypy_cache/ build/ dist/