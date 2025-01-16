#app/schemas/user.py

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, Dict
from datetime import datetime

# Schema untuk menyimpan progress Learning
class ProgressLearningSchema(BaseModel):
    completed: bool = False
    lastAccessed: Optional[datetime] = None

# Schema untuk menyimpan progress Practice
class ProgressPracticeSchema(BaseModel):
    completed: bool = False
    bestTime: Optional[int] = None  # Waktu terbaik dalam detik

# Schema untuk menyimpan progress Test
class ProgressTestSchema(BaseModel):
    completed: bool = False
    lastScore: Optional[int] = None  # Nilai kuis terakhir
    attempts: int = 0  # Jumlah percobaan

# Schema untuk menyimpan semua progress (Learning, Practice, Test)
class UserProgressSchema(BaseModel):
    learning: Dict[str, ProgressLearningSchema] = Field(default_factory=dict)
    practice: Dict[str, ProgressPracticeSchema] = Field(default_factory=dict)
    test: Dict[str, ProgressTestSchema] = Field(default_factory=dict)

# Schema untuk pembuatan user baru
class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=2)
    password: str = Field(..., min_length=6)
    
    @validator('password')
    def validate_password(cls, value):
        if not any(c.isdigit() for c in value):
            raise ValueError("Password must contain at least one digit")
        return value

# Schema untuk respons user (termasuk progress)
class UserResponse(BaseModel):
    id: str
    email: EmailStr
    name: str
    progress: Optional[UserProgressSchema] = None  # Menyertakan progress dalam respons
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    access_token: Optional[str] = None
    token_type: Optional[str] = None

    class Config:
        from_attributes = True

# Schema untuk mengupdate progress (Learning, Practice, Test)
class UserProgressUpdate(BaseModel):
    algorithm_type: str = Field(..., pattern='^(bubbleSort|insertionSort|selectionSort)$')
    progress_type: str = Field(..., pattern='^(learning|practice|test)$')
    value: dict
    
    @validator('value', pre=True)
    def check_value_structure(cls, v):
        if not isinstance(v, dict):
            raise ValueError("Value must be a dictionary")
        return v

# Schema untuk login user
class UserLogin(BaseModel):
    email: EmailStr
    password: str
