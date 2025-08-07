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
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('La contraseña debe tener al menos 8 caracteres')
        if not re.search(r'[A-Z]', v):
            raise ValueError('La contraseña debe contener al menos una letra mayúscula')
        if not re.search(r'[a-z]', v):
            raise ValueError('La contraseña debe contener al menos una letra minúscula')
        if not re.search(r'[0-9]', v):
            raise ValueError('La contraseña debe contener al menos un número')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('La contraseña debe contener al menos un carácter especial')
        return v

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    current_day: Optional[int] = None
    libre_mode: Optional[bool] = None

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
    libre_mode: bool
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

class LibreModeToggle(BaseModel):
    libre_mode: bool 