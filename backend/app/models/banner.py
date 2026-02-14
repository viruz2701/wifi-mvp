from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.models.base import BaseModel

class Banner(BaseModel):
    __tablename__ = "banners"

    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=False)
    image_url = Column(String, nullable=False)     # путь к изображению
    target_url = Column(String, nullable=False)    # ссылка при клике
    clicks_count = Column(Integer, default=0)
    impressions_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)