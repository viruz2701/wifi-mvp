from sqlalchemy import Column, String, Boolean, DateTime
from app.models.base import BaseModel

class Venue(BaseModel):
    __tablename__ = "venues"

    name = Column(String, nullable=False)
    description = Column(String)
    address = Column(String)
    contact_phone = Column(String)
    contact_email = Column(String)
    is_active = Column(Boolean, default=True)
    # Новые поля для этапа 4
    domain = Column(String, unique=True, nullable=True)       # уникальный домен площадки
    ssl_enabled = Column(Boolean, default=False)             # флаг HTTPS