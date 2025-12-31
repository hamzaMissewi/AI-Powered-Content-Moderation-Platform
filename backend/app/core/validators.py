# backend/app/core/validators.py
import os
from typing import Optional
from fastapi import UploadFile
from app.core.config import settings
from app.core.exceptions import FileUploadError, ContentValidationError

def validate_file_upload(file: UploadFile) -> None:
    """
    Validate uploaded file for size and type.
    
    Args:
        file: The uploaded file
        
    Raises:
        FileUploadError: If file validation fails
    """
    # Check file size
    file.file.seek(0, os.SEEK_END)
    file_size = file.file.tell()
    file.file.seek(0)  # Reset file pointer
    
    if file_size > settings.MAX_UPLOAD_SIZE:
        raise FileUploadError(
            f"File size ({file_size} bytes) exceeds maximum allowed size "
            f"({settings.MAX_UPLOAD_SIZE} bytes)"
        )
    
    # Check content type
    if file.content_type not in settings.ALLOWED_IMAGE_TYPES:
        raise FileUploadError(
            f"File type '{file.content_type}' is not allowed. "
            f"Allowed types: {', '.join(settings.ALLOWED_IMAGE_TYPES)}"
        )
    
    # Check file extension
    if file.filename:
        ext = os.path.splitext(file.filename)[1].lower()
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        if ext not in allowed_extensions:
            raise FileUploadError(
                f"File extension '{ext}' is not allowed. "
                f"Allowed extensions: {', '.join(allowed_extensions)}"
            )

def validate_text_content(text: Optional[str], min_length: int = 1, max_length: int = 10000) -> None:
    """
    Validate text content.
    
    Args:
        text: The text content to validate
        min_length: Minimum text length
        max_length: Maximum text length
        
    Raises:
        ContentValidationError: If text validation fails
    """
    if not text:
        raise ContentValidationError("Text content is required")
    
    text_length = len(text.strip())
    if text_length < min_length:
        raise ContentValidationError(f"Text content must be at least {min_length} characters")
    
    if text_length > max_length:
        raise ContentValidationError(f"Text content must not exceed {max_length} characters")
