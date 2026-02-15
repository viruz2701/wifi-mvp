from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, date
import csv
import json
from io import StringIO
from fastapi.responses import StreamingResponse, JSONResponse

from app.db.session import get_db
from app.models.session import Session as DBSession
from app.models.user_profile import UserProfile
from app.models.event import Event
from app.models.user import User
from app.core.dependencies import get_current_active_user, get_current_venue_owner_or_admin
from app.crud.venue import venue as crud_venue

router = APIRouter()

def get_venue_ids_for_user(user: User, db: Session, requested_venue_id: int = None):
    """Возвращает список доступных venue_id для пользователя."""
    if user.is_superuser or user.role == 'admin':
        if requested_venue_id:
            # проверяем, что площадка существует и не удалена
            venue = crud_venue.get(db, id=requested_venue_id)
            if not venue:
                raise HTTPException(status_code=404, detail="Venue not found")
            return [requested_venue_id]
        else:
            # все активные площадки
            from app.models.venue import Venue
            venues = db.query(Venue.id).filter(Venue.deleted_at.is_(None)).all()
            return [v.id for v in venues]
    elif user.role == 'venue_owner' and user.venue_id:
        if requested_venue_id and requested_venue_id != user.venue_id:
            raise HTTPException(status_code=403, detail="Access denied to this venue")
        return [user.venue_id]
    else:
        raise HTTPException(status_code=403, detail="No venues available")

@router.get("/user-sessions")
def export_user_sessions(
    db: Session = Depends(get_db),
    venue_id: int = Query(None, description="ID площадки"),
    mac: str = Query(None, description="MAC-адрес"),
    phone: str = Query(None, description="Номер телефона"),
    from_date: date = Query(None, description="Начало периода (YYYY-MM-DD)"),
    to_date: date = Query(None, description="Конец периода (YYYY-MM-DD)"),
    format: str = Query("csv", regex="^(csv|json)$"),
    current_user: User = Depends(get_current_active_user)
):
    """
    Экспорт сессий пользователей с фильтрацией.
    Доступно администратору и владельцу площадки.
    """
    venue_ids = get_venue_ids_for_user(current_user, db, venue_id)

    query = db.query(
        DBSession.id,
        DBSession.mac_address,
        DBSession.ip_address,
        DBSession.session_start,
        DBSession.session_end,
        DBSession.traffic_in_bytes,
        DBSession.traffic_out_bytes,
        UserProfile.phone_number,
        UserProfile.email
    ).outerjoin(UserProfile, DBSession.user_profile_id == UserProfile.id
    ).filter(DBSession.venue_id.in_(venue_ids), DBSession.deleted_at.is_(None))

    if mac:
        query = query.filter(DBSession.mac_address.ilike(f"%{mac}%"))
    if phone:
        query = query.filter(UserProfile.phone_number == phone)
    if from_date:
        query = query.filter(DBSession.session_start >= datetime.combine(from_date, datetime.min.time()))
    if to_date:
        query = query.filter(DBSession.session_start <= datetime.combine(to_date, datetime.max.time()))

    results = query.all()

    if format == "json":
        data = [{
            "id": r.id,
            "mac_address": r.mac_address,
            "ip_address": r.ip_address,
            "session_start": r.session_start.isoformat() if r.session_start else None,
            "session_end": r.session_end.isoformat() if r.session_end else None,
            "traffic_in_bytes": r.traffic_in_bytes,
            "traffic_out_bytes": r.traffic_out_bytes,
            "phone_number": r.phone_number,
            "email": r.email
        } for r in results]
        return JSONResponse(content=data)
    else:  # csv
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["id", "mac_address", "ip_address", "session_start", "session_end",
                         "traffic_in_bytes", "traffic_out_bytes", "phone_number", "email"])
        for r in results:
            writer.writerow([
                r.id,
                r.mac_address,
                r.ip_address,
                r.session_start.isoformat() if r.session_start else "",
                r.session_end.isoformat() if r.session_end else "",
                r.traffic_in_bytes,
                r.traffic_out_bytes,
                r.phone_number or "",
                r.email or ""
            ])
        output.seek(0)
        return StreamingResponse(
            output,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment;filename=sessions.csv"}
        )

@router.get("/auth-logs")
def export_auth_logs(
    db: Session = Depends(get_db),
    venue_id: int = Query(None, description="ID площадки"),
    mac: str = Query(None, description="MAC-адрес"),
    phone: str = Query(None, description="Номер телефона"),
    from_date: date = Query(None, description="Начало периода"),
    to_date: date = Query(None, description="Конец периода"),
    format: str = Query("csv", regex="^(csv|json)$"),
    current_user: User = Depends(get_current_active_user)
):
    """
    Экспорт логов авторизации (auth_confirm, session_start).
    """
    venue_ids = get_venue_ids_for_user(current_user, db, venue_id)

    query = db.query(
        Event.id,
        Event.type,
        Event.created_at,
        Event.data,
        UserProfile.mac_address,
        UserProfile.phone_number
    ).join(UserProfile, Event.user_profile_id == UserProfile.id
    ).filter(
        Event.venue_id.in_(venue_ids),
        Event.type.in_(["auth_confirm", "session_start"]),
        Event.deleted_at.is_(None)
    )

    if mac:
        query = query.filter(UserProfile.mac_address.ilike(f"%{mac}%"))
    if phone:
        query = query.filter(UserProfile.phone_number == phone)
    if from_date:
        query = query.filter(Event.created_at >= datetime.combine(from_date, datetime.min.time()))
    if to_date:
        query = query.filter(Event.created_at <= datetime.combine(to_date, datetime.max.time()))

    results = query.all()

    if format == "json":
        data = [{
            "id": r.id,
            "type": r.type,
            "created_at": r.created_at.isoformat(),
            "mac_address": r.mac_address,
            "phone_number": r.phone_number,
            "data": r.data
        } for r in results]
        return JSONResponse(content=data)
    else:
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["id", "type", "created_at", "mac_address", "phone_number", "data"])
        for r in results:
            writer.writerow([
                r.id,
                r.type,
                r.created_at.isoformat(),
                r.mac_address,
                r.phone_number or "",
                json.dumps(r.data, ensure_ascii=False) if r.data else ""
            ])
        output.seek(0)
        return StreamingResponse(
            output,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment;filename=auth_logs.csv"}
        )