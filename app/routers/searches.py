from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.search import SearchCreate, SearchResponse
from app.services.search_service import SearchService
from app.routers.dependencies import get_current_user_id

router = APIRouter(prefix="/searches", tags=["searches"])


@router.get("", response_model=List[SearchResponse])
async def get_searches(current_user_id: str = Depends(get_current_user_id)):
    """Get user's search history (last 20 searches)."""
    return await SearchService.get_user_searches(current_user_id, limit=20)


@router.post("", response_model=SearchResponse, status_code=status.HTTP_201_CREATED)
async def create_search(
    search_data: SearchCreate,
    current_user_id: str = Depends(get_current_user_id)
):
    """Save a new documentation URL."""
    return await SearchService.create_search(current_user_id, search_data)


@router.delete("/{search_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_search(
    search_id: str,
    current_user_id: str = Depends(get_current_user_id)
):
    """Delete a search entry."""
    await SearchService.delete_search(search_id, current_user_id)
    return None


