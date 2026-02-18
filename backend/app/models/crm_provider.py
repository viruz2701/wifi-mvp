from sqlalchemy import Column, Integer, String, Boolean, JSON, Enum
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
import enum

class CRMProviderType(str, enum.Enum):
    BITRIX24 = "bitrix24"
    # Здесь будут другие CRM по мере добавления

class CRMProvider(BaseModel):
    __tablename__ = "crm_providers"

    name = Column(String, nullable=False)
    type = Column(Enum(CRMProviderType), nullable=False)
    config = Column(JSON, nullable=False, default={})
    is_active = Column(Boolean, default=True)
    priority = Column(Integer, default=0)

    # Связь с площадками
    venues = relationship("Venue", secondary="venue_crm", back_populates="crm_providers")