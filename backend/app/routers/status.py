from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import kyc as models
from ..schemas import kyc as schemas
from ..utils import security

router = APIRouter(
    prefix="/status",
    tags=["status"],
)

@router.get("/{kyc_id}", response_model=schemas.KYCRecord)
def get_status(
    kyc_id: int,
    current_user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    kyc = db.query(models.KYCRecord).filter(models.KYCRecord.id == kyc_id).first()
    if not kyc:
        raise HTTPException(status_code=404, detail="KYC record not found")
    if kyc.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return kyc
