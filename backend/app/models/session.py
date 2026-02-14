from sqlalchemy import Column, Integer, String, DateTime, BigInteger, Boolean, ForeignKey
from sqlalchemy.sql import func
from app.models.base import BaseModel

class Session(BaseModel):
    __tablename__ = "sessions"

    user_profile_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=True)
    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=False)
    nas_id = Column(Integer, ForeignKey("nas_devices.id"), nullable=False)
    mac_address = Column(String(17), nullable=False, index=True)
    ip_address = Column(String(45), nullable=True)
    session_start = Column(DateTime(timezone=True), server_default=func.now())
    session_end = Column(DateTime(timezone=True), nullable=True)
    traffic_in_bytes = Column(BigInteger, default=0)
    traffic_out_bytes = Column(BigInteger, default=0)
    is_active = Column(Boolean, default=True)