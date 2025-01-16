#app/models/user.py

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Dict, Optional
from bson import ObjectId
from datetime import datetime

class ProgressLearning(BaseModel):
    completed: bool = False
    lastAccessed: Optional[datetime] = None

class ProgressPractice(BaseModel):
    completed: bool = False
    bestTime: Optional[int] = None  # Dalam detik

class ProgressTest(BaseModel):
    completed: bool = False
    lastScore: Optional[int] = None  # Nilai dari 0-10
    attempts: int = 0  # Jumlah percobaan

class UserProgress(BaseModel):
    learning: Dict[str, ProgressLearning] = Field(default_factory=dict)
    practice: Dict[str, ProgressPractice] = Field(default_factory=dict)
    test: Dict[str, ProgressTest] = Field(default_factory=dict)

class UserInDB(BaseModel):
    id: str = Field(alias="_id")
    email: EmailStr
    name: str
    password: str
    role: str = "user"
    is_active: bool = True
    created_at: datetime
    updated_at: datetime
    progress: Optional[UserProgress] = Field(default_factory=UserProgress)  # Tambahkan progress di sini
    access_token: Optional[str] = None
    token_type: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str  # Konversi ObjectId ke string
        }
        from_attributes = True

