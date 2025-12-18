from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import shutil
import os
from ..database import get_db
from ..models import document as models
from ..schemas import document as schemas
from ..utils import security

router = APIRouter(
    prefix="/upload",
    tags=["upload"],
)

UPLOAD_DIR = "backend/uploads"

@router.post("/document", response_model=schemas.Document)
async def upload_document(
    doc_type: str,
    file: UploadFile = File(...),
    current_user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    
    file_location = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    new_doc = models.Document(
        user_id=current_user.id,
        file_path=file_location,
        doc_type=doc_type
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    return new_doc
