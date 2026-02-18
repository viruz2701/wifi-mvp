from sqlalchemy import Column, Integer, String, Boolean, Text
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class RadiusAttribute(BaseModel):
    __tablename__ = "radius_attributes"

    name = Column(String, nullable=False, unique=True, index=True)
    vendor_id = Column(Integer, nullable=True)  # для VSA, null для стандартных
    is_proprietary = Column(Boolean, default=False)
    description = Column(Text, nullable=True)
    format_hint = Column(String, nullable=True)  # подсказка о формате

    # Связь с тарифами
    tariffs = relationship("TariffRadiusAttribute", back_populates="attribute", cascade="all, delete-orphan")