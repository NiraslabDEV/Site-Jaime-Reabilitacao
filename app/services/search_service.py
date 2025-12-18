from typing import List, Optional
from app.core.database import supabase
from app.schemas.search import SearchCreate, SearchResponse
from fastapi import HTTPException, status


class SearchService:
    """Service for search operations."""
    
    @staticmethod
    async def get_user_searches(user_id: str, limit: int = 20) -> List[SearchResponse]:
        """Get user's search history."""
        result = supabase.table("searches").select("*").eq("user_id", user_id).order("created_at", desc=True).limit(limit).execute()
        
        if not result.data:
            return []
        
        return [SearchResponse(**item) for item in result.data]
    
    @staticmethod
    async def create_search(user_id: str, search_data: SearchCreate) -> SearchResponse:
        """Create a new search entry."""
        new_search = supabase.table("searches").insert({
            "user_id": user_id,
            "url": search_data.url
        }).execute()
        
        if not new_search.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create search"
            )
        
        return SearchResponse(**new_search.data[0])
    
    @staticmethod
    async def delete_search(search_id: str, user_id: str) -> bool:
        """Delete a search entry if it belongs to the user."""
        # First verify the search belongs to the user
        search_result = supabase.table("searches").select("*").eq("id", search_id).eq("user_id", user_id).execute()
        
        if not search_result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Search not found or access denied"
            )
        
        # Delete the search
        delete_result = supabase.table("searches").delete().eq("id", search_id).eq("user_id", user_id).execute()
        
        return True


