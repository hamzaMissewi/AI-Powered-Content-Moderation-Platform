# backend/app/core/exceptions.py
from fastapi import HTTPException, status
from typing import Any, Dict, Optional

class ContentModerationException(HTTPException):
    """Base exception for content moderation errors."""
    def __init__(
        self,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail: str = "An error occurred during content moderation",
        headers: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)

class ContentValidationError(ContentModerationException):
    """Exception raised when content validation fails."""
    def __init__(self, detail: str = "Content validation failed"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )

class FileUploadError(ContentModerationException):
    """Exception raised when file upload fails."""
    def __init__(self, detail: str = "File upload failed"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )

class ModelLoadError(ContentModerationException):
    """Exception raised when ML model fails to load."""
    def __init__(self, detail: str = "Failed to load ML model"):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=detail
        )

class RateLimitExceeded(ContentModerationException):
    """Exception raised when rate limit is exceeded."""
    def __init__(self, detail: str = "Rate limit exceeded"):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=detail,
            headers={"Retry-After": "60"}
        )
