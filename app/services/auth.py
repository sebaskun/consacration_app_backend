from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, Token
from app.utils.security import get_password_hash, verify_password, create_access_token, create_refresh_token
from fastapi import HTTPException, status
from typing import Optional
from app.models.content import UserProgress
import uuid

class AuthService:
    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:
        # Check if user already exists
        db_user = db.query(User).filter(User.email == user.email).first()
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )
        
        # Create new user
        hashed_password = get_password_hash(user.password)
        db_user = User(
            name=user.name,
            email=user.email,
            password_hash=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        # Create initial progress for day 1
        progress = UserProgress(
            user_id=db_user.id,
            day=1,
            meditation_completed=False,
            video_completed=False,
            rosary_completed=False
        )
        db.add(progress)
        db.commit()
        return db_user
    
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return None
        if not verify_password(password, str(user.password_hash)):
            return None
        return user
    
    @staticmethod
    def create_tokens(user: User) -> Token:
        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first() 