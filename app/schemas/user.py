from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime

from app.core.password import validate_password_strength


class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, v:str):
        return validate_password_strength(v)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
    created_at: datetime

    class Config:
        from_attributes = True
