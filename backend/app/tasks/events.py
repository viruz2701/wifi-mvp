from celery import shared_task
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.event import Event
from app.models.user_profile import UserProfile
from datetime import datetime

@shared_task
def record_event(venue_id: int, event_type: str, user_profile_id: int = None, data: dict = None):
    """Асинхронно записывает событие и обновляет профиль пользователя."""
    db = SessionLocal()
    try:
        event = Event(
            venue_id=venue_id,
            type=event_type,
            user_profile_id=user_profile_id,
            data=data
        )
        db.add(event)

        if user_profile_id and event_type in ['session_start', 'session_stop']:
            profile = db.query(UserProfile).filter(UserProfile.id == user_profile_id).first()
            if profile:
                if event_type == 'session_start':
                    profile.total_sessions += 1
                profile.last_seen = datetime.utcnow()
                db.add(profile)

        db.commit()
    finally:
        db.close()

@shared_task
def update_session_traffic(session_id: int, bytes_in: int, bytes_out: int):
    """Асинхронно обновляет трафик сессии (вызывается из RADIUS или NetFlow)."""
    from app.models.session import Session as DBSession
    db = SessionLocal()
    try:
        session = db.query(DBSession).filter(DBSession.id == session_id).first()
        if session:
            session.traffic_in_bytes += bytes_in
            session.traffic_out_bytes += bytes_out
            db.add(session)
            db.commit()
    finally:
        db.close()