.PHONY: install test lint format run build up down clean

install:
	poetry install
	poetry run pre-commit install

test:
	poetry run pytest --cov=src --cov-report=term-missing

unit-tests:
	poetry run pytest tests/unit -v

integration-tests:
	poetry run pytest tests/integration -v

e2e-tests:
	poetry run pytest tests/e2e -v

lint:
	poetry run flake8 src
	poetry run mypy src

format:
	poetry run black src tests
	poetry run isort src tests

run:
	poetry run uvicorn src.main:app --reload

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	rm -rf .coverage .pytest_cache

check-precommit: lint unit-tests integration-tests
