from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers.auth import AuthController
from app.schemas.user import UserCreate, UserLogin, Token, LoginResponse
from fastapi.security import HTTPBearer

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()

@router.post("/register", response_model=LoginResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    return AuthController.register(user, db)

@router.post("/login", response_model=LoginResponse)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user and return tokens with user profile"""
    return AuthController.login(user_credentials, db)

@router.post("/refresh", response_model=Token)
def refresh_token(token: str = Depends(security), db: Session = Depends(get_db)):
    """Refresh access token using refresh token"""
    return AuthController.refresh_token(token, db) 