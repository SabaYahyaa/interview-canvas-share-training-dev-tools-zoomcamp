# 🎨 System Design Interview Platform 🚀

A browser-based collaborative workspace for conducting live system-design interviews. An interviewer creates a session and shares a link; candidates and other interviewers join and work together on the same infinite canvas in real time — placing architecture components, connecting them with arrows, adding labels and notes, and drawing freehand. Edits are broadcast over WebSockets so every participant sees updates immediately, and the final canvas is preserved for later review.


## 🌐 Live Application & Production Endpoints

The application is deployed across multi-environment web services hosted on **Render** using container images published to **GitHub Container Registry (GHCR)**:

* 🖥️ **Production Web App:** [https://interview-canvas-prod.onrender.com](https://interview-canvas-prod.onrender.com)
* 📚 **Production API / Swagger Docs:** [https://interview-canvas-prod.onrender.com/docs](https://interview-canvas-prod.onrender.com/docs)
* 🧪 **Dev Web App:** [https://interview-canvas-dev.onrender.com](https://interview-canvas-dev.onrender.com)
* 📚 **Dev API / Swagger Docs:** [https://interview-canvas-dev.onrender.com/docs](https://interview-canvas-dev.onrender.com/docs)

> **Note:** Running on free Render instances, the services may sleep after periods of inactivity. Initial cold-start requests may take ~30–50 seconds to wake up an instance.



## 💡 Acknowledgments & Context

* 🎓 **Training Context:** Built as part of hands-on practice following the **DataTalksClub LLMs & AI Engineering Zoomcamp** methodology.
* 🎨 **Frontend Base & OpenAPI Contract:** Adapted from [Alexey Grigorev's interview-canvas-share repository](https://github.com/alexeygrigorev/interview-canvas-share/tree/main/frontend). The frontend UI was initially generated using Lovable and adopted here to avoid token consumption costs during generation. Special thanks to Alexey Grigorev for sharing the base UI and API contract.
* 🤖 **AI-Assisted Development:** Developed using **Gemini** and **ChatGPT** for backend logic, unit test creation, and CI/CD workflow automation, with local task management executed via **Cline with Ollama**. Every generated component was manually reviewed, integrated, and verified against quality gates.

---

## 🚀 AI-Driven App Blueprint: From Fast Prototype to Production CI/CD

This repository serves as a repeatable, step-by-step framework for rapidly prototyping, containerizing, testing, and deploying production-ready web applications using AI tools and automated pipelines.



### 1. 🎨 Frontend Setup & Mock Backend Prototyping (Module 1)

Following the **Module 1 training workflow** on AI-assisted application prototyping, this initial phase focuses on establishing a functional user interface using prompt-to-code tools before writing any server-side logic. Decoupling the frontend allows for immediate visual validation and rapid UI/UX iteration.
#### What We Did:
1. **Frontend UI Generation (Lovable / Bolt.new):**
   - Generated the full React/TypeScript user interface using **Lovable** (equivalent prompt-to-app tools like **Bolt.new** or **v0** follow the identical workflow).
   - Exported the generated source code into the repository workspace as a clean, stand-alone frontend.

2. **In-Memory Mock Backend Integration:**
   - Configured frontend components to use local mock state and static fallback objects instead of live database calls.
   - Enabled immediate visual verification of core UI interactions—placing canvas shapes, moving arrows, adding notes—without waiting for server implementation.

#### Repeatable Blueprint Checklist for Future Projects:
- [ ] Prompt an AI generator (**Lovable**, **Bolt.new**) to output the base UI layout and client interaction handlers.
- [ ] Export and push the generated code directly into a version-controlled Git repository.
- [ ] Confirm client components interact with in-memory mock data for fast visual verification.
- [ ] Open PowerShell / Terminal to verify the frontend builds cleanly before starting backend work:
  ```powershell
  cd frontend
  npm install
  npm run build
  ```

### 2. ⚙️ Building the Backend & Connecting the App (Module 2)

In **Module 2**, we took the static frontend and built a real backend for it step-by-step. Instead of jumping straight into a complex database setup, we replaced the fake data in three simple stages:

#### What We Did:
1. **FastAPI Server with In-Memory State:**
   - Built a Python backend using **FastAPI** to handle live HTTP requests (REST endpoints) and WebSockets for real-time canvas sync.
   - Decoded mock handlers with live HTTP/WebSocket client requests connected to the FastAPI server using in-memory state.
   - Stored data temporarily in Python memory (lists and dicts) while testing connection flows.

2. **Added SQLite with SQLAlchemy:**
   - Set up **SQLAlchemy** models to structure our data (canvas sessions, shapes, and lines).
   - Replaced in-memory lists and dicts with a lightweight **SQLite** file database (`interview.db`) so data saves even when restarting the server.

3. **Switched to PostgreSQL:**
   - Upgraded from SQLite to **PostgreSQL** for a real, production-ready database setup.
   - Added connection pooling and a `/health` route to make sure the database connects reliably.

4. **Testing & Makefile Automation:**
   - Wrote automated unit and integration tests for all backend routes using `pytest`.
   - Created a `Makefile` to simplify starting the server and running test suites with single-line commands.

#### Checklist for Next Time:
- [ ] Create a FastAPI backend to handle both HTTP requests and WebSocket connections.
- [ ] Decode mock handlers with live HTTP/WebSocket client requests connected to the FastAPI server using in-memory state.
- [ ] Store data temporarily in Python memory (lists and dicts) while testing connection flows.
- [ ] Add SQLAlchemy models and save data locally using a SQLite `interview.db` file.
- [ ] Update the `DATABASE_URL` string to connect to PostgreSQL when ready for a production database.
- [ ] Test the backend server and unit tests locally in PowerShell:
  ```powershell
  # Run backend locally
  cd backend
  poetry run uvicorn app.main:app --host 0.0.0.0 --port 8091

  # Run backend unit tests
  cd backend
  poetry run pytest tests/ -v

- [ ] Run automated tests or local servers using make commands in PowerShell:
      . make poetry-test-backend — runs the backend unit and integration test suite via pytest.

      . make run-backend — launches the FastAPI uvicorn server locally on port 8091.

      . make run-frontend — starts the frontend Vite development server.

      . make test — executes default project tests.


### 3. 🐳 Containerization, Orchestration & Automated Testing (Module 3)

In **Module 3**, we used Ubuntu on Windows WSL to package the entire application into Docker containers. This ensures the app, database, and static frontend run identically in local development and production.

#### What We Did:
1. **Multi-Stage Dockerfile:** 
   - Authored a multi-stage `Dockerfile`: Stage 1 sets up the frontend build directory, copies `frontend/package.json` and `frontend/package-lock.json ./`, installs dependencies with `npm install`, and builds the frontend. Stage 2 sets up Python/Poetry, copies the compiled static assets into `/app/static`, and serves everything through FastAPI and Uvicorn on port `8000`.

2. **Docker Compose & PostgreSQL Setup:**
   - Configured `docker-compose.yml` to orchestrate a `db` service running `postgres:15-alpine` alongside the `web` application container over a shared bridge network (`interviewer-net`).
   - Added health checks (`pg_isready`) so the FastAPI container waits until PostgreSQL is ready before starting.

3. **Automated End-to-End (E2E) Testing with Containerized Playwright:**
   - Created automated E2E integration tests (using Playwright) simulating real user interactions: opening the app, creating a session, generating a share link, joining as a candidate, and verifying live canvas synchronization between participants.
   - Ran Playwright tests inside an isolated, temporary Docker container using a `Makefile` script so tests execute cleanly without needing a local virtual environment or manual browser setup on Ubuntu/WSL or PowerShell.

4. **CI/CD Integration & Render Deployment:**
   - Pushed code to GitHub with workflow files (`.github/workflows/deploy.yml` and `render.yaml`).
   - Configured the workflow to run code quality checks and tests automatically on push, then trigger manually a deployment on Render to build and run the Docker container.

#### Checklist for Next Time:
- [ ] Create a multi-stage `Dockerfile` to install frontend dependencies (`COPY frontend/package.json frontend/package-lock.json ./`), build the frontend, and serve it via FastAPI.
- [ ] Build and test the container stack locally either via Docker Compose or manually:
  ```powershell
  # Option A: Quick build and run using Docker Compose (Recommended)
  docker compose build
  docker compose up -d

  # Option B: Manual container build against a standalone DB container
  # 1. Clean up old containers
  docker compose down -v --remove-orphans

  # 2. Start PostgreSQL container only
  docker compose up -d db

  # 3. Build and run the web app container attached to host network
  docker build -t interviewer-canvas-app .
  docker run -d --name interviewer-canvas-container `
    --add-host=host.docker.internal:host-gateway `
    -p 8000:8000 `
    -e DATABASE_URL=postgresql://postgres:postgres@host.docker.internal:5432/interviewer_db `
    interviewer-canvas-app
  ```    
- [ ] Inspect container logs or run unit tests inside the active stack:
  ```powershell
   docker compose ps
   docker compose logs web
   docker compose exec web pytest -v
    ```
- [ ] Execute make run-e2e from PowerShell or Ubuntu (WSL) to test locally — it automatically spins up the stack, waits for container health, runs Playwright tests in a temporary container without needing a local virtual environment, and tears everything down cleanly.

- [ ] Add GitHub Actions workflows (deploy.yml) to automatically check code quality, run tests, and notify Render to deploy the updated image.




## 4. 🚀 Automated CI/CD, Container Registry & Multi-Environment Deployments (Module 4)

In **Module 4**, we replaced manual Render triggers with a fully automated CI/CD pipeline using GitHub Actions,
set up container image tagging, and configured dual development (interview-canvas-dev) and production (interview-canvas-prod) web services on Render with database schema isolation,
and integrated full-stack OpenTelemetry monitoring with Grafana Cloud (Prometheus, Loki, and Tempo).

### What We Did:
1. **Automated GitHub Actions Pipeline (3 Jobs):**
   - **Job 1 (Quality & Unit Tests):** Runs code quality checks and executes `pytest` for the backend.
   - **Job 2 (E2E Integration Tests):** Spins up the stack and runs the containerized Playwright E2E tests to verify canvas sync across sessions.
   - **Job 3 (Build & Push Image):** Builds the production Docker image and pushes it to GitHub Container Registry (´GHCR´) using a custom tag format (`YYYY-MM-DD-<SHA>` and `latest`).

2. **Render Web Services Setup (Dev vs. Prod):**
   - Removed the old manual service setup in Render and created two separate web services: `Dev` (interview-canvas-dev) and `Prod` (interview-canvas-prod).
   - **Dev Environment:** Automatically pulls the `latest` tagged image from `GHCR` on new code pushes.
   - **Prod Environment:** Serves production traffic and is triggered manually via GitHub Actions workflow dispatch (`promote-prod.yaml`).

3. **Single-Branch Strategy & Database Schema Isolation:**
   - Kept a single `main` branch to maintain one unified version of the codebase without branch-management overhead.
   - Utilized separate database schemas ( `dev` and `prod`) inside a single Render PostgreSQL database to isolate environments without extra cost.

4. **Full-Stack OpenTelemetry (OTEL) Setup in FastAPI** (`telemetry.py`):
   - Added OpenTelemetry SDK with HTTP exporters (`OTLPMetricExporter`, `OTLPSpanExporter`, `OTLPLogExporter`) to instrument FastAPI endpoints and log handlers.
   - Configured exported logs to attach active `trace_id` and `span_id` values to log records automatically using `LoggingHandler`.
   - Directed all telemetry via OTLP/HTTP to Grafana Cloud endpoints using environment variables:
      - `OTEL_EXPORTER_OTLP_ENDPOINT`
      - `OTEL_EXPORTER_OTLP_HEADERS`
      - `OTEL_SERVICE_NAME` (`interview-canvas-backend-dev` / `interview-canvas-backend-prod`)

5. **Grafana Cloud Dashboard Panels & Data Sources**F:
   - Prometheus (Metrics): Visualized request rates, HTTP status distribution (2xx, 4xx, 5xx), and request latency percentiles (`p50`, `p90`, `p99`).
   - Loki (Logs): Configured LogQL panels filtering by `{service_name="interview-canvas-backend-dev"}` to stream live stdout logs.
   - Tempo (Traces): Created TraceQL panels (`{ resource.service.name = "interview-canvas-backend-dev" }`) displaying request waterfall timelines and execution spans.

6. **Loki Derived Fields (Log-to-Trace Correlation)**:
   - **Configured Derived Fields** in the Loki data source settings to enable 1-click navigation from log lines to Tempo traces.
   - **Regex Pattern:** `trace_id=(\w+)`
   - **Internal Link:** Pointed directly to the Grafana Cloud Tempo trace data source (`grafanacloud-*-traces`) passing `${__value.raw}` as the Trace ID.

7. **Proactive Email Alerting:**
   - Configured evaluation rules in Grafana Alerting under the `fastapi-monitoring` group with a 1-minute evaluation interval and a 2-minute pending period (for: `2m`).
   - **5xx Error Rate Alert:** Triggers when 5xx server responses exceed threshold.
   - **High Latency Alert:** Triggers when request duration exceeds `1s`.
   - **Contact Point:** Integrated email notifications to deliver instant alert state transitions directly to the team inbox.

### Checklist for Next Time:
- [ ] Configure a GitHub Actions workflow (`.github/workflows/deploy.yaml`) structured into 3 distinct sequential jobs:
  1. Code quality (`black' and `flake8`) + unit testing (`pytest`).
  2. Automated E2E testing.
  3. Image build & push to GitHub Container Registry (GHCR).
- [ ] Set up image tagging in GitHub Actions using `YYYY-MM-DD-SHA` alongside the `latest` tag for version tracking.
- [ ] Configure two distinct web services on Render pointing to your GHCR image:
  - **Dev Service:** Configured for auto-deploy on new GHCR image pushes.
  - **Prod Service:** Configured for manual deplyment triggers only, manually run a `.github/workflows/promote-prod.yaml` GitHub Actions workflow.
- [ ] Set environment variables on Render to direct Dev and Prod services.
- [ ] Set up database schema isolation by appending ?options=-csearch_path=dev to the Dev database connection string.
- [ ] Keep a single main branch workflow: push changes to trigger automated tests and Dev deployments, then 
- [ ] Add telemetry.py to FastAPI using OpenTelemetry Python SDK and OTLP exporters.
- [ ] Configure Grafana Cloud OTLP endpoint and authentication headers via environment variables.
- [ ] Set up Loki Derived Fields on the Loki data source (Regex: trace_id=(\w+) $\rightarrow$ Tempo Data Source).
- [ ] Create Grafana dashboard panels for Prometheus metrics, Loki LogQL streams, and Tempo TraceQL waterfalls.
- [ ] Create alert rules in Grafana for 5xx errors and latency > 1s, attached to an email notification contact point.



---




## 🚀 Deployment & Environments Architecture

This project uses a multi-environment CI/CD pipeline hosted on **Render** and backed by **GitHub Container Registry (GHCR)** for immutable Docker image storage.

### Database Isolation Strategy

To fit within Render's single active free-tier database limit, both environments share one PostgreSQL instance (`interview-postgres`). Data isolation is handled using separate PostgreSQL schemas:

* **Production Environment:** Uses the `public` schema (`SDIP_DATABASE_URL`).
* **Dev Environment:** Uses the `dev` schema (`SDIP_DATABASE_URL` with `?options=-csearch_path=dev` appended).

All Dev queries, writes, and migrations run strictly inside the `dev` schema, keeping production data completely untouched.

---

### Environment Breakdown

| Environment | Web Service Name | Database Instance | Schema Isolation | Trigger Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Dev** | `interviewer-canvas-dev` | `interview-postgres` | `dev` (`?options=-csearch_path=dev`) | **Automated:** Pushes to `main` build `ghcr.io/<owner>/<repo>:<YYYY-MM-DD-SHA>` and deploy to Dev. |
| **Production** | `interview-canvas-app` | `interview-postgres` | `public` (default) | **Manual:** Triggered via `Promote Image to Production` workflow in GitHub Actions. |

---

### Deployment Pipeline Procedures

#### 1. Automated Dev Deployment (Git Push)

```mermaid
flowchart TD
    User([Developer / User]) -->|1. git push main| GHRepo[GitHub Repository]
    GHRepo -->|2. Triggers deploy.yml| GHRunner[GitHub Actions Runner]
    
    subgraph GHActionsDev [GitHub Actions: Dev Workflow]
        GHRunner -->|3. Build & Push Image| GHCR[(GitHub Container Registry)]
        GHRunner -->|4. Trigger RENDER_DEV_DEPLOY_HOOK| RenderDev[Render Service: interviewer-canvas-dev]
    end
    
    RenderDev -->|5. Pull new image| GHCR
    RenderDev -->|6. Start Container| DevContainer[Live Dev Instance]
    DevContainer -->|7. Connect via SDIP_DATABASE_URL| DB[(PostgreSQL: interview-postgres)]
    
    subgraph SchemaDev [Database Isolation]
        DB -->|?options=-csearch_path=dev| DevSchema[dev Schema]
    end
```
#### 2. Manual Production Promotion (Workflow Dispatch)
```mermaid
flowchart TD
    User([Developer / User]) -->|1. Select 'Promote Image to Production' & input tag| GHUI[GitHub Actions UI]
    GHUI -->|2. Triggers promote-prod.yml| GHRunnerProd[GitHub Actions Runner]
    
    subgraph GHActionsProd [GitHub Actions: Prod Promotion]
        GHRunnerProd -->|3. Trigger RENDER_DEPLOY_HOOK_URL| RenderProd[Render Service: interview-canvas-app]
    end
    
    RenderProd -->|4. Pull specified image tag| GHCR[(GitHub Container Registry)]
    RenderProd -->|5. Start Container| ProdContainer[Live Production Instance]
    ProdContainer -->|6. Connect via SDIP_DATABASE_URL| DB[(PostgreSQL: interview-postgres)]
    
    subgraph SchemaProd [Database Isolation]
        DB -->|Default Search Path| PublicSchema[public Schema]
    end
```






## 💻 Local Setup & Quick Start

Follow these simple steps to get the application up and running locally.

### 📋 Prerequisites

* **Operating System:** Ubuntu / Linux (or WSL2 on Windows).
* **Docker & Docker Compose:** Installed and running.
* **Node.js & npm:** (Optional, only needed if modifying the frontend directly).
* **Python 3.12 & Poetry:** (Optional, only needed if developing backend code outside Docker).

---

### 🚀 Running the Project Locally

```sh
# Step 1: Clone the Repository
git clone [https://github.com/SabaYahyaa/interview-canvas-share-training-dev-tools-zoomcamp.git](https://github.com/SabaYahyaa/interview-canvas-share-training-dev-tools-zoomcamp.git)
cd interview-canvas-share-training-dev-tools-zoomcamp

# Step 2: Choose One of the Two Ways to Run the App Locally:

# --- Way 1: One-Command Stack Execution (Recommended) ---
# Builds and launches the PostgreSQL database and application container together:
docker compose up --build

# --- Way 2: Granular Database & Web Container Execution ---
# Alternatively, start the database first and build/run the application container manually:
# 1. Start the PostgreSQL database service in detached mode:
docker compose up -d db

# 2. Build the web application Docker image:
docker build -t interviewer-canvas-app .

# 3. Run the web container attached to the Docker Compose network:
docker run -p 8000:8000 \
  --network interview-canvas-share-training-dev-tools-zoomcamp_default \
  -e DATABASE_URL="postgresql://postgres:postgres@db:5432/interviewer_db" \
  interviewer-canvas-app


# Step 3: Access Endpoints
# Frontend Web App: http://localhost:8000
# Backend API Docs (Swagger): http://localhost:8000/docs


```

### 🧪 Steps for Automated End-to-End Testing Locally

```sh
# Step 1: Stop any currently running Docker containers and volumes
docker compose down -v

# Step 2: Run the automated E2E tests via Makefile
# Spins up the stack, waits for database healthchecks, and executes Playwright tests
make run-e2e
```

### 📊 Full-Stack Observability & Grafana Production Dashboard Setup

The step-by-step configuration for monitoring the production environment in FastAPI (**interview-canvas-prod**) using OpenTelemetry (OTEL) instrumentation (**app/telemetry.py**), Prometheus metrics, Loki log streams, and Tempo trace execution waterfalls in Grafana Cloud.


```sh
# Step 1: Grafana Account & Stack Instance Creation
   - Sign Up & Launch Instance
      1. Navigate to https://grafana.com/products/cloud/ and log in or create a free account.
      2. From the Grafana Cloud portal, launch your generated stack instance (e.g., whitecantaloupe3594).
      3. Grafana Instance URL: https://whitecantaloupe3594.grafana.net

   - Retrieve Instance ID & OTLP Credentials
      1. In your Grafana Cloud stack, navigate to Connections -> Add new connection -> OpenTelemetry (OTLP)
      2.  Locate your unique numeric Instance ID (User Number) (e.g., 1023456) and generate an API Key / Access Token, or go to https://grafana.com/orgs/ -> stack instance (e.g., whitecantaloupe3594) -> find OpenTelemetry -> click Configuration -> get the ID and create a token.

# Step 2: Environment Variable Configuration
Configure the following environment variables in your Render Production service deployment:
   - Set the OTLP Exporter Endpoint (Grafana Cloud Gateway), OTEL_EXPORTER_OTLP_ENDPOINT
   - Set Authorization Header KEY, OTEL_EXPORTER_OTLP_HEADERS_KEY  <Your-Base64-Grafana-Token>
   - Define Service Name, OTEL_SERVICE_NAME to isolate Production from dev, dev environment uses: interview-canvas-backend-dev, and the prod environment uses interview-canvas-backend-prod
   - Set Grafana user ID, OTEL_EXPORTER_OTLP_HEADERS_USER

# Step 3: Production Dashboard Setup
- Access Grafana Cloud Instance, navigate to https://whitecantaloupe3594.grafana.net and log in
- Create a New Dashboard, click Dashboards -> New -> New Dashboard and name it "Observability FastAPI interview-canvas-prod"
- Configure Prometheus Request Rate & Latency Metrics
   - Inside your dashboard, click + Add -> Visualization.
   - Select your Prometheus data source (e.g., grafanacloud-whitecantaloupe3594-prom).
   - Under the Query tab, paste this PromQL query: sum(rate(http_server_duration_milliseconds_count{service_name="interview-canvas-backend-prod"}[5m]))

- Configure Loki Production Log Stream
{service_name="interview-canvas-backend-prod"}

- Configure Tempo Traces Waterfall
{ resource.service.name = "interview-canvas-backend-prod" }


```