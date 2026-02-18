from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class WireGuardPeer(BaseModel):
    __tablename__ = "wireguard_peers"

    nas_device_id = Column(Integer, ForeignKey("nas_devices.id"), nullable=False, unique=True)
    public_key = Column(String, nullable=False)
    allowed_ips = Column(String, nullable=False)
    endpoint = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    # Relationship с NASDevice
    nas_device = relationship("NASDevice", back_populates="wireguard_peer")