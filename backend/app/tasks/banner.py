from celery import shared_task
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.banner import Banner

@shared_task
def increment_clicks(banner_id: int):
    db = SessionLocal()
    try:
        banner = db.query(Banner).filter(Banner.id == banner_id).first()
        if banner:
            banner.clicks_count += 1
            db.add(banner)
            db.commit()
    finally:
        db.close()

@shared_task
def increment_impressions(banner_id: int):
    db = SessionLocal()
    try:
        banner = db.query(Banner).filter(Banner.id == banner_id).first()
        if banner:
            banner.impressions_count += 1
            db.add(banner)
            db.commit()
    finally:
        db.close()