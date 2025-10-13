from fastapi import APIRouter, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse
import os
import shutil
import uuid
from datetime import datetime

router = APIRouter(prefix="/api/v1/upload", tags=["upload"])

# Konfigurasi upload
UPLOAD_DIR = "uploads"
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png'}  
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/image")
async def upload_image(
    file: UploadFile = File(...)
):

    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File type not allowed. Only JPG, JPEG, PNG are allowed."
        )
    
    # Validasi ukuran file
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)
    
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File too large. Maximum size is 5MB"
        )
    
    # Generate nama file unik
    unique_filename = f"{uuid.uuid4().hex}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # Simpan file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving file: {str(e)}"
        )
    
    # URL untuk diakses publik
    image_url = f"/{UPLOAD_DIR}/{unique_filename}"
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Image uploaded successfully",
            "image_url": image_url,
            "filename": unique_filename,
            "original_filename": file.filename,
            "file_size": file_size,
            "uploaded_at": datetime.utcnow().isoformat()
        }
    )

@router.delete("/image")
async def delete_image(
    image_url: str
):
    """
    Delete uploaded image
    """
    try:
        # Extract filename dari URL
        filename = image_url.split("/")[-1]
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        if os.path.exists(file_path):
            os.remove(file_path)
            return {
                "message": "Image deleted successfully",
                "deleted_image": filename
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Image not found"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting image: {str(e)}"
        )