from fastapi import APIRouter, Depends, HTTPException
from app.middleware.auth_handler import get_current_user
from app.services.progress_service import ProgressService

router = APIRouter()

# Endpoint untuk update progress belajar
@router.post("/learn/{algorithm}")
async def update_learning_progress(
    algorithm: str, current_user=Depends(get_current_user)
):
    if algorithm not in ["bubbleSort", "insertionSort", "selectionSort"]:
        raise HTTPException(status_code=400, detail="Invalid algorithm type")
    return await ProgressService.update_learning_progress(current_user["_id"], algorithm)

# Endpoint untuk update progress practice
@router.post("/practice/{algorithm}")
async def update_practice_progress(
    algorithm: str, time_taken: int, current_user=Depends(get_current_user)
):
    if algorithm not in ["bubbleSort", "insertionSort", "selectionSort"]:
        raise HTTPException(status_code=400, detail="Invalid algorithm type")
    return await ProgressService.update_practice_progress(current_user["_id"], algorithm, time_taken)

# Endpoint untuk update progress test
@router.post("/test/{algorithm}")
async def update_test_progress(
    algorithm: str, score: int, current_user=Depends(get_current_user)
):
    if algorithm not in ["bubbleSort", "insertionSort", "selectionSort"]:
        raise HTTPException(status_code=400, detail="Invalid algorithm type")
    return await ProgressService.update_test_progress(current_user["_id"], algorithm, score)

# Endpoint untuk mendapatkan ringkasan progress
@router.get("/progress")
async def get_progress_summary(current_user=Depends(get_current_user)):
    return await ProgressService.get_progress_summary(current_user["_id"])
