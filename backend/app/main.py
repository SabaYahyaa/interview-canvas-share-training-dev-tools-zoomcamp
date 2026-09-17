import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.routers.sessions import router as sessions_router
from contextlib import asynccontextmanager
from app.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs automatically when container starts
    init_db()
    yield

app = FastAPI(title="Interviewer Canvas API", lifespan=lifespan)
# Enable CORS for local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Router
app.include_router(sessions_router)

# ==========================================
# STATIC FILES & SPA FALLBACK
# ==========================================
# Resolve static directory across common Docker/Local project structures
POSSIBLE_STATIC_DIRS = [
    os.path.abspath("static"),
    os.path.abspath("static/client"),
    os.path.abspath("/app/static"),
]

STATIC_DIR = None
for directory in POSSIBLE_STATIC_DIRS:
    if os.path.exists(os.path.join(directory, "index.html")):
        STATIC_DIR = directory
        break

if not STATIC_DIR and os.path.exists("static"):
    STATIC_DIR = os.path.abspath("static")

# Mount /assets if present (where Vite builds compiled CSS & JS)
if STATIC_DIR:
    assets_dir = os.path.join(STATIC_DIR, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")
    elif os.path.exists(STATIC_DIR):
        app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.api_route("/{full_path:path}", methods=["GET"])
async def serve_spa(request: Request, full_path: str):
    # Pass-through for API, WebSockets, and Swagger docs
    if (
        full_path.startswith("v1")
        or full_path.startswith("ws")
        or full_path in ["docs", "openapi.json", "redoc"]
    ):
        raise HTTPException(status_code=404, detail="API route not found")

    if not STATIC_DIR:
        return {"message": "API Server Running (No static frontend found)"}

    # Serve direct file matches (e.g. favicon, static assets)
    file_path = os.path.join(STATIC_DIR, full_path)
    if os.path.isfile(file_path):
        return FileResponse(file_path)

    # Single-Page Application (SPA) fallback for /room/{session_id} or other frontend routes
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)

    raise HTTPException(status_code=404, detail="Index file not found")
