from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.db.session import get_db
from app.models.session import Session as RadiusSession
from app.models.user_profile import UserProfile
from app.models.nas_device import NASDevice
from app.models.tariff import TariffPlan
from app.core.redis_client import get_redis

router = APIRouter()

@router.post("/authorize")
async def radius_authorize(request: Request, db: Session = Depends(get_db)):
    """
    RADIUS authorization endpoint.
    Ожидает JSON от freeradius-rest.
    Возвращает Access-Accept или Access-Reject с возможными атрибутами скорости.
    """
    data = await request.json()
    mac = data.get("Calling-Station-Id", "").replace("-", ":").upper()
    
    # Проверяем авторизацию в Redis (установлена при успешном входе через SMS/Call/Telegram)
    redis = await get_redis()
    authorized = await redis.get(f"auth:mac:{mac}")
    if not authorized:
        return {"result": "Access-Reject"}
    
    # Получаем профиль пользователя
    profile = db.query(UserProfile).filter(UserProfile.mac_address == mac).first()
    if not profile:
        # Если профиль не найден, но есть ключ в Redis – возможно, нужно создать профиль?
        # На всякий случай отклоняем, чтобы избежать несоответствий.
        return {"result": "Access-Reject"}
    
    # Проверяем наличие активного тарифа
    attributes = {}
    if profile.current_tariff_id and profile.tariff_expires_at and profile.tariff_expires_at > datetime.utcnow():
        tariff = db.get(TariffPlan, profile.current_tariff_id)
        if tariff:
            if tariff.speed_limit_up_kbps:
                attributes["WISPr-Bandwidth-Max-Up"] = str(tariff.speed_limit_up_kbps)
            if tariff.speed_limit_down_kbps:
                attributes["WISPr-Bandwidth-Max-Down"] = str(tariff.speed_limit_down_kbps)
    
    response = {"result": "Access-Accept"}
    if attributes:
        response["attributes"] = attributes
    return response


@router.post("/accounting")
async def radius_accounting(request: Request, db: Session = Depends(get_db)):
    """
    RADIUS accounting endpoint.
    Принимает Start/Stop/Interim-Update пакеты и сохраняет сессии.
    """
    data = await request.json()
    acct_status = data.get("Acct-Status-Type")
    mac = data.get("Calling-Station-Id", "").replace("-", ":").upper()
    session_id = data.get("Acct-Session-Id")
    nas_ip = data.get("NAS-IP-Address")
    framed_ip = data.get("Framed-IP-Address")
    
    # Определяем NAS устройство по IP (может быть основной IP или WireGuard IP)
    nas = db.query(NASDevice).filter(
        (NASDevice.ip_address == nas_ip) | (NASDevice.wireguard_ip == nas_ip)
    ).first()
    if not nas:
        # Если NAS не найден, логируем ошибку, но не прерываем обработку
        # Можно вернуть ошибку, чтобы клиент знал, но для совместимости вернём ok
        return {"result": "error", "message": "NAS not found"}
    
    nas_id = nas.id
    venue_id = nas.venue_id

    if acct_status == "Start":
        # Проверяем, нет ли уже активной сессии для этого MAC на этом NAS
        existing = db.query(RadiusSession).filter(
            RadiusSession.mac_address == mac,
            RadiusSession.nas_id == nas_id,
            RadiusSession.is_active == True
        ).first()
        if existing:
            # Закрываем старую сессию
            existing.is_active = False
            existing.session_end = datetime.utcnow()
            db.add(existing)
        
        # Создаём новую сессию
        session = RadiusSession(
            mac_address=mac,
            nas_id=nas_id,
            venue_id=venue_id,
            ip_address=framed_ip,
            session_start=datetime.utcnow(),
            is_active=True
        )
        db.add(session)
        db.commit()
        
    elif acct_status == "Stop":
        # Завершаем сессию
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
            
    elif acct_status == "Interim-Update":
        # Обновляем трафик
        session = db.query(RadiusSession).filter(
            RadiusSession.session_id == session_id,
            RadiusSession.is_active == True
        ).first()
        if session:
            session.traffic_in_bytes = int(data.get("Acct-Input-Octets", 0))
            session.traffic_out_bytes = int(data.get("Acct-Output-Octets", 0))
            db.add(session)
            db.commit()
    
    return {"result": "ok"}