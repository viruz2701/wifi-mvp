from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Enum, LargeBinary, Integer
from sqlalchemy.sql import func
from app.models.base import BaseModel
import enum

class NASDeviceType(str, enum.Enum):
    MIKROTIK = "mikrotik"
    OPENWRT = "openwrt"
    UBIQUITI = "ubiquiti"

class NASDevice(BaseModel):
    __tablename__ = "nas_devices"

    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=False)
    name = Column(String, nullable=False)
    type = Column(Enum(NASDeviceType), nullable=False)
    ip_address = Column(String, unique=True, nullable=False)
    secret = Column(LargeBinary, nullable=False)  # зашифрованный RADIUS secret
    api_username = Column(String, nullable=True)
    api_password = Column(LargeBinary, nullable=True)  # зашифрованный пароль API
    wireguard_pubkey = Column(String, nullable=True)
    wireguard_ip = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    last_seen = Column(DateTime(timezone=True), nullable=True)
    status = Column(String, default='unknown')  # 'online', 'offline', 'unknown'
    last_check = Column(DateTime(timezone=True), nullable=True)