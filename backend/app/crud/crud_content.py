# backend/app/crud/crud_content.py
from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.crud.base import CRUDBase
from app.models.content import Content
from app.schemas.content import ContentCreate, ContentUpdate

class CRUDContent(CRUDBase[Content, ContentCreate, ContentUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: ContentCreate, owner_id: int
    ) -> Content:
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100,
        is_approved: Optional[bool] = None, content_type: Optional[str] = None
    ) -> List[Content]:
        query = db.query(self.model).filter(Content.owner_id == owner_id)
        
        if is_approved is not None:
            query = query.filter(Content.is_approved == is_approved)
        if content_type:
            query = query.filter(Content.content_type == content_type)
        
        return query.offset(skip).limit(limit).all()
    
    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100,
        is_approved: Optional[bool] = None, content_type: Optional[str] = None
    ) -> List[Content]:
        query = db.query(self.model)
        
        if is_approved is not None:
            query = query.filter(Content.is_approved == is_approved)
        if content_type:
            query = query.filter(Content.content_type == content_type)
        
        return query.offset(skip).limit(limit).all()

content = CRUDContent(Content)