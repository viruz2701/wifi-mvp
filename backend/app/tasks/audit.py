from celery import shared_task
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.audit_log import AuditLog

@shared_task
def log_action(user_id: int, action: str, resource_type: str, resource_id: int, details: dict, ip: str):
    db = SessionLocal()
    try:
        log = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            ip_address=ip
        )
        db.add(log)
        db.commit()
    finally:
        db.close()