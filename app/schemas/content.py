from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class DailyContentResponse(BaseModel):
    id: str
    day: int
    title: str
    description: str
    video_url: Optional[str] = None
    rosary_video_url: Optional[str] = None
    meditation_pdf_url: Optional[str] = None
    mysteries: Optional[str] = None
    quote: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class UserProgressCreate(BaseModel):
    day: int
    meditation_completed: bool = False
    video_completed: bool = False
    rosary_completed: bool = False

class UserProgressResponse(BaseModel):
    id: str
    user_id: str
    day: int
    meditation_completed: bool
    video_completed: bool
    rosary_completed: bool
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class UserProgressSummary(BaseModel):
    day: int
    meditation_completed: bool
    video_completed: bool
    rosary_completed: bool
    total_completed: int
    total_tasks: int = 3 