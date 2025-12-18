from typing import Optional
from datetime import datetime
from pydantic import BaseModel, HttpUrl


class Search(BaseModel):
    """Search model."""
    id: str
    user_id: str
    url: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class SearchCreate(BaseModel):
    """Search creation model."""
    url: str


class SearchResponse(BaseModel):
    """Search response model."""
    id: str
    user_id: str
    url: str
    created_at: datetime
    
    class Config:
        from_attributes = True


