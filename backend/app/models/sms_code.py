from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.models.base import BaseModel

class SMSCode(BaseModel):
    __tablename__ = "sms_codes"

    phone_number = Column(String(15), nullable=False, index=True)
    code = Column(String(6), nullable=False)
    is_used = Column(Boolean, default=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    attempts = Column(Integer, default=0)
    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=True)  # площадка, с которой отправлен код