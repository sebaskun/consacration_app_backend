from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.content import DailyContentResponse
from app.models.content import DailyContent
from typing import List

class ContentController:
    @staticmethod
    def get_daily_content(day: int, db: Session) -> DailyContentResponse:
        """Get daily content for a specific day"""
        if day < 1 or day > 33:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El día debe estar entre 1 y 33"
            )
        
        content = db.query(DailyContent).filter(DailyContent.day == day).first()
        if not content:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contenido no encontrado para este día"
            )
        
        return content

    @staticmethod
    def get_all_content(db: Session) -> List[DailyContentResponse]:
        """Get all daily content"""
        content_list = db.query(DailyContent).order_by(DailyContent.day).all()
        return content_list 