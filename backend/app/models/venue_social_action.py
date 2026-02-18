from sqlalchemy import Column, Integer, ForeignKey
from app.models.base import BaseModel

class VenueSocialAction(BaseModel):
    __tablename__ = "venue_social_actions"

    venue_id = Column(Integer, ForeignKey("venues.id", ondelete="CASCADE"), nullable=False)
    action_id = Column(Integer, ForeignKey("social_actions.id", ondelete="CASCADE"), nullable=False)
    reward_tariff_id = Column(Integer, ForeignKey("tariff_plans.id"), nullable=True)  # тариф-награда
    reward_duration_hours = Column(Integer, nullable=False, default=1)  # длительность награды