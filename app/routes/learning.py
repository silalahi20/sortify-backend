from fastapi import APIRouter, Depends, HTTPException
from app.services.progress_service import ProgressService
from app.middleware.auth_handler import get_current_user  # Assuming this function exists and properly fetches user
from app.schemas.user import UserProgressUpdate
from typing import Dict

router = APIRouter()

@router.post("/progress")
async def update_learning_progress(
    progress_data: UserProgressUpdate,
    current_user=Depends(get_current_user)  # Updated to use get_current_user
):
    if progress_data.progress_type != "learning":
        raise HTTPException(status_code=400, detail="Invalid progress type")
    
    # Updated to use current_user from the dependency
    return await ProgressService.update_learning_progress(
        current_user.id,  # Assuming User model has an 'id' field
        progress_data.algorithm_type
    )

@router.get("/content/{algorithm_type}")
async def get_learning_content(
    algorithm_type: str,
    current_user=Depends(get_current_user)  # Added for user verification, not used here but for auth
) -> Dict:
    content = {
        "bubbleSort": {
            "title": "Bubble Sort Algorithm",
            "description": "Bubble sort is a simple sorting algorithm...",
            "timeComplexity": "O(n²)",
            "spaceComplexity": "O(1)",
            "steps": [
                "Compare adjacent elements",
                "Swap if they are in wrong order",
                "Repeat until no swaps needed"
            ]
        },
        "insertionSort": {
            "title": "Insertion Sort Algorithm",
            "description": "Insertion sort is a simple sorting algorithm...",
            "timeComplexity": "O(n²)",
            "spaceComplexity": "O(1)",
            "steps": [
                "Start from the second element",
                "Compare with previous elements",
                "Insert in correct position"
            ]
        },
        "selectionSort": {
            "title": "Selection Sort Algorithm",
            "description": "Selection sort is a simple sorting algorithm...",
            "timeComplexity": "O(n²)",
            "spaceComplexity": "O(1)",
            "steps": [
                "Find minimum element",
                "Swap with first unsorted element",
                "Repeat for remaining array"
            ]
        }
    }
    
    if algorithm_type not in content:
        raise HTTPException(status_code=404, detail="Algorithm not found")
        
    return content[algorithm_type]
