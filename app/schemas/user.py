from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime
import re

class UserBase(BaseModel):
    name: str
    email: EmailStr

    @validator('email')
    def validate_email_provider(cls, v):
        allowed_domains = [
            'gmail.com', 'outlook.com', 'hotmail.com', 'yahoo.com', 'icloud.com'
        ]
        domain = v.split('@')[1].lower()
        if domain not in allowed_domains:
            raise ValueError(
                'Solo se permiten cuentas de Gmail, Outlook, Hotmail, Yahoo o iCloud'
            )
        return v

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    current_day: Optional[int] = None

    @validator('email')
    def validate_email_provider(cls, v):
        if v is None:
            return v
        allowed_domains = [
            'gmail.com', 'outlook.com', 'hotmail.com', 'yahoo.com', 'icloud.com'
        ]
        domain = v.split('@')[1].lower()
        if domain not in allowed_domains:
            raise ValueError(
                'Solo se permiten cuentas de Gmail, Outlook, Hotmail, Yahoo o iCloud'
            )
        return v

class UserResponse(UserBase):
    id: str
    current_day: int
    start_date: datetime
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user: UserResponse 