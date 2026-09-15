test:
	poetry run pytest

run-backend:
	cd backend && poetry run uvicorn app.main:app --host 0.0.0.0 --port 8091

poetry-test:
	cd backend && poetry run pytest tests/ -v

run-frontend:
	cd frontend && npm run dev