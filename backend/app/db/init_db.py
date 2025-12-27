# backend/app/db/init_db.py
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.core.config import settings
from app.core.security import get_password_hash

def init_db(db: Session) -> None:
    # Create superuser
    user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.user.create(db, obj_in=user_in)