# backend/app/crud/crud_content.py
from typing import List, Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.content import Content
from app.schemas.content import ContentCreate, ContentUpdate

class CRUDContent(CRUDBase[Content, ContentCreate, ContentUpdate]):
    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Content]:
        return (
            db.query(self.model)
            .filter(Content.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

content = CRUDContent(Content)