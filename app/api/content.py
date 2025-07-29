from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers.content import ContentController
from app.schemas.content import DailyContentResponse
from typing import List

router = APIRouter(prefix="/content", tags=["content"])

@router.get("/daily/{day}", response_model=DailyContentResponse)
def get_daily_content(day: int, db: Session = Depends(get_db)):
    """Get daily content for a specific day"""
    return ContentController.get_daily_content(day, db)

@router.get("/all", response_model=List[DailyContentResponse])
def get_all_content(db: Session = Depends(get_db)):
    """Get all daily content"""
    return ContentController.get_all_content(db)