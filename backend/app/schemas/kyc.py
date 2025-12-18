from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class KYCBase(BaseModel):
    pass

class KYCCreate(KYCBase):
    pass

class KYCUpdate(BaseModel):
    extracted_data: Dict[str, Any]
    status: Optional[str] = None

class KYCRecord(BaseModel):
    id: int
    user_id: int
    status: str
    extracted_data: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
