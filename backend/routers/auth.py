from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Optional

from backend.models.schemas import UserRegisterRequest, UserLoginRequest, UserUpdateRequest, AuthResponse, UserResponse
from backend.services.auth_service import register_user, login_user, get_current_user, update_user_profile

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

def get_bearer_token(authorization: Optional[str] = Header(None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Bearer token")
    return authorization.split("Bearer ", 1)[1].strip()

@router.post("/register", response_model=AuthResponse)
async def api_register(req: UserRegisterRequest):
    try:
        return register_user(req)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@router.post("/login", response_model=AuthResponse)
async def api_login(req: UserLoginRequest):
    try:
        return login_user(req)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

@router.get("/me", response_model=UserResponse)
async def api_get_current_user(token: str = Depends(get_bearer_token)):
    user = get_current_user(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user

@router.put("/profile", response_model=UserResponse)
async def api_update_user_profile(req: UserUpdateRequest, token: str = Depends(get_bearer_token)):
    user = get_current_user(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    try:
        return update_user_profile(user.id, req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update profile: {str(e)}")
