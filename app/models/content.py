from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

class DailyContent(Base):
    __tablename__ = "daily_content"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, index=True, nullable=False)
    day = Column(Integer, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    video_url = Column(String)
    rosary_video_url = Column(String)
    meditation_pdf_url = Column(String)
    mysteries = Column(String)  # JSON string of rosary mysteries
    quote = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class UserProgress(Base):
    __tablename__ = "user_progress"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, index=True, nullable=False)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    day = Column(Integer, nullable=False)
    meditation_completed = Column(Boolean, default=False)
    video_completed = Column(Boolean, default=False)
    rosary_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True, default=None)
    
    # Relationship
    user = relationship("User", back_populates="progress")
    
    class Config:
        unique_together = ("user_id", "day") 