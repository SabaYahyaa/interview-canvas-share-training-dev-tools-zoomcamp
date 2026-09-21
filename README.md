# System Design Interview Platform

A browser-based collaborative workspace for conducting live system-design interviews. An interviewer creates a session and shares a link; candidates and other interviewers join and work together on the same infinite canvas in real time — placing architecture components, connecting them with arrows, adding labels and notes, and drawing freehand. Edits are broadcast over WebSockets so every participant sees updates immediately, and the final canvas is preserved for later review.

---

## Acknowledgments & Context

* **Frontend & OpenAPI Spec:** The frontend application and the `openapi.yaml` specification in this repository are based on [Alexey Grigorev's interview-canvas-share repository](https://github.com/alexeygrigorev/interview-canvas-share/tree/main/frontend). The frontend UI was initially generated using Lovable and adopted here to avoid token consumption costs during generation. Special thanks to Alexey Grigorev for sharing the base UI and API contract.
* **Course & AI Assistance:** Built as part of hands-on practice to reinforce and review training course material. Development was assisted using **Gemini** and **ChatGPT** for complex generation tasks. **Cline with Ollama** was utilized for project planning and managing smaller sub-tasks, with every generated change carefully reviewed and validated manually.

---

## Development Strategy & Agentic AI Workflow

This project serves as a step-by-step blueprint for rapidly prototyping and building production-ready applications using AI agents:

1. **Frontend Setup:** Generated the initial frontend using Lovable and established the OpenAPI specification contract (`openapi.yaml`).
2. **Frontend Mock Verification:** Validated the frontend UI against a mock backend server to ensure contract compliance before writing backend logic.
3. **Iterative Backend Development:**
   - **Phase 1 (In-Memory):** Built the core FastAPI routes and WebSocket server using in-memory state for rapid prototyping.
   - **Phase 2 (SQLite & SQLAlchemy):** Integrated SQLAlchemy for persistent storage using SQLite.
   - **Phase 3 (PostgreSQL Migration):** Upgraded database layer to production-ready PostgreSQL.
4. **Containerization & Orchestration:**
   - Created a multi-stage `Dockerfile` to serve the compiled frontend bundle via FastAPI.
   - Configured `docker-compose.yaml` to orchestrate PostgreSQL and application health checks.
5. **E2E Testing Automation:** Implemented automated Playwright test suites to continuously verify UI-to-backend integration.
6. **Deployment Target:** Designed with cloud container deployment in mind (targeted for deployment on Render).

---

## Local Setup & Quick Start

Follow these simple steps to get the application up and running locally.

### Prerequisites

* **Operating System:** Ubuntu / Linux (or WSL2 on Windows).
* **Docker & Docker Compose:** Installed and running.
* **Node.js & npm:** (Optional, only needed if modifying the frontend directly).
* **Python 3.12 & Poetry:** (Optional, only needed if developing backend code outside Docker).

---

### Steps for setting up the project locally:

```sh
# Step 1: Clone the Repository
git clone [https://github.com/your-username/interviewer-canvas-app.git](https://github.com/your-username/interviewer-canvas-app.git)
cd interviewer-canvas-app

# Step 2: Run the App with Docker Compose
# Builds and launches the PostgreSQL database and unified application container:
docker compose up --build

# Step 3: Access Endpoints
# Frontend Web App: http://localhost:8000
# Backend API Docs (Swagger): http://localhost:8000/docs


```

### Steps for automated end-2-end testing the project locally:
```sh
# Step 1: Stop any currently running Docker containers
docker compose down -v

# Step 2: Run the automated E2E tests via Makefile (spins up the stack and executes Playwright tests)
make e2e
```