# backend/app/api/v1/endpoints/content.py
from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
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

@router.get("", response_model=List[schemas.Content])
def read_contents(
    skip: int = Query(0, ge=0),
    limit: int = Query(settings.DEFAULT_PAGE_SIZE, ge=1, le=settings.MAX_PAGE_SIZE),
    is_approved: Optional[bool] = None,
    content_type: Optional[str] = None,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Retrieve contents with pagination and filtering.
    """
    # If not superuser, only show own content
    if crud.user.is_superuser(current_user):
        contents = crud.content.get_multi(
            db, skip=skip, limit=limit, 
            is_approved=is_approved,
            content_type=content_type
        )
    else:
        contents = crud.content.get_multi_by_owner(
            db, owner_id=current_user.id, skip=skip, limit=limit,
            is_approved=is_approved,
            content_type=content_type
        )
    return contents

@router.put("/{content_id}", response_model=schemas.Content)
def update_content(
    *,
    db: Session = Depends(deps.get_db),
    content_id: int,
    content_in: schemas.ContentUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update content.
    """
    content = crud.content.get(db=db, id=content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    if not crud.user.is_superuser(current_user) and (content.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    content = crud.content.update(db=db, db_obj=content, obj_in=content_in)
    return content

@router.delete("/{content_id}", response_model=schemas.Content)
def delete_content(
    *,
    db: Session = Depends(deps.get_db),
    content_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete content.
    """
    content = crud.content.get(db=db, id=content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    if not crud.user.is_superuser(current_user) and (content.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    content = crud.content.remove(db=db, id=content_id)
    return content