from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers.users import UserController
from app.schemas.user import UserResponse, UserUpdate, LibreModeToggle
from app.schemas.content import UserProgressCreate, UserProgressResponse, UserProgressSummary
from app.models.user import User
from app.utils.rate_limiter import progress_rate_limiter, libre_mode_rate_limiter
from fastapi.security import HTTPBearer
from typing import List

router = APIRouter(prefix="/users", tags=["users"])
security = HTTPBearer()

def get_current_user(token: str = Depends(security), db: Session = Depends(get_db)) -> User:
    """Get current authenticated user"""
    return UserController.get_current_user(token, db)

@router.get("/profile", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile"""
    return UserController.get_profile(current_user)

@router.put("/profile", response_model=UserResponse)
def update_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user profile"""
    return UserController.update_profile(user_update, current_user, db)

@router.get("/progress", response_model=List[UserProgressSummary])
def get_progress(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get user progress for all days"""
    return UserController.get_progress(current_user, db)

@router.post("/progress", response_model=UserProgressResponse)
def update_progress(
    progress_data: UserProgressCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user progress for a specific day"""
    # Check rate limit
    is_allowed, remaining = progress_rate_limiter.is_allowed(current_user.id)
    
    if not is_allowed:
        retry_after = progress_rate_limiter.get_retry_after(current_user.id)
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "message": "Demasiadas operaciones. Por favor, intenta de nuevo en 5 minutos.",
                "retry_after": retry_after,
                "remaining_requests": 0
            }
        )
    
    result = UserController.update_progress(progress_data, current_user, db)
    
    # Return the result directly - FastAPI will handle the response model conversion
    # We'll add headers in a middleware or use a different approach
    return result

@router.get("/dashboard")
def get_dashboard(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get all dashboard data for the user (profile, progress, available day, daily content)"""
    return UserController.get_dashboard_data(current_user, db)

@router.put("/libre-mode", response_model=UserResponse)
def toggle_libre_mode(
    libre_mode_data: LibreModeToggle,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Toggle libre mode for user"""
    # Check rate limit for libre mode changes
    is_allowed, remaining = libre_mode_rate_limiter.is_allowed(current_user.id)
    
    if not is_allowed:
        retry_after = libre_mode_rate_limiter.get_retry_after(current_user.id)
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "message": "Demasiados cambios de modo libre. Intenta de nuevo más tarde.",
                "retry_after": retry_after,
                "remaining_requests": 0
            }
        )
    
    try:
        # Validate user can change libre mode (business rule validation)
        if current_user.current_day > 33:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede cambiar el modo libre después de completar la consagración"
            )
        
        # Update with transaction safety
        current_user.libre_mode = libre_mode_data.libre_mode
        db.commit()
        db.refresh(current_user)
        return current_user
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar el modo libre"
        )

@router.delete("/account")
def delete_account(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Delete user account and all associated data"""
    return UserController.delete_account(current_user, db) 