from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    file_path = Column(String)
    doc_type = Column(String) # aadhaar, pan, etc.
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
