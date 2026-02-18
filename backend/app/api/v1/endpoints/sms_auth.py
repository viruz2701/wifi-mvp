from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random
import string
from app.db.session import get_db
from app.core.redis_client import get_redis
from app.core.sms import send_sms_with_fallback
from app.models.sms_code import SMSCode, CodeMethod
from app.models.user_profile import UserProfile
from app.schemas.sms import SMSRequest, SMSVerify

router = APIRouter()

def generate_code(length: int = 4) -> str:
    return ''.join(random.choices(string.digits, k=length))

@router.post("/sms/request")
async def sms_request(request: SMSRequest, db: Session = Depends(get_db)):
    # Проверяем, нет ли недавнего кода для этого номера (защита от флуда)
    last_code = db.query(SMSCode).filter(
        SMSCode.phone_number == request.phone,
        SMSCode.created_at > datetime.utcnow() - timedelta(minutes=1)
    ).first()
    if last_code:
        raise HTTPException(status_code=429, detail="Too many requests")

    code = generate_code(4)
    expires_at = datetime.utcnow() + timedelta(minutes=5)

    # Сохраняем в БД
    sms_code = SMSCode(
        phone_number=request.phone,
        code=code,
        expires_at=expires_at,
        venue_id=request.venue_id,
        method=CodeMethod.SMS,
        provider_id=None
    )
    db.add(sms_code)
    db.commit()

    # Отправляем SMS через fallback-механизм
    success = await send_sms_with_fallback(db, request.phone, code)
    if not success:
        # Если ни один провайдер не сработал, логируем предупреждение
        print(f"Warning: No SMS provider available for {request.phone}, code={code}")
    else:
        print(f"SMS sent to {request.phone}, code={code}")

    return {"message": "Code sent"}

@router.post("/sms/verify")
async def sms_verify(request: SMSVerify, db: Session = Depends(get_db)):
    # Поиск кода с учётом метода SMS
    sms_code = db.query(SMSCode).filter(
        SMSCode.phone_number == request.phone,
        SMSCode.code == request.code,
        SMSCode.method == CodeMethod.SMS,
        SMSCode.is_used == False,
        SMSCode.expires_at > datetime.utcnow()
    ).first()
    if not sms_code:
        raise HTTPException(status_code=400, detail="Invalid or expired code")

    # Помечаем как использованный
    sms_code.is_used = True
    db.add(sms_code)

    # Создаём или обновляем профиль пользователя
    profile = db.query(UserProfile).filter(UserProfile.mac_address == request.mac).first()
    if not profile:
        profile = UserProfile(
            mac_address=request.mac,
            phone_number=request.phone,
            first_seen=datetime.utcnow()
        )
        db.add(profile)
    else:
        profile.last_seen = datetime.utcnow()
        profile.phone_number = request.phone

    db.commit()
    db.refresh(profile)

    # Сохраняем авторизацию в Redis для RADIUS
    redis = await get_redis()
    await redis.setex(f"auth:mac:{request.mac}", 28800, "1")

    return {"message": "Success", "profile_id": profile.id}