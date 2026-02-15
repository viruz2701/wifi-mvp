from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.models.base import BaseModel

class NASStatusHistory(BaseModel):
    __tablename__ = "nas_status_history"

    nas_device_id = Column(Integer, ForeignKey("nas_devices.id"), nullable=False)
    status = Column(String, nullable=False)  # 'online' или 'offline'
    checked_at = Column(DateTime(timezone=True), server_default=func.now())