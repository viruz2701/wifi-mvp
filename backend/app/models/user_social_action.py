from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.models.base import BaseModel

class UserSocialAction(BaseModel):
    __tablename__ = "user_social_actions"

    user_profile_id = Column(Integer, ForeignKey("user_profiles.id", ondelete="CASCADE"), nullable=False)
    action_id = Column(Integer, ForeignKey("social_actions.id", ondelete="CASCADE"), nullable=False)
    completed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    reward_tariff_id = Column(Integer, ForeignKey("tariff_plans.id"), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)  # когда закончится награда