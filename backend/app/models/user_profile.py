from sqlalchemy import Column, Integer, String, DateTime, BigInteger, Boolean, ForeignKey
from sqlalchemy.sql import func
from app.models.base import BaseModel

class UserProfile(BaseModel):
    __tablename__ = "user_profiles"

    mac_address = Column(String(17), unique=True, index=True, nullable=False)
    phone_number = Column(String(15), index=True, nullable=True)
    email = Column(String, nullable=True)
    full_name = Column(String, nullable=True)                # новое поле
    marketing_consent = Column(Boolean, default=False)      # новое поле
    first_seen = Column(DateTime(timezone=True), server_default=func.now())
    last_seen = Column(DateTime(timezone=True), onupdate=func.now())
    total_sessions = Column(Integer, default=0)
    total_traffic_bytes = Column(BigInteger, default=0)
    is_blocked = Column(Boolean, default=False)
    is_vip = Column(Boolean, default=False)
    device_oui = Column(String(8), nullable=True)
    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=True)
    current_tariff_id = Column(Integer, ForeignKey('tariff_plans.id'), nullable=True)
    tariff_expires_at = Column(DateTime(timezone=True), nullable=True)