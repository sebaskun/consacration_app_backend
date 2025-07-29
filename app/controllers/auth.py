from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.services.auth import AuthService
from app.schemas.user import UserCreate, UserLogin, LoginResponse
from app.utils.security import verify_token
from fastapi.security import HTTPBearer
import uuid

security = HTTPBearer()

class AuthController:
    @staticmethod
    def register(user: UserCreate, db: Session) -> LoginResponse:
        """Register a new user"""
        try:
            db_user = AuthService.create_user(db, user)
            tokens = AuthService.create_tokens(db_user)
            return LoginResponse(
                access_token=tokens.access_token,
                refresh_token=tokens.refresh_token,
                token_type=tokens.token_type,
                user=db_user
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )

    @staticmethod
    def login(user_credentials: UserLogin, db: Session) -> LoginResponse:
        """Login user and return tokens with user profile"""
        user = AuthService.authenticate_user(db, user_credentials.email, user_credentials.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email o contraseña incorrectos"
            )
        if not bool(user.is_active):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuario inactivo"
            )
        
        tokens = AuthService.create_tokens(user)
        return LoginResponse(
            access_token=tokens.access_token,
            refresh_token=tokens.refresh_token,
            token_type=tokens.token_type,
            user=user
        )

    @staticmethod
    def refresh_token(token: str, db: Session):
        """Refresh access token using refresh token"""
        payload = verify_token(token.credentials)
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
        
        user_id = str(payload.get("sub"))
        user = AuthService.get_user_by_id(db, user_id)
        if not user or not bool(user.is_active):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no encontrado o inactivo"
            )
        
        return AuthService.create_tokens(user) 