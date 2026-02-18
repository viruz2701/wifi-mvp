from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class TariffRadiusAttribute(BaseModel):
    __tablename__ = "tariff_radius_attributes"

    tariff_id = Column(Integer, ForeignKey("tariff_plans.id", ondelete="CASCADE"), nullable=False)
    attribute_id = Column(Integer, ForeignKey("radius_attributes.id", ondelete="CASCADE"), nullable=False)
    value = Column(String, nullable=False)  # строковое значение атрибута

    tariff = relationship("TariffPlan", back_populates="radius_attributes")
    attribute = relationship("RadiusAttribute", back_populates="tariffs")