# backend/app/schemas/content.py
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class ContentBase(BaseModel):
    content_type: str
    content: Optional[str] = None
    file_path: Optional[str] = None

class ContentCreate(ContentBase):
    pass

class ContentUpdate(ContentBase):
    is_approved: Optional[bool] = None
    moderation_result: Optional[Dict[str, Any]] = None

class ContentInDBBase(ContentBase):
    id: int
    is_approved: bool
    moderation_result: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    user_id: int

    class Config:
        from_attributes = True

class Content(ContentInDBBase):
    pass

class ContentInDB(ContentInDBBase):
    pass