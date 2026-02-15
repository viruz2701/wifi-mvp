from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc
from datetime import datetime, date
from typing import List, Optional
import csv
from io import StringIO
from fastapi.responses import StreamingResponse
from app.db.session import get_db
from app.models.session import Session as DBSession
from app.models.user_profile import UserProfile
from app.models.sms_code import SMSCode
from app.core.dependencies import get_current_active_user, get_current_marketing, get_current_venue_owner
from app.models.user import User
from app.models.venue import Venue

router = APIRouter()

def get_venue_ids_for_user(user: User, db: Session, requested_venue_id: Optional[int] = None) -> List[int]:
    """Возвращает список ID площадок, доступных пользователю."""
    if user.is_superuser or user.role == "admin":
        if requested_venue_id:
            # Проверяем, что запрошенная площадка существует
            venue = db.get(Venue, requested_venue_id)
            if not venue or venue.deleted_at is not None:
                raise HTTPException(status_code=404, detail="Venue not found")
            return [requested_venue_id]
        else:
            # Все активные площадки
            venues = db.query(Venue.id).filter(Venue.deleted_at.is_(None)).all()
            return [v.id for v in venues]
    elif user.role == "venue_owner" and user.venue_id:
        if requested_venue_id and requested_venue_id != user.venue_id:
            raise HTTPException(status_code=403, detail="Access denied to this venue")
        return [user.venue_id]
    else:
        raise HTTPException(status_code=403, detail="No venues available")

@router.get("/activity")
def activity_report(
    db: Session = Depends(get_db),
    from_date: date = Query(..., description="Начало периода (YYYY-MM-DD)"),
    to_date: date = Query(..., description="Конец периода (YYYY-MM-DD)"),
    venue_id: Optional[int] = Query(None, description="ID площадки (если не указан, то все доступные)"),
    format: str = Query("json", regex="^(json|csv)$"),
    current_user: User = Depends(get_current_marketing),
):
    """Отчёт по активности: уникальные пользователи и сессии по дням."""
    venue_ids = get_venue_ids_for_user(current_user, db, venue_id)

    query = db.query(
        func.date(DBSession.session_start).label('day'),
        func.count(DBSession.id).label('sessions'),
        func.count(func.distinct(DBSession.user_profile_id)).label('unique_users')
    ).filter(
        DBSession.venue_id.in_(venue_ids),
        DBSession.session_start >= datetime.combine(from_date, datetime.min.time()),
        DBSession.session_start <= datetime.combine(to_date, datetime.max.time()),
        DBSession.deleted_at.is_(None)
    ).group_by(func.date(DBSession.session_start)).order_by('day')

    results = query.all()

    if format == "csv":
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["day", "sessions", "unique_users"])
        for r in results:
            writer.writerow([r.day, r.sessions, r.unique_users])
        output.seek(0)
        return StreamingResponse(output, media_type="text/csv",
                                 headers={"Content-Disposition": "attachment;filename=activity.csv"})
    return [{"day": r.day, "sessions": r.sessions, "unique_users": r.unique_users} for r in results]

@router.get("/top-users")
def top_users_report(
    db: Session = Depends(get_db),
    venue_id: Optional[int] = Query(None),
    limit: int = Query(10, ge=1, le=100),
    format: str = Query("json", regex="^(json|csv)$"),
    current_user: User = Depends(get_current_marketing),
):
    """Топ пользователей по трафику и сессиям."""
    venue_ids = get_venue_ids_for_user(current_user, db, venue_id)

    top_traffic = db.query(
        UserProfile.mac_address,
        UserProfile.phone_number,
        func.sum(DBSession.traffic_in_bytes + DBSession.traffic_out_bytes).label('total_traffic'),
        func.count(DBSession.id).label('total_sessions')
    ).join(DBSession, DBSession.user_profile_id == UserProfile.id
    ).filter(
        DBSession.venue_id.in_(venue_ids),
        DBSession.deleted_at.is_(None),
        UserProfile.deleted_at.is_(None)
    ).group_by(UserProfile.id
    ).order_by(desc('total_traffic')
    ).limit(limit).all()

    if format == "csv":
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["mac", "phone", "total_traffic_bytes", "total_sessions"])
        for r in top_traffic:
            writer.writerow([r.mac_address, r.phone_number, r.total_traffic, r.total_sessions])
        output.seek(0)
        return StreamingResponse(output, media_type="text/csv",
                                 headers={"Content-Disposition": "attachment;filename=top_users.csv"})
    return [{"mac": r.mac_address, "phone": r.phone_number,
             "total_traffic_bytes": r.total_traffic, "total_sessions": r.total_sessions} for r in top_traffic]


