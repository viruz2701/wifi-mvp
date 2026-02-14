from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, JSON
from app.models.base import BaseModel

class PortalTemplate(BaseModel):
    __tablename__ = "portal_templates"

    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=False)
    type = Column(String, nullable=False)  # 'auth', 'welcome', 'error'
    html_content = Column(Text, nullable=False)
    css_files = Column(JSON, default=list)   # список путей к загруженным CSS
    js_files = Column(JSON, default=list)    # список путей к загруженным JS
    images = Column(JSON, default=list)      # список путей к изображениям
    is_active = Column(Boolean, default=True)