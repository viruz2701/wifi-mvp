from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.models.base import BaseModel

class LocalUser(BaseModel):
    __tablename__ = "local_users"

    username = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=False)
    user_profile_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=True)
    is_active = Column(Boolean, default=True)