#app/schemas/user.py

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, Dict
from datetime import datetime

class ProgressLearningSchema(BaseModel):
    completed: bool = False
    lastAccessed: Optional[datetime] = None

class ProgressPracticeSchema(BaseModel):
    completed: bool = False
    bestTime: Optional[int] = None

class ProgressTestSchema(BaseModel):
    completed: bool = False
    lastScore: Optional[int] = None 
    attempts: int = 0 

class UserProgressSchema(BaseModel):
    learning: Dict[str, ProgressLearningSchema] = Field(default_factory=dict)
    practice: Dict[str, ProgressPracticeSchema] = Field(default_factory=dict)
    test: Dict[str, ProgressTestSchema] = Field(default_factory=dict)

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
    progress: Optional[UserProgressSchema] = None  
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    access_token: Optional[str] = None
    token_type: Optional[str] = None

    class Config:
        from_attributes = True

class UserProgressUpdate(BaseModel):
    algorithm_type: str = Field(..., pattern='^(bubbleSort|insertionSort|selectionSort)$')
    progress_type: str = Field(..., pattern='^(learning|practice|test)$')
    value: dict
    
    @validator('value', pre=True)
    def check_value_structure(cls, v):
        if not isinstance(v, dict):
            raise ValueError("Value must be a dictionary")
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str
