from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers.auth import AuthController
from app.schemas.user import UserCreate, UserLogin, Token, LoginResponse
from app.utils.rate_limiter import auth_rate_limiter
from fastapi.security import HTTPBearer

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()

@router.post("/register", response_model=LoginResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    return AuthController.register(user, db)

@router.post("/login", response_model=LoginResponse)
def login(user_credentials: UserLogin, request: Request, db: Session = Depends(get_db)):
    """Login user and return tokens with user profile"""
    # Use IP address for rate limiting login attempts
    client_ip = request.client.host if request.client else "unknown"
    
    # Check rate limit for login attempts
    is_allowed, remaining = auth_rate_limiter.is_allowed(client_ip)
    
    if not is_allowed:
        retry_after = auth_rate_limiter.get_retry_after(client_ip)
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "message": "Demasiados intentos de inicio de sesión. Intenta de nuevo más tarde.",
                "retry_after": retry_after,
                "remaining_requests": 0
            }
        )
    
    return AuthController.login(user_credentials, db)

@router.post("/refresh", response_model=Token)
def refresh_token(token: str = Depends(security), db: Session = Depends(get_db)):
    """Refresh access token using refresh token"""
    return AuthController.refresh_token(token, db) 