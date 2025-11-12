.PHONY: help install test test-verbose test-coverage clean lint format

help:
	@echo "Leafmap MCP Server - Development Commands"
	@echo ""
	@echo "Available commands:"
	@echo "  make install         Install package and dependencies"
	@echo "  make install-dev     Install with development dependencies"
	@echo "  make test            Run tests"
	@echo "  make test-verbose    Run tests with verbose output"
	@echo "  make test-coverage   Run tests with coverage report"
	@echo "  make lint            Run linting checks"
	@echo "  make format          Format code with black"
	@echo "  make clean           Clean up generated files"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"
	pip install -r requirements-test.txt

test:
	pytest

test-verbose:
	pytest -vv

test-coverage:
	pytest --cov=server --cov-report=term-missing --cov-report=html

lint:
	flake8 server.py test_server.py --max-line-length=100
	mypy server.py --ignore-missing-imports

format:
	black server.py test_server.py --line-length=100

clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf *.pyc
	rm -rf .mypy_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
