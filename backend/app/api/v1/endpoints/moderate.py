# backend/app/api/v1/endpoints/moderate.py
from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import Optional
from pydantic import BaseModel
from app.ml.content_moderator import ContentModerator
import aiofiles
import os
from datetime import datetime

router = APIRouter()
moderator = ContentModerator()

class ModerationRequest(BaseModel):
    text: Optional[str] = None
    content_type: str

@router.post("/moderate/text")
async def moderate_text(request: ModerationRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="Text content is required")
    
    try:
        result = await moderator.moderate_text(request.text)
        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/moderate/image")
async def moderate_image(file: UploadFile = File(...)):
    try:
        # Save the uploaded file temporarily
        file_path = f"/tmp/{file.filename}"
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        
        # Process the image (placeholder for actual ML processing)
        result = {
            "is_approved": True,
            "categories": {
                "explicit": {"score": 0.1, "is_violation": False},
                "violence": {"score": 0.2, "is_violation": False},
                "suggestive": {"score": 0.3, "is_violation": False}
            }
        }
        
        # Clean up
        os.remove(file_path)
        
        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))