#app/service/progress_service.py

from app.config.database import get_collection
from datetime import datetime
from fastapi import HTTPException
from bson import ObjectId

class ProgressService:
    @staticmethod
    async def update_learning_progress(user_id: str, algorithm_type: str) -> dict:
        users_collection =get_collection("users")
        
        update_data = {
            f"progress.learning.{algorithm_type}.completed": True,
            f"progress.learning.{algorithm_type}.lastAccessed": datetime.utcnow()
        }
        
        result = await users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
            
        user_data = await users_collection.find_one({"_id": ObjectId(user_id)})
        user_data["id"] = str(user_data["_id"])
        del user_data["_id"]
        return user_data

    @staticmethod
    async def update_practice_progress(user_id: str, algorithm_type: str, time_taken: int) -> dict:
        users_collection = get_collection("users")
        
        user_data = await users_collection.find_one({"_id": ObjectId(user_id)})
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")
            
        current_best = user_data.get("progress", {}).get("practice", {}).get(algorithm_type, {}).get("bestTime", float('inf'))
        
        update_data = {
            f"progress.practice.{algorithm_type}.attempts": user_data.get("progress", {}).get("practice", {}).get(algorithm_type, {}).get("attempts", 0) + 1
        }
        
        if time_taken < current_best:
            update_data[f"progress.practice.{algorithm_type}.bestTime"] = time_taken
        
        await users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        
        updated_user_data = await users_collection.find_one({"_id": ObjectId(user_id)})
        updated_user_data["id"] = str(updated_user_data["_id"])
        del updated_user_data["_id"]
        return updated_user_data
