# backend/app/tests/utils/utils.py
from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.crud import crud_user
from app.schemas import UserCreate
# from app.core.security import get_password_hash

def user_authentication_headers(
    *, client: TestClient, email: str, password: str
) -> Dict[str, str]:
    data = {"username": email, "password": password}
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers

def create_random_user(db: Session) -> User:
    email = "user@example.com"
    password = "random-passW0rd"
    user_in = UserCreate(
        email=email,
        password=password,
        full_name="Test User",
    )
    user = crud_user.user.create(db, obj_in=user_in)
    return user

def get_superuser_token_headers(client: TestClient) -> Dict[str, str]:
    return user_authentication_headers(
        client=client,
        email=settings.FIRST_SUPERUSER,
        password=settings.FIRST_SUPERUSER_PASSWORD,
    )