import os
import tempfile
import logging
from fastapi import APIRouter, UploadFile, File, Depends
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

from app.services.ml_service import ContentModerator
from app.core.validators import validate_file_upload, validate_text_content
from app.core.exceptions import FileUploadError, ContentValidationError, ModelLoadError
from app.api import deps
from app import models

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize moderator (lazy loading would be better in production)
try:
    moderator = ContentModerator()
except Exception as e:
    logger.error(f"Failed to initialize ContentModerator: {e}")
    moderator = None

class ModerationRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000, description="Text content to moderate")
    content_type: Optional[str] = Field(default="text", description="Type of content")

class ModerationResponse(BaseModel):
    status: str
    data: dict
    timestamp: str

@router.post("/text", response_model=ModerationResponse)
async def moderate_text(
    request: ModerationRequest,
    current_user: models.User = Depends(deps.get_current_active_user)
):
    """
    Moderate text content for inappropriate content.
    
    - **text**: Text content to moderate (required)
    - **content_type**: Type of content (default: "text")
    """
    # Validate text content
    validate_text_content(request.text)
    
    if not moderator:
        raise ModelLoadError("Content moderation service is not available")
    
    try:
        result = await moderator.moderate_text(request.text)
        return ModerationResponse(
            status="success",
            data=result,
            timestamp=datetime.utcnow().isoformat()
        )
    except Exception as e:
        logger.error(f"Error in text moderation: {e}", exc_info=True)
        raise ModelLoadError(f"Error during text moderation: {str(e)}")

@router.post("/image", response_model=ModerationResponse)
async def moderate_image(
    file: UploadFile = File(...),
    current_user: models.User = Depends(deps.get_current_active_user)
):
    """
    Moderate image content for inappropriate content.
    
    - **file**: Image file to moderate (JPEG, PNG, GIF, or WebP)
    """
    # Validate file upload
    validate_file_upload(file)
    
    if not moderator:
        raise ModelLoadError("Content moderation service is not available")
    
    file_path = None
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp_file:
            file_path = tmp_file.name
            content = await file.read()
            tmp_file.write(content)
        
        # Read file as bytes for moderation
        with open(file_path, 'rb') as f:
            image_bytes = f.read()
        
        # Process the image
        result = await moderator.moderate_image(image_bytes)
        
        return ModerationResponse(
            status="success",
            data=result,
            timestamp=datetime.utcnow().isoformat()
        )
        
    except (FileUploadError, ModelLoadError):
        raise
    except Exception as e:
        logger.error(f"Error in image moderation: {e}", exc_info=True)
        raise ModelLoadError(f"Error during image moderation: {str(e)}")
    finally:
        # Clean up temporary file
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                logger.warning(f"Failed to remove temporary file {file_path}: {e}")