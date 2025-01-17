# #app/service/progress_service.py

# from app.config.database import get_collection
# from datetime import datetime
# from bson import ObjectId
# from fastapi import HTTPException

# class ProgressService:
#     @staticmethod
#     async def update_learning_progress(user_id: str, algorithm: str) -> dict:
#         users_collection = get_collection("users")
#         update_data = {
#             f"progress.learning.{algorithm}.completed": True,
#             f"progress.learning.{algorithm}.lastAccessed": datetime.utcnow()
#         }
#         result = await users_collection.update_one(
#             {"_id": ObjectId(user_id)}, {"$set": update_data}
#         )
#         if result.modified_count == 0:
#             raise HTTPException(status_code=404, detail="User not found")
#         return {"message": f"Learning progress for {algorithm} updated successfully"}

#     @staticmethod
#     async def update_practice_progress(user_id: str, algorithm: str, time_taken: int) -> dict:
#         users_collection = get_collection("users")
#         user_data = await users_collection.find_one({"_id": ObjectId(user_id)})
#         if not user_data:
#             raise HTTPException(status_code=404, detail="User not found")

#         current_best = user_data.get("progress", {}).get("practice", {}).get(algorithm, {}).get("bestTime", float('inf'))
#         update_data = {
#             f"progress.practice.{algorithm}.completed": True,
#             f"progress.practice.{algorithm}.bestTime": min(time_taken, current_best)
#         }
#         await users_collection.update_one(
#             {"_id": ObjectId(user_id)}, {"$set": update_data}
#         )
#         return {"message": f"Practice progress for {algorithm} updated successfully"}

#     @staticmethod
#     async def update_test_progress(user_id: str, algorithm: str, score: int) -> dict:
#         users_collection = get_collection("users")
#         update_data = {
#             f"progress.test.{algorithm}.completed": True,
#             f"progress.test.{algorithm}.lastScore": score,
#             f"progress.test.{algorithm}.attempts": 1  # Increment attempts
#         }
#         user_data = await users_collection.find_one({"_id": ObjectId(user_id)})
#         if not user_data:
#             raise HTTPException(status_code=404, detail="User not found")
        
#         attempts = user_data.get("progress", {}).get("test", {}).get(algorithm, {}).get("attempts", 0)
#         update_data[f"progress.test.{algorithm}.attempts"] = attempts + 1

#         await users_collection.update_one(
#             {"_id": ObjectId(user_id)}, {"$set": update_data}
#         )
#         return {"message": f"Test progress for {algorithm} updated successfully"}

#     @staticmethod
#     async def get_progress_summary(user_id: str) -> dict:
#         users_collection = get_collection("users")
#         user_data = await users_collection.find_one({"_id": ObjectId(user_id)})
#         if not user_data:
#             raise HTTPException(status_code=404, detail="User not found")

#         progress = user_data.get("progress", {})
#         summary = {
#             "learning": ProgressService.calculate_percentage(progress.get("learning", {})),
#             "practice": ProgressService.calculate_percentage(progress.get("practice", {})),
#             "test": ProgressService.calculate_percentage(progress.get("test", {}))
#         }
#         return summary

#     @staticmethod
#     def calculate_percentage(progress_data: dict) -> int:
#         total = len(progress_data)
#         completed = sum(1 for v in progress_data.values() if v.get("completed"))
#         return int((completed / total) * 100) if total > 0 else 0
from app.config.database import get_collection
from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException


class ProgressService:
    @staticmethod
    async def update_learning_progress(user_id: str, algorithm: str) -> dict:
        users_collection = get_collection("users")
        update_data = {
            f"progress.learning.{algorithm}.completed": True,
            f"progress.learning.{algorithm}.lastAccessed": datetime.utcnow()
        }
        result = await users_collection.update_one(
            {"_id": ObjectId(user_id)}, {"$set": update_data}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": f"Learning progress for {algorithm} updated successfully"}

    @staticmethod
    async def update_practice_progress(user_id: str, algorithm: str, time_taken: int) -> dict:
        users_collection = get_collection("users")
        user_data = await users_collection.find_one({"_id": ObjectId(user_id)})
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")

        current_best = user_data.get("progress", {}).get("practice", {}).get(algorithm, {}).get("bestTime", float('inf'))
        update_data = {
            f"progress.practice.{algorithm}.completed": True,
            f"progress.practice.{algorithm}.bestTime": min(time_taken, current_best)
        }
        await users_collection.update_one(
            {"_id": ObjectId(user_id)}, {"$set": update_data}
        )
        return {"message": f"Practice progress for {algorithm} updated successfully"}

    @staticmethod
    async def update_test_progress(user_id: str, algorithm: str, score: int) -> dict:
        users_collection = get_collection("users")
        user_data = await users_collection.find_one({"_id": ObjectId(user_id)})
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")

        attempts = user_data.get("progress", {}).get("test", {}).get(algorithm, {}).get("attempts", 0)
        update_data = {
            f"progress.test.{algorithm}.completed": True,
            f"progress.test.{algorithm}.lastScore": score,
            f"progress.test.{algorithm}.attempts": attempts + 1
        }
        await users_collection.update_one(
            {"_id": ObjectId(user_id)}, {"$set": update_data}
        )
        return {"message": f"Test progress for {algorithm} updated successfully"}

    @staticmethod
    async def get_progress_summary(user_id: str) -> dict:
        users_collection = get_collection("users")
        user_data = await users_collection.find_one({"_id": ObjectId(user_id)})
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")

        progress = user_data.get("progress", {})
        summary = {
            "learning": ProgressService.calculate_percentage(progress.get("learning", {})),
            "practice": ProgressService.calculate_percentage(progress.get("practice", {})),
            "test": ProgressService.calculate_percentage(progress.get("test", {}))
        }
        return summary

    @staticmethod
    def calculate_percentage(progress_data: dict) -> float:
        """
        Menghitung persentase progress berdasarkan algoritma yang telah selesai.
        Persentase dihitung sebagai (jumlah algoritma selesai / total algoritma) * 100.
        """
        total_algorithms = 3  # Bubble Sort, Insertion Sort, Selection Sort
        if not progress_data:
            return 0.0

        # Hitung jumlah algoritma yang completed
        completed = sum(1 for v in progress_data.values() if v.get("completed", False))
        return round((completed / total_algorithms) * 100, 3)
