# import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.utils import get_superuser_token_headers

def test_create_content(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {
        "title": "Test Content",
        "description": "Test Description",
        "content": "Test content body"
    }
    response = client.post(
        f"{settings.API_V1_STR}/content/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert "id" in content