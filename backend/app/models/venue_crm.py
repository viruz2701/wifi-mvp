from sqlalchemy import Column, Integer, Boolean, JSON, ForeignKey
from app.models.base import BaseModel

class VenueCRM(BaseModel):
    __tablename__ = "venue_crm"

    venue_id = Column(Integer, ForeignKey("venues.id", ondelete="CASCADE"), primary_key=True)
    crm_provider_id = Column(Integer, ForeignKey("crm_providers.id", ondelete="CASCADE"), primary_key=True)
    is_active = Column(Boolean, default=True)
    config_override = Column(JSON, nullable=True)  # переопределение настроек для конкретной площадки