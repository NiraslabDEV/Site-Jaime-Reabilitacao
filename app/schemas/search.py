from pydantic import BaseModel, HttpUrl
from datetime import datetime


class SearchCreate(BaseModel):
    """Search creation schema."""
    url: str


class SearchResponse(BaseModel):
    """Search response schema."""
    id: str
    user_id: str
    url: str
    created_at: datetime
    
    class Config:
        from_attributes = True


