from sqlalchemy import Column, String, Text
from app.models.base import BaseModel

class Setting(BaseModel):
    __tablename__ = "settings"

    key = Column(String, unique=True, nullable=False, index=True)
    value = Column(Text, nullable=True)
    description = Column(String, nullable=True)