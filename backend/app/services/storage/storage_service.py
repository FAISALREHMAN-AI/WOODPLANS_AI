import os
import uuid
import aiofiles
from fastapi import UploadFile, HTTPException
from app.config import settings

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".pdf"}
ALLOWED_MIME_TYPES = {
    "image/jpeg", "image/png", "image/webp", "application/pdf"
}

class StorageService:
    def __init__(self):
        self.upload_dir = os.path.join(settings.STORAGE_DIR, "uploads")
        self.diagram_dir = os.path.join(settings.STORAGE_DIR, "diagrams")
        self.pdf_dir = os.path.join(settings.STORAGE_DIR, "pdfs")
        
        os.makedirs(self.upload_dir, exist_ok=True)
        os.makedirs(self.diagram_dir, exist_ok=True)
        os.makedirs(self.pdf_dir, exist_ok=True)

    def validate_file(self, file: UploadFile):
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file extension '{ext}'. Supported formats: JPG, JPEG, PNG, WEBP, PDF"
            )
        return ext

    async def save_upload(self, file: UploadFile, project_id: str) -> dict:
        ext = self.validate_file(file)
        unique_name = f"{project_id}_{uuid.uuid4().hex[:8]}{ext}"
        target_path = os.path.join(self.upload_dir, unique_name)
        
        size = 0
        async with aiofiles.open(target_path, "wb") as out_file:
            while content := await file.read(1024 * 1024): # 1MB chunks
                size += len(content)
                if size > settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024:
                    # Clean up
                    try:
                        os.remove(target_path)
                    except Exception:
                        pass
                    raise HTTPException(
                        status_code=413,
                        detail=f"File exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE_MB}MB."
                    )
                await out_file.write(content)

        file_type = "application/pdf" if ext == ".pdf" else f"image/{ext.replace('.', '')}"
        if ext in [".jpg", ".jpeg"]:
            file_type = "image/jpeg"

        return {
            "file_name": file.filename,
            "stored_name": unique_name,
            "file_path": target_path,
            "file_type": file_type,
            "file_size": size,
            "url": f"/api/files/uploads/{unique_name}"
        }

    def save_svg_diagram(self, project_id: str, view_name: str, svg_content: str) -> str:
        filename = f"{project_id}_{view_name}.svg"
        path = os.path.join(self.diagram_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg_content)
        return path

    def get_pdf_path(self, project_id: str) -> str:
        return os.path.join(self.pdf_dir, f"{project_id}_plan.pdf")

storage_service = StorageService()
