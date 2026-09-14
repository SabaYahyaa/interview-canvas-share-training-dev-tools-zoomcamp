from fastapi import APIRouter, HTTPException, status
from models.auth_models import LoginRequest, TokenResponse, User
from datetime import datetime

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    if request.email == "avery@northwind.dev" and request.password == "demo-password":
        mock_user = User(
            id="user-123",
            email=request.email,
            display_name="Test User",
            organization_id=None,
            created_at=datetime.utcnow()
        )

        return TokenResponse(
            access_token="mock_access_token",
            user=mock_user
        )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )