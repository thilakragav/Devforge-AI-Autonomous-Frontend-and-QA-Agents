"""
Upload API Route
Handles file uploads (supports base64 JSON payload and direct multipart when python-multipart is present).
"""
import base64
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Optional

from backend.services.file_service import FileService

router = APIRouter(prefix="/api/upload", tags=["Upload"])
file_service = FileService()


class Base64UploadRequest(BaseModel):
    filename: str
    content_b64: str
    project_name: Optional[str] = "RDGCC Corporate Website"


@router.post("")
def upload_file(req: Base64UploadRequest):
    """
    Accepts design upload as base64-encoded file (PNG, JPG, PDF) for zero-dependency reliability.
    """
    try:
        file_bytes = base64.b64decode(req.content_b64)
        saved_path = file_service.save_upload(file_bytes, req.filename)
        preview_image = file_service.process_input_for_analysis(saved_path)
        return {
            "status": "success",
            "filename": req.filename,
            "saved_path": saved_path,
            "preview_image": preview_image
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload processing failed: {str(e)}")
