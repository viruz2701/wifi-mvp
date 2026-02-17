import asyncio
import json
import secrets
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.session import get_db
from app.core.redis_client import get_redis
from app.models.user_profile import UserProfile
from app.schemas.telegram import TelegramCallback
import os

router = APIRouter()

BOT_USERNAME = os.getenv("TELEGRAM_BOT_USERNAME", "your_bot_username")

@router.post("/telegram/init")
async def telegram_init(request: Request, db: Session = Depends(get_db)):
    """
    Инициирует авторизацию через Telegram.
    Генерирует уникальный state и сохраняет в Redis привязку к MAC и venue_id.
    Возвращает ссылку на бота и state для отображения QR-кода.
    """
    data = await request.json()
    mac = data.get("mac")
    venue_id = data.get("venue_id")
    
    if not mac or not venue_id:
        raise HTTPException(status_code=400, detail="mac and venue_id required")
    
    state = secrets.token_urlsafe(32)
    
    redis = await get_redis()
    # Сохраняем данные сессии на 5 минут. Используем | как разделитель, т.к. MAC содержит двоеточия
    await redis.setex(f"tg:init:{state}", 300, f"{mac}|{venue_id}")
    
    bot_link = f"https://t.me/{BOT_USERNAME}?start={state}"
    
    return {
        "state": state,
        "bot_link": bot_link,
        "qr_code_data": bot_link
    }

@router.post("/telegram/callback")
async def telegram_callback(
    callback: TelegramCallback,
    db: Session = Depends(get_db)
):
    """
    Принимает callback от Telegram-бота с номером телефона и state.
    Проверяет state, создаёт профиль пользователя и авторизует.
    """
    redis = await get_redis()
    init_key = f"tg:init:{callback.state}"
    init_data = await redis.get(init_key)
    
    if not init_data:
        raise HTTPException(status_code=400, detail="Invalid or expired state")
    
    # init_data уже строка, разделяем по |
    mac, venue_id = init_data.split("|")
    
    # Создаём или обновляем профиль пользователя
    profile = db.query(UserProfile).filter(UserProfile.mac_address == mac).first()
    if not profile:
        profile = UserProfile(
            mac_address=mac,
            phone_number=callback.phone,
            first_seen=datetime.utcnow(),
            venue_id=int(venue_id)
        )
        db.add(profile)
    else:
        profile.last_seen = datetime.utcnow()
        profile.phone_number = callback.phone
    
    db.commit()
    db.refresh(profile)
    
    # Сохраняем авторизацию в Redis для RADIUS
    await redis.setex(f"auth:mac:{mac}", 28800, "1")
    
    # Публикуем уведомление через Redis Pub/Sub
    await redis.publish(f"tg:auth:{callback.state}", "success")
    
    # Удаляем использованный init
    await redis.delete(init_key)
    
    return {"status": "ok"}

@router.get("/telegram/events")
async def telegram_events(state: str):
    """
    Server-Sent Events endpoint для уведомления клиента об успешной авторизации.
    """
    redis = await get_redis()
    pubsub = redis.pubsub()
    await pubsub.subscribe(f"tg:auth:{state}")
    
    async def event_generator():
        try:
            while True:
                message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
                if message:
                    yield f"data: {message['data']}\n\n"
                    break
                await asyncio.sleep(0.1)
        finally:
            await pubsub.unsubscribe(f"tg:auth:{state}")
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")