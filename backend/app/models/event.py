from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.models.base import BaseModel

class Event(BaseModel):
    __tablename__ = "events"

    user_profile_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=True)
    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=False)
    type = Column(String, nullable=False)          # session_start, session_stop, session_update
    data = Column(JSON, nullable=True)             # дополнительные данные (ip, bytes и т.п.)
    created_at = Column(DateTime(timezone=True), server_default=func.now())