cat > Dockerfile <<'EOL'
# Development
FROM python:3.9-slim as development

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

COPY . .

CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Production
FROM python:3.9-slim as production

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --only main

COPY . .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOL

cat > docker-compose.yml <<'EOL'
version: '3.8'

services:
  app:
    build:
      context: .
      target: development
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    environment:
      - PYTHONUNBUFFERED=1
      - PYTHONPATH=/app

  tests:
    build:
      context: .
      target: development
    command: ["pytest", "--cov=src", "--cov-report=term-missing"]
    volumes:
      - .:/app
    environment:
      - PYTHONUNBUFFERED=1
      - PYTHONPATH=/app
    depends_on:
      - app
EOL

# 2. Create Makefile
cat > Makefile <<'EOL'
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
EOL

# 3. Generate .gitignore
cat > .gitignore <<'EOL'
# Python
__pycache__/
*.py[cod]
*$py.class
.python-version
.env
.venv
venv/
ENV/

# Testing
.coverage
htmlcov/
.pytest_cache/
.mypy_cache/

# Docker
docker-compose.override.yml

# IDE
.vscode/
.idea/

# Logs
*.log
logs/

# System
.DS_Store
EOL

# 4. Set up pre-commit hooks
cat > .pre-commit-config.yaml <<'EOL'
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 23.7.0
    hooks:
      - id: black
        language_version: python3.9

  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
        additional_dependencies: [flake8-bugbear==23.7.10]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.5.1
    hooks:
      - id: mypy
        additional_dependencies: [pydantic==1.10.7]

  - repo: local
    hooks:
      - id: run-tests
        name: Run Unit & Integration Tests
        entry: make check-precommit
        language: system
        types: [python]
        pass_filenames: false
        always_run: true
EOL

# 5. Create README.md with complete instructions
cat > README.md <<'EOL'
# FastAPI Hexagonal Architecture Project

## Development Setup

### Local Development
```bash
make install  # Install dependencies
make run      # Start development server
Docker Development
bash
make build    # Build containers
make up       # Start services
make down     # Stop services
Testing
bash
make test             # Run all tests
make unit-tests       # Run unit tests
make integration-tests # Run integration tests
make e2e-tests        # Run end-to-end tests
Code Quality
bash
make lint    # Run linters
make format  # Auto-format code
make clean   # Remove temporary files
Pre-commit Hooks
Hooks run automatically before each commit:

Code formatting

Linting

Type checking

Unit & Integration tests

Deployment
bash
docker build --target production -t app .
docker run -p 8000:8000 app
Project Structure
text
.
├── src/                # Application code
├── tests/              # Test suites
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Service orchestration
├── Makefile            # Project automation
└── README.md           # Documentation
EOL
