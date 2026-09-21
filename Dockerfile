######################################################
#   Application Build Instructions
######################################################
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
# Note to Run Dockerfile without docker compose:
#1. docker compose down -v --remove-orphans
#2. docker compose up -d db
#3. docker build -t interviewer-canvas-app .
#4. docker run -d --name interviewer-canvas-container --add-host=host.docker.internal:host-gateway -p 8000:8000 -e DATABASE_URL=postgresql://postgres:postgres@host.docker.internal:5432/interviewer_db -e INTERVIEWER_USER_ID=user-123 -e INTERVIEWER_EMAIL=host@example.com -e INTERVIEWER_DISPLAY_NAME=Interviewer interviewer-canvas-app