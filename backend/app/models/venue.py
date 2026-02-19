
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.models.tariff import venue_tariff

#venue_crm = Table(
#    'venue_crm',
#    BaseModel.metadata,
#    Column('venue_id', Integer, ForeignKey('venues.id'), primary_key=True),
#    Column('crm_provider_id', Integer, ForeignKey('crm_providers.id'), primary_key=True),
 ###   Column('is_active', Boolean, default=True),
#)

class Venue(BaseModel):
    __tablename__ = "venues"

    name = Column(String, nullable=False)
    description = Column(String)
    address = Column(String)
    contact_phone = Column(String)
    contact_email = Column(String)
    is_active = Column(Boolean, default=True)
    domain = Column(String, unique=True, nullable=True)
    ssl_enabled = Column(Boolean, default=False)
    crm_enabled = Column(Boolean, default=False)
    show_email_field = Column(Boolean, default=False)
    show_name_field = Column(Boolean, default=False)
    show_marketing_consent = Column(Boolean, default=False)
    allow_nas_connection_info = Column(Boolean, default=False)

    # Relationship с тарифами
    tariffs = relationship("TariffPlan", secondary=venue_tariff, back_populates="venues")
    
    # Relationship с CRM-провайдерами
    crm_providers = relationship("CRMProvider", secondary="venue_crm", back_populates="venues")
    
    # Relationship с NAS-устройствами
    nas_devices = relationship("NASDevice", back_populates="venue", cascade="all, delete-orphan")
