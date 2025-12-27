# backend/app/api/v1/endpoints/content.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings

router = APIRouter()

@router.post("/", response_model=schemas.Content)
def create_content(
    *,
    db: Session = Depends(deps.get_db),
    content_in: schemas.ContentCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new content.
    """
    content = crud.content.create_with_owner(
        db=db, obj_in=content_in, owner_id=current_user.id
    )
    return content

@router.get("/{content_id}", response_model=schemas.Content)
def read_content(
    content_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get content by ID.
    """
    content = crud.content.get(db=db, id=content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    if not crud.user.is_superuser(current_user) and (content.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return content