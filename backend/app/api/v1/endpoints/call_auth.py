import json
import random
import string
from fastapi import APIRouter, Depends, HTTPException, Request, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.db.session import get_db
from app.core.redis_client import get_redis
from app.core.call import get_call_provider
from app.models.sms_provider import SMSProvider, SMSProviderType
from app.models.sms_code import SMSCode, CodeMethod
from app.models.user_profile import UserProfile
from app.schemas.sms import SMSRequest, SMSVerify

router = APIRouter()

def generate_code(length: int = 4) -> str:
    return ''.join(random.choices(string.digits, k=length))

@router.post("/call/request")
async def call_request(
    request: SMSRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Запрос на звонок с кодом"""
    # Находим активного провайдера для звонков (тип callpassword)
    provider = db.query(SMSProvider).filter(
        SMSProvider.type == SMSProviderType.CALLPASSWORD,
        SMSProvider.is_active == True
    ).first()
    
    if not provider:
        raise HTTPException(status_code=503, detail="No active call provider configured")
    
    # Генерируем код
    code = generate_code(4)
    expires_at = datetime.utcnow() + timedelta(minutes=5)
    
    # Сохраняем в БД (история)
    sms_code = SMSCode(
        phone_number=request.phone,
        code=code,
        expires_at=expires_at,
        venue_id=request.venue_id,  # предполагаем, что в SMSRequest есть venue_id
        method=CodeMethod.CALL,
        provider_id=provider.id
    )
    db.add(sms_code)
    db.commit()
    db.refresh(sms_code)
    
    # Сохраняем в Redis для быстрого доступа при вебхуке и верификации
    redis = await get_redis()
    session_key = f"call:session:{request.phone}:{code}"
    await redis.setex(session_key, 300, json.dumps({
        "phone": request.phone,
        "mac": request.mac,
        "code": code,
        "verified": False,
        "sms_code_id": sms_code.id
    }))
    
    # Формируем callback URL для вебхука (должен быть публичным)
    # В production замените на реальный домен
    callback_url = "https://your-server.com/api/v1/auth/call/webhook"
    
    # Инициируем звонок через адаптер
    adapter = get_call_provider(provider)
    user_data = f"{request.phone}:{code}"  # передадим телефон и код в userData
    
    try:
        call_details = await adapter.initiate_call(
            phone=request.phone,
            user_data=user_data,
            callback_url=callback_url
        )
    except Exception as e:
        # В случае ошибки удаляем запись из БД?
        # Можно просто отметить как ошибочную, но для простоты удалим
        db.delete(sms_code)
        db.commit()
        raise HTTPException(status_code=502, detail=f"Call provider error: {str(e)}")
    
    # Обновляем запись в БД: сохраняем call_id от провайдера
    sms_code.call_id = call_details.get("call_id")
    db.add(sms_code)
    db.commit()
    
    # Возвращаем данные для отображения пользователю
    return {
        "message": "Call initiated",
        "confirmation_number": call_details.get("confirmation_number"),
        "qr_code_uri": call_details.get("qr_code_uri"),
        "call_id": call_details.get("call_id")
    }

@router.post("/call/webhook")
async def call_webhook(request: Request, background_tasks: BackgroundTasks):
    """Принимает вебхуки от CallPassword"""
    data = await request.json()
    
    call_id = data.get("callId")
    client_number = data.get("clientNumber")
    user_data = data.get("userData")
    status = data.get("status")  # предположим, есть поле status со значением "success"
    
    if status == "success" and user_data:
        try:
            phone, code = user_data.split(":")
        except:
            return {"status": "error", "message": "Invalid userData"}
        
        redis = await get_redis()
        session_key = f"call:session:{phone}:{code}"
        session_data = await redis.get(session_key)
        
        if session_data:
            data_dict = json.loads(session_data)
            data_dict["verified"] = True
            data_dict["call_id"] = call_id
            # Можно продлить время жизни, чтобы пользователь успел подтвердить
            await redis.setex(session_key, 60, json.dumps(data_dict))
            
            # Здесь можно также обновить запись в БС, например, добавить флаг call_confirmed
            # Но для этого потребуется отдельное поле в модели SMSCode, пока не добавляем.
            
            return {"status": "ok"}
    
    return {"status": "ignored"}

@router.post("/call/verify")
async def call_verify(request: SMSVerify, db: Session = Depends(get_db)):
    """Проверка кода после звонка"""
    redis = await get_redis()
    session_key = f"call:session:{request.phone}:{request.code}"
    session_data = await redis.get(session_key)
    
    if not session_data:
        raise HTTPException(status_code=400, detail="Session expired or invalid")
    
    data = json.loads(session_data)
    
    # Проверяем, подтвержден ли звонок через вебхук
    if not data.get("verified"):
        raise HTTPException(status_code=400, detail="Call not yet confirmed")
    
    # Находим запись в БД и помечаем как использованную
    sms_code = db.query(SMSCode).filter(
        SMSCode.phone_number == request.phone,
        SMSCode.code == request.code,
        SMSCode.is_used == False,
        SMSCode.expires_at > datetime.utcnow()
    ).first()
    
    if not sms_code:
        raise HTTPException(status_code=400, detail="Code not found in database")
    
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
    await redis.setex(f"auth:mac:{request.mac}", 28800, "1")
    
    # Удаляем временные данные из Redis
    await redis.delete(session_key)
    
    return {"message": "Success", "profile_id": profile.id}