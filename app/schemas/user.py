from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=2)
    password: str = Field(..., min_length=6)
    @validator('password')
    def validate_password(cls, value):
        if not any(c.isdigit() for c in value):
            raise ValueError("Password must contain at least one digit")
        return value

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    name: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    access_token: Optional[str] = None
    token_type: Optional[str] = None

    class Config:
        from_attributes = True

class UserProgressUpdate(BaseModel):
    algorithm_type: str = Field(..., pattern='^(bubbleSort|insertionSort|selectionSort)$')
    progress_type: str = Field(..., pattern='^(learning|practice|quiz)$')
    value: dict
    @validator('value', pre=True)
    def check_value_structure(cls, v):
        if not isinstance(v, dict):
            raise ValueError("Value must be a dictionary")
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str
