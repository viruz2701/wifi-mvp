from sqlalchemy import Column, Integer, String, Boolean, DateTime, LargeBinary, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
import enum

class NASDeviceType(str, enum.Enum):
    MIKROTIK = "mikrotik"
    OPENWRT = "openwrt"
    UBIQUITI = "ubiquiti"
    # Можно добавить другие типы

class NASDevice(BaseModel):
    __tablename__ = "nas_devices"

    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=False)
    name = Column(String, nullable=False)
    type = Column(Enum(NASDeviceType), nullable=False)
    ip_address = Column(String, nullable=False)
    secret = Column(LargeBinary, nullable=False)  # зашифрованный RADIUS secret
    api_username = Column(String, nullable=True)
    api_password = Column(LargeBinary, nullable=True)  # зашифрованный пароль API
    wireguard_pubkey = Column(String, nullable=True)
    wireguard_ip = Column(String, nullable=True)
    wireguard_private_key = Column(LargeBinary, nullable=True)  # зашифрованный приватный ключ
    is_active = Column(Boolean, default=True)
    last_seen = Column(DateTime(timezone=True), nullable=True)
    status = Column(String, nullable=True)
    last_check = Column(DateTime(timezone=True), nullable=True)
    config = Column(JSON, nullable=True)  # дополнительные настройки
    wireguard_generated = Column(Boolean, default=False)
    

    # Relationships
    venue = relationship("Venue", back_populates="nas_devices")
    wireguard_peer = relationship("WireGuardPeer", back_populates="nas_device", uselist=False)