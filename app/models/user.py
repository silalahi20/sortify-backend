#app/models/user.py

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Dict, Optional
from bson import ObjectId
from datetime import datetime

class UserProgress(BaseModel):
    learning: Dict[str, Dict[str, bool]] = Field(default_factory=lambda: {
        "bubbleSort": {"completed": False, "lastAccessed": datetime.utcnow()},
        "insertionSort": {"completed": False, "lastAccessed": datetime.utcnow()},
        "selectionSort": {"completed": False, "lastAccessed": datetime.utcnow()}
    })

    @validator('*', pre=True, each_item=True)
    def update_last_accessed(cls, v):
        if 'lastAccessed' in v:
            v['lastAccessed'] = datetime.utcnow()
        return v

class UserInDB(BaseModel):
    id: str = Field(alias="_id")  # Menggunakan alias untuk ObjectId
    email: EmailStr
    name: str
    password: str
    role: str = "user"
    is_active: bool = True
    created_at: datetime
    updated_at: datetime
    access_token: Optional[str] = None
    token_type: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str  # Konversi ObjectId ke string
        }
        from_attributes = True

