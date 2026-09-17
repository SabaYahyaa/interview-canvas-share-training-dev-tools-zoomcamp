# Stage 1: Build Frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Build Backend & Serve
FROM python:3.10-slim
WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy Poetry config files from backend directory
COPY backend/pyproject.toml backend/poetry.lock* ./

# Disable virtualenv creation inside container & install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Copy compiled frontend static assets from Stage 1 into /app/static
COPY --from=frontend-builder /app/frontend/dist ./static

# Copy backend application code
COPY backend/ ./

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# build a docker container without docker compose file
# docker build -t interviewer-canvas-app .
# docker run -p 8000:8000 --name interviewer-canvas-container interviewer-canvas-app