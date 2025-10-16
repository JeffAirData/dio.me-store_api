# Local development commands
run:
	@echo "Starting application locally..."
	@poetry run uvicorn store.main:app --reload --host 127.0.0.1 --port 8000

precommit-install:
	@poetry run pre-commit install

test:
	@poetry run pytest

run-local:
	@echo "Starting application with local environment..."
	@cp .env.local .env.temp && \
	poetry run uvicorn store.main:app --reload --host 127.0.0.1 --port 8000 && \
	rm .env.temp

# Docker commands
run-docker:
	@echo "Starting application with Docker Compose..."
	@docker compose up --build

run-docker-detached:
	@echo "Starting application with Docker Compose in background..."
	@docker compose up --build -d

stop-docker:
	@echo "Stopping Docker services..."
	@docker compose down

clean-docker:
	@echo "Cleaning Docker resources..."
	@docker compose down -v --remove-orphans
	@docker system prune -f

# Database commands
db-only:
	@echo "Starting only MongoDB..."
	@docker compose up db -d

# Test commands
test:
	@poetry run pytest

test-verbose:
	@poetry run pytest -v

test-matching:
	@poetry run pytest -s -rx -k $(K) --pdb store ./tests/

test-docker:
	@echo "Running tests in Docker..."
	@docker compose run --rm app poetry run pytest

# Setup commands
setup:
	@echo "Setting up project..."
	@poetry install
	@poetry run pre-commit install
	@cp .env.example .env
	@echo "Setup complete! Remember to configure your .env file."

precommit-install:
	@poetry run pre-commit install

# Health check
health:
	@echo "Checking application health..."
	@curl -f http://localhost:8000/health || echo "Application is not running"
