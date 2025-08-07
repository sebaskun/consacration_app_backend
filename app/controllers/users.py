from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserResponse, UserUpdate
from app.schemas.content import UserProgressCreate, UserProgressResponse, UserProgressSummary, DailyContentResponse
from app.models.user import User
from app.models.content import UserProgress, DailyContent
from app.utils.security import verify_token
from app.services.auth import AuthService
from fastapi.security import HTTPBearer
from typing import List
import uuid
from datetime import datetime, timedelta
import pytz
from app.config import settings

security = HTTPBearer()

class UserController:
    @staticmethod
    def get_current_user(token: str, db: Session) -> User:
        """Get current authenticated user"""
        payload = verify_token(token.credentials)
        if not payload or payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
        
        user_id = str(payload.get("sub"))
        user = AuthService.get_user_by_id(db, user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no encontrado o inactivo"
            )
        return user

    @staticmethod
    def get_profile(current_user: User) -> UserResponse:
        """Get current user profile"""
        return current_user

    @staticmethod
    def update_profile(user_update: UserUpdate, current_user: User, db: Session) -> UserResponse:
        """Update current user profile"""
        for field, value in user_update.dict(exclude_unset=True).items():
            setattr(current_user, field, value)
        
        db.commit()
        db.refresh(current_user)
        return current_user

    @staticmethod
    def get_progress(current_user: User, db: Session) -> List[UserProgressSummary]:
        """Get user progress for all days"""
        progress_list = db.query(UserProgress).filter(UserProgress.user_id == current_user.id).all()
        
        # Create a dictionary to map day to progress
        progress_dict = {p.day: p for p in progress_list}
        
        # Create summary for all 33 days
        summaries = []
        for day in range(1, 34):
            progress = progress_dict.get(day)
            if progress:
                total_completed = sum([
                    progress.meditation_completed,
                    progress.video_completed,
                    progress.rosary_completed
                ])
                summaries.append(UserProgressSummary(
                    day=day,
                    meditation_completed=progress.meditation_completed,
                    video_completed=progress.video_completed,
                    rosary_completed=progress.rosary_completed,
                    total_completed=total_completed
                ))
            else:
                summaries.append(UserProgressSummary(
                    day=day,
                    meditation_completed=False,
                    video_completed=False,
                    rosary_completed=False,
                    total_completed=0
                ))
        
        return summaries

    @staticmethod
    def update_progress(progress_data: UserProgressCreate, current_user: User, db: Session) -> UserProgressResponse:
        """Update user progress for a specific day"""
        if progress_data.day < 1 or progress_data.day > 33:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El día debe estar entre 1 y 33"
            )
        
        # Check if progress already exists
        existing_progress = db.query(UserProgress).filter(
            UserProgress.user_id == current_user.id,
            UserProgress.day == progress_data.day
        ).first()
        
        if existing_progress:
            # Update existing progress
            existing_progress.meditation_completed = progress_data.meditation_completed
            existing_progress.video_completed = progress_data.video_completed
            existing_progress.rosary_completed = progress_data.rosary_completed
            
            from datetime import datetime
            # Update completed_at timestamp when all tasks are completed
            if (progress_data.meditation_completed and 
                progress_data.video_completed and 
                progress_data.rosary_completed):
                existing_progress.completed_at = datetime.utcnow()
            else:
                # Clear completed_at if day is no longer fully completed
                existing_progress.completed_at = None
            
            db.commit()
            db.refresh(existing_progress)
            return existing_progress
        else:
            # Create new progress
            from datetime import datetime
            completed_at = None
            
            # Set completed_at only when all tasks are completed
            if (progress_data.meditation_completed and 
                progress_data.video_completed and 
                progress_data.rosary_completed):
                completed_at = datetime.utcnow()
            
            new_progress = UserProgress(
                user_id=current_user.id,
                day=progress_data.day,
                meditation_completed=progress_data.meditation_completed,
                video_completed=progress_data.video_completed,
                rosary_completed=progress_data.rosary_completed,
                completed_at=completed_at
            )
            
            db.add(new_progress)
            db.commit()
            db.refresh(new_progress)
            return new_progress

    @staticmethod
    def get_dashboard_data(current_user: User, db: Session):
        """Return dashboard data with progress gating logic"""
        # Get all progress for user in one query, ordered by day
        progress_list = db.query(UserProgress).filter(
            UserProgress.user_id == current_user.id
        ).order_by(UserProgress.day).all()
        
        # Create progress dict and find last completed day efficiently
        progress_dict = {p.day: p for p in progress_list}
        last_completed_day = 0
        last_completed_at = None
        
        # NEW LOGIC: Use user.current_day as the day user is currently working on
        # User can never go backwards, only stay on current day or advance forward
        
        current_day = current_user.current_day
        now = datetime.now(pytz.UTC)
        next_available_time = None
        
        # Check if current day is fully completed
        current_day_progress = progress_dict.get(current_day)
        current_day_completed = (
            current_day_progress and 
            current_day_progress.meditation_completed and 
            current_day_progress.video_completed and 
            current_day_progress.rosary_completed and
            current_day_progress.completed_at
        )
        
        if current_day_completed and current_day < 33:
            # Current day is completed, check if user can advance to next day
            if settings.debug_mode or current_user.libre_mode:
                # DEBUG MODE or LIBRE MODE: Allow immediate advancement
                current_user.current_day = min(current_day + 1, 33)
                db.commit()
                current_day = current_user.current_day
            else:
                # NORMAL MODE: Check 24-hour timer
                completed_at = current_day_progress.completed_at
                if completed_at.tzinfo is None:
                    completed_at = pytz.UTC.localize(completed_at)
                
                # Convert to Peru timezone (UTC-5)
                peru_tz = pytz.timezone('America/Lima')
                completed_at_peru = completed_at.astimezone(peru_tz)
                
                # Calculate when next day becomes available (midnight next day in Peru time)
                next_day_peru = (completed_at_peru + timedelta(days=1)).replace(
                    hour=0, minute=0, second=0, microsecond=0
                )
                
                # Convert back to UTC for storage and comparison
                next_available_time = next_day_peru.astimezone(pytz.UTC)
                
                if now >= next_available_time:
                    # Timer expired, advance to next day
                    current_user.current_day = min(current_day + 1, 33)
                    db.commit()
                    current_day = current_user.current_day
                    next_available_time = None
                # else: stay on current day, show timer
        
        available_day = current_day
        
        # Get daily content for available day
        daily_content = db.query(DailyContent).filter(
            DailyContent.day == available_day
        ).first()
        
        # Get user progress for the available day (which is user's current_day)
        user_progress = progress_dict.get(available_day)
        
        # If no progress record exists for current day, create one
        if not user_progress:
            user_progress = UserProgress(
                user_id=current_user.id,
                day=available_day,
                meditation_completed=False,
                video_completed=False,
                rosary_completed=False,
                completed_at=None
            )
            db.add(user_progress)
            db.commit()
            db.refresh(user_progress)
        
        # Clear timer in debug mode, libre mode, or if current day is not completed
        if settings.debug_mode or current_user.libre_mode or not current_day_completed:
            next_available_time = None
        
        # Add tasks to daily content
        if daily_content:
            daily_content_dict = {
                "id": daily_content.id,
                "day": daily_content.day,
                "title": daily_content.title,
                "description": daily_content.description,
                "readingTime": "5 min",  # Default reading time
                "mysteries": daily_content.mysteries or "Misterios del Rosario",
                "mysteriesDescription": "Reza el rosario completo con devoción",
                "video": {
                    "title": f"Video del Día {daily_content.day}",
                    "youtubeUrl": daily_content.video_url or ""
                },
                "rosaryVideo": {
                    "title": "Guía para Rezar el Rosario",
                    "youtubeUrl": daily_content.rosary_video_url or ""
                },
                "quote": {
                    "text": daily_content.quote,
                    "author": "San Luis María Grignion de Montfort"
                },
                "tasks": {
                    "meditationCompleted": user_progress.meditation_completed if user_progress else False,
                    "videoCompleted": user_progress.video_completed if user_progress else False,
                    "rosaryCompleted": user_progress.rosary_completed if user_progress else False
                },
                "meditationPdfUrl": daily_content.meditation_pdf_url or ""
            }
        else:
            daily_content_dict = None
        
        # Build progress summaries efficiently
        summaries = []
        for day in range(1, 34):
            p = progress_dict.get(day)
            if p:
                total_completed = sum([
                    p.meditation_completed,
                    p.video_completed,
                    p.rosary_completed
                ])
                summaries.append({
                    "day": day,
                    "meditation_completed": p.meditation_completed,
                    "video_completed": p.video_completed,
                    "rosary_completed": p.rosary_completed,
                    "total_completed": total_completed
                })
            else:
                summaries.append({
                    "day": day,
                    "meditation_completed": False,
                    "video_completed": False,
                    "rosary_completed": False,
                    "total_completed": 0
                })
        
        # Prepare user dict for frontend
        user_dict = current_user.__dict__.copy()
        user_dict["totalDays"] = 33
        user_dict["currentDay"] = available_day
        # Calculate progress percentage
        completed_tasks = sum([d["total_completed"] for d in summaries])
        total_tasks = 33 * 3
        user_dict["progressPercentage"] = int((completed_tasks / total_tasks) * 100) if total_tasks else 0

        return {
            "user": user_dict,
            "available_day": available_day,
            "progress": summaries,
            "daily_content": daily_content_dict,
            "next_available_time": next_available_time.isoformat() if next_available_time else None
        }

    @staticmethod
    def delete_account(user: User, db: Session) -> dict:
        """Delete user account and all associated data"""
        try:
            # Delete user progress first (foreign key constraint)
            db.query(UserProgress).filter(UserProgress.user_id == user.id).delete()
            
            # Delete the user
            db.delete(user)
            db.commit()
            
            return {
                "message": "Cuenta eliminada exitosamente",
                "deleted": True
            }
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar la cuenta"
            )