test:
	poetry run pytest

run:
	cd backend && poetry run uvicorn main:app --host 0.0.0.0 --port 8091