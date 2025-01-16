#app/routes/user.py

from fastapi import APIRouter, Depends, HTTPException
from app.middleware.auth_handler import get_current_user, create_access_token, pwd_context
from app.config.database import get_collection
from app.models.user import UserInDB
from app.schemas.user import UserCreate, UserLogin
from datetime import datetime

router = APIRouter()

@router.post("/register", response_model=UserInDB)
async def register_user(user: UserCreate):
    users_collection = get_collection("users")
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = pwd_context.hash(user.password)
    user_dict = user.dict()
    user_dict.update({
        "password": hashed_password,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "is_active": True
    })
    
    new_user = await users_collection.insert_one(user_dict)
    created_user = await users_collection.find_one({"_id": new_user.inserted_id})

    created_user["_id"] = str(created_user["_id"])
    return UserInDB(**created_user)



@router.post("/login", response_model=UserInDB)
async def login_user(user: UserLogin):
    users_collection = get_collection("users")
    existing_user = await users_collection.find_one({"email": user.email})
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    if not pwd_context.verify(user.password, existing_user["password"]):
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    existing_user["access_token"] = create_access_token({"sub": str(existing_user["_id"])})
    existing_user["token_type"] = "bearer"
    existing_user["_id"] = str(existing_user["_id"])
    
    return UserInDB.from_orm(existing_user)


@router.get("/me", response_model=UserInDB)
async def get_me(current_user: dict = Depends(get_current_user)):
    current_user["_id"] = str(current_user["_id"])
    return UserInDB(**current_user)