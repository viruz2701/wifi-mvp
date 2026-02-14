from sqlalchemy import Column, String, Boolean, Text
from app.models.base import BaseModel

class SMSProvider(BaseModel):
    __tablename__ = "sms_providers"

    name = Column(String, nullable=False)  # например "rocketsms"
    api_url = Column(String, nullable=False)
    api_key = Column(String, nullable=False)
    sender = Column(String, nullable=True)  # отправитель
    is_active = Column(Boolean, default=True)
    config = Column(Text, nullable=True)  # дополнительные параметры в JSON