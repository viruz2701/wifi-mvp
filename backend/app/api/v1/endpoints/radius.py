from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from datetime import datetime
from app.db.session import get_db
from app.models.session import Session as RadiusSession
from app.models.user_profile import UserProfile
from app.core.redis_client import get_redis

router = APIRouter()

@router.post("/authorize")
async def radius_authorize(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    # Ожидаем формат от freeradius-rest
    mac = data.get("Calling-Station-Id", "").replace("-", ":").upper()
    username = data.get("User-Name")  # может быть телефон или логин

    # Проверяем в Redis, есть ли авторизация для этого MAC
    redis = await get_redis()
    authorized = await redis.get(f"auth:mac:{mac}")
    if authorized:
        return {"result": "Access-Accept"}
    else:
        return {"result": "Access-Reject"}

@router.post("/accounting")
async def radius_accounting(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    acct_status = data.get("Acct-Status-Type")
    mac = data.get("Calling-Station-Id", "").replace("-", ":").upper()
    session_id = data.get("Acct-Session-Id")
    nas_ip = data.get("NAS-IP-Address")
    framed_ip = data.get("Framed-IP-Address")
    # Для определения nas_id и venue_id нужно будет реализовать поиск по NAS-IP
    # Пока используем заглушки
    nas_id = 1
    venue_id = 1

    if acct_status == "Start":
        session = RadiusSession(
            mac_address=mac,
            nas_id=nas_id,
            venue_id=venue_id,
            ip_address=framed_ip,
            session_start=datetime.utcnow()
        )
        db.add(session)
        db.commit()
    elif acct_status == "Stop":
        session = db.query(RadiusSession).filter(
            RadiusSession.session_id == session_id,
            RadiusSession.is_active == True
        ).first()
        if session:
            session.session_end = datetime.utcnow()
            session.is_active = False
            session.traffic_in_bytes = int(data.get("Acct-Input-Octets", 0))
            session.traffic_out_bytes = int(data.get("Acct-Output-Octets", 0))
            db.add(session)
            db.commit()
    # Обработка Interim-Update аналогично

    return {"result": "ok"}