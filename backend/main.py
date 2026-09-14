from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import auth, sessions

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/v1/me")
async def get_current_user():
    return {
        "id": "user-123",
        "email": "avery@northwind.dev",
        "display_name": "Test User",
        "organization_id": None,
        "created_at": datetime.now().isoformat(),
    }


app.include_router(auth.router, prefix="/v1/auth")
app.include_router(sessions.router)