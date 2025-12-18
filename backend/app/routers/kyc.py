from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import kyc as models
from ..models import user as user_models
from ..models import document as doc_models
from ..schemas import kyc as schemas
from ..utils import security
from ..services import agent_stub, ocr_service, document_classifier, aadhaar_agent
from ..models import document as doc_models

router = APIRouter(
    prefix="/kyc",
    tags=["kyc"],
)

@router.post("/start", response_model=schemas.KYCRecord)
async def start_kyc(
    current_user: user_models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    # Check if pending KYC exists
    existing_kyc = db.query(models.KYCRecord).filter(
        models.KYCRecord.user_id == current_user.id,
        models.KYCRecord.status.in_(["pending", "processing"])
    ).first()
    
    if existing_kyc:
        return existing_kyc

    # Create new KYC record
    new_kyc = models.KYCRecord(user_id=current_user.id, status="processing")
    db.add(new_kyc)
    db.commit()
    db.refresh(new_kyc)

    # Get user documents
    docs = db.query(doc_models.Document).filter(doc_models.Document.user_id == current_user.id).all()
    doc_paths = [doc.file_path for doc in docs]

    # Trigger Agent (Stub)
    extracted_data = await agent_stub.run_kyc_agent(doc_paths)
    
    # Update KYC record
    new_kyc.extracted_data = extracted_data
    new_kyc.status = "review_needed"
    db.commit()
    db.refresh(new_kyc)
    
    return new_kyc

@router.get("/{kyc_id}", response_model=schemas.KYCRecord)
def get_kyc(
    kyc_id: int,
    current_user: user_models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    kyc = db.query(models.KYCRecord).filter(models.KYCRecord.id == kyc_id).first()
    if not kyc:
        raise HTTPException(status_code=404, detail="KYC record not found")
    if kyc.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return kyc

@router.post("/confirm", response_model=schemas.KYCRecord)
def confirm_kyc(
    kyc_update: schemas.KYCUpdate,
    current_user: user_models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    # Find the latest review_needed KYC
    kyc = db.query(models.KYCRecord).filter(
        models.KYCRecord.user_id == current_user.id,
        models.KYCRecord.status == "review_needed"
    ).order_by(models.KYCRecord.created_at.desc()).first()

    if not kyc:
        raise HTTPException(status_code=404, detail="No KYC record found needing review")

    kyc.extracted_data = kyc_update.extracted_data
    kyc.status = "approved" # Auto-approve for now
    db.commit()
    db.refresh(kyc)
    return kyc

@router.post("/extract/aadhaar")
async def extract_aadhaar(
    file_path: str, # In real app, might upload file here or pass ID
    current_user: user_models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    """
    Extracts Aadhaar data from a given file path (must be uploaded first).
    """
    # 1. Run OCR
    raw_text = ocr_service.extract_text(file_path)
    if not raw_text:
        raise HTTPException(status_code=400, detail="OCR failed to extract text")
        
    # 2. Classify
    doc_type = document_classifier.classify_document(raw_text)
    if doc_type != "AADHAAR":
        return {
            "error": "Document not recognized as Aadhaar",
            "detected_type": doc_type,
            "raw_text_preview": raw_text[:100]
        }
        
    # 3. Extract Fields
    extracted_data = aadhaar_agent.extract_aadhaar_fields(raw_text)
    
    return extracted_data