@router.get("/dashboard-metrics")
def dashboard_metrics(
    period: str = Query("today", regex="^(today|week|month)$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    venue_ids = get_venue_ids_for_user(current_user, db, None)
    now = datetime.utcnow()
    if period == "today":
        start = datetime(now.year, now.month, now.day)
    elif period == "week":
        start = now - timedelta(days=7)
    else:  # month
        start = now - timedelta(days=30)

    # Уникальные пользователи
    unique_users = db.query(func.count(func.distinct(DBSession.user_profile_id))).filter(
        DBSession.venue_id.in_(venue_ids),
        DBSession.session_start >= start,
        DBSession.deleted_at.is_(None)
    ).scalar() or 0

    # Новые сессии
    new_sessions = db.query(func.count(DBSession.id)).filter(
        DBSession.venue_id.in_(venue_ids),
        DBSession.session_start >= start,
        DBSession.deleted_at.is_(None)
    ).scalar() or 0

    # Трафик
    traffic = db.query(func.sum(DBSession.traffic_in_bytes + DBSession.traffic_out_bytes)).filter(
        DBSession.venue_id.in_(venue_ids),
        DBSession.session_start >= start,
        DBSession.deleted_at.is_(None)
    ).scalar() or 0

    # SMS отправлено и подтверждено
    sms_sent = db.query(func.count(SMSCode.id)).filter(
        SMSCode.venue_id.in_(venue_ids),
        SMSCode.created_at >= start,
        SMSCode.deleted_at.is_(None)
    ).scalar() or 0

    sms_confirmed = db.query(func.count(SMSCode.id)).filter(
        SMSCode.venue_id.in_(venue_ids),
        SMSCode.created_at >= start,
        SMSCode.is_used == True,
        SMSCode.deleted_at.is_(None)
    ).scalar() or 0

    return {
        "unique_users": unique_users,
        "new_sessions": new_sessions,
        "total_traffic_bytes": traffic,
        "sms_sent": sms_sent,
        "sms_confirmed": sms_confirmed
    }

@router.get("/devices")
def devices_report(
    db: Session = Depends(get_db),
    venue_id: Optional[int] = Query(None),
    format: str = Query("json", regex="^(json|csv)$"),
    current_user: User = Depends(get_current_marketing),
):
    """Распределение по производителям (device_oui)."""
    venue_ids = get_venue_ids_for_user(current_user, db, venue_id)

    devices = db.query(
        UserProfile.device_oui,
        func.count(func.distinct(UserProfile.id)).label('count')
    ).join(DBSession, DBSession.user_profile_id == UserProfile.id
    ).filter(
        DBSession.venue_id.in_(venue_ids),
        UserProfile.device_oui.isnot(None),
        DBSession.deleted_at.is_(None),
        UserProfile.deleted_at.is_(None)
    ).group_by(UserProfile.device_oui
    ).all()

    if format == "csv":
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["device_oui", "count"])
        for r in devices:
            writer.writerow([r.device_oui, r.count])
        output.seek(0)
        return StreamingResponse(output, media_type="text/csv",
                                 headers={"Content-Disposition": "attachment;filename=devices.csv"})
    return [{"device_oui": r.device_oui, "count": r.count} for r in devices]

@router.get("/sms")
def sms_report(
    db: Session = Depends(get_db),
    from_date: date = Query(..., description="Начало периода"),
    to_date: date = Query(..., description="Конец периода"),
    venue_id: Optional[int] = Query(None),
    format: str = Query("json", regex="^(json|csv)$"),
    current_user: User = Depends(get_current_marketing),
):
    """Статистика по SMS: отправленные и подтверждённые коды."""
    venue_ids = get_venue_ids_for_user(current_user, db, venue_id)

    sent = db.query(func.count(SMSCode.id)).filter(
        SMSCode.venue_id.in_(venue_ids),
        SMSCode.created_at >= datetime.combine(from_date, datetime.min.time()),
        SMSCode.created_at <= datetime.combine(to_date, datetime.max.time()),
        SMSCode.deleted_at.is_(None)
    ).scalar() or 0

    verified = db.query(func.count(SMSCode.id)).filter(
        SMSCode.venue_id.in_(venue_ids),
        SMSCode.created_at >= datetime.combine(from_date, datetime.min.time()),
        SMSCode.created_at <= datetime.combine(to_date, datetime.max.time()),
        SMSCode.is_used == True,
        SMSCode.deleted_at.is_(None)
    ).scalar() or 0

    data = {"sent": sent, "verified": verified, "period": {"from": from_date, "to": to_date}}

    if format == "csv":
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["from", "to", "sent", "verified"])
        writer.writerow([from_date, to_date, sent, verified])
        output.seek(0)
        return StreamingResponse(output, media_type="text/csv",
                                 headers={"Content-Disposition": "attachment;filename=sms.csv"})
    return data