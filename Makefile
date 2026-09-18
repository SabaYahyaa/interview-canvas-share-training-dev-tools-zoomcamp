test:
	poetry run pytest

run-backend:
	cd backend && poetry run uvicorn app.main:app --host 0.0.0.0 --port 8091

poetry-test-backend:
	cd backend && poetry run pytest tests/ -v

run-frontend:
	cd frontend && npm run dev

POETRY := /mnt/c/Windows/poetry.exe

run-e2e:
	@echo "==> Starting Docker stack for DB and backend services..."
	docker compose up -d --build
	@echo "==> Waiting for interviewer-canvas-container to become healthy..."
	@until [ $$(docker inspect -f '{{.State.Health.Status}}' interviewer-canvas-container 2>/dev/null || echo "unhealthy") = "healthy" ]; do \
		sleep 2; \
	done
	@echo "==> Running backend unit tests..."
	cd backend && $(POETRY) run pytest || (STATUS=$$?; docker compose down -v; exit $$STATUS)
	@echo "==> Running Playwright E2E tests via Poetry..."
	@cd test-e2e && $(POETRY) run pytest || (STATUS=$$?; docker compose down -v; exit $$STATUS)
	@echo "==> Cleaning up Docker containers..."
	docker compose down -v