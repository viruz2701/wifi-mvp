from sqlalchemy import Column, String, Boolean, JSON, Enum
from app.models.base import BaseModel
import enum

class SocialActionType(str, enum.Enum):
    LIKE = "like"
    SHARE = "share"
    SUBSCRIBE = "subscribe"
    FOLLOW = "follow"

class SocialNetwork(str, enum.Enum):
    VK = "vk"
    TELEGRAM = "telegram"
    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"
    VIBER = "viber"  # добавлен Viber

class SocialAction(BaseModel):
    __tablename__ = "social_actions"

    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    type = Column(Enum(SocialActionType), nullable=False)
    network = Column(Enum(SocialNetwork), nullable=False)
    config = Column(JSON, nullable=False, default={})  # параметры для проверки (например, group_id, app_id, token)
    is_active = Column(Boolean, default=True)