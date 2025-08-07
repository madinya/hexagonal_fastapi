# FastAPI Hexagonal Architecture Starter

## Features
- Clean architecture separation
- Docker support (development & production)
- Complete testing setup (unit, integration, e2e)
- Pre-commit hooks for code quality
- Makefile for easy commands
- 90%+ test coverage enforcement

## Installation
1. Clone repository:
   `git clone https://github.com/your-repo/fastapi-hexagonal.git`
   `cd fastapi-hexagonal`
2. Install dependencies:
   `make install`

## Running the Application
Local development:
`make run` (http://localhost:8000)

With Docker:
`make build && make up`

## Testing
- All tests: `make test`
- Unit tests: `make unit-tests`
- Integration tests: `make integration-tests`
- E2E tests: `make e2e-tests`

## Code Quality
- Lint: `make lint`
- Format: `make format`
- Clean: `make clean`

## Project Structure
fastapi-hexagonal/
├── src/
├── tests/
├── Dockerfile
├── docker-compose.yml
├── Makefile
└── pyproject.toml