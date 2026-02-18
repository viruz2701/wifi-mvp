from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import re
import random
import string
import json
from typing import Optional
from app.db.session import get_db
from app.models.venue import Venue
from app.models.portal_template import PortalTemplate
from app.models.user_profile import UserProfile
from app.models.banner import Banner
from app.models.sms_code import SMSCode
from app.core.redis_client import get_redis
from app.core.sms import send_sms_with_fallback
from app.core.validators import validate_phone_number, normalize_phone_number

router = APIRouter()

def render_template(html: str, context: dict) -> str:
    """Заменяет макросы вида $(name) на значения из context."""
    def replace(match):
        key = match.group(1)
        return str(context.get(key, f"$({key})"))
    return re.sub(r'\$\((\w+)\)', replace, html)

# Словарь для преобразования кодов ошибок в текст на русском
ERROR_MESSAGES = {
    "invalid_phone": "Неверный формат номера. Введите номер в международном формате (например, +375291234567).",
    "too_many_requests": "Слишком много запросов. Попробуйте позже.",
    "too_many_requests_mac": "Слишком много запросов с этого устройства. Попробуйте позже.",
    "blocked": "Доступ временно заблокирован из-за большого числа попыток.",
    "invalid_code": "Неверный код подтверждения. Попробуйте снова.",
    "code_expired": "Код истёк. Запросите новый код.",
}

@router.get("/{venue_domain}/auth", response_class=HTMLResponse)
async def auth_page(
    venue_domain: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """Страница авторизации (запрос номера телефона)."""
    venue = db.query(Venue).filter(Venue.domain == venue_domain, Venue.is_active == True).first()
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")

    template = db.query(PortalTemplate).filter(
        PortalTemplate.venue_id == venue.id,
        PortalTemplate.type == "auth",
        PortalTemplate.is_active == True
    ).first()
    if not template:
        # fallback с кнопкой Telegram
        html = """
        <!DOCTYPE html>
        <html>
        <head><title>Авторизация</title></head>
        <body>
            <h1>Добро пожаловать в Wi-Fi</h1>
            $(if error_text)
            <div class="error">$(error_text)</div>
            $(endif)
            <form method="post" action="/portal/$(venue_id)/auth">
                <input type="hidden" name="mac" value="$(mac)">
                <input type="text" name="phone" placeholder="Номер телефона" value="$(phone)">
                <button type="submit">Получить код</button>
            </form>
            <hr>
            <p>Или войдите через Telegram:</p>
            <a href="/telegram-auth?mac=$(mac)&venue_id=$(venue_id)">
                <button type="button">Войти через Telegram</button>
            </a>
        </body>
        </html>
        """
    else:
        html = template.html_content

    mac = request.query_params.get("mac", "")
    dst = request.query_params.get("dst", "")
    error_code = request.query_params.get("error", "")
    error_text = ERROR_MESSAGES.get(error_code, "")
    
    context = {
        "venue_name": venue.name,
        "mac": mac,
        "dst": dst,
        "error": error_code,
        "error_text": error_text,
        "phone": request.query_params.get("phone", ""),
        "banner_url": "",
        "venue_id": venue.id,
        "code": ""
    }
    return render_template(html, context)

@router.post("/{venue_id}/auth")
async def auth_request(
    venue_id: int,
    request: Request,
    phone: str = Form(...),
    mac: str = Form(...),
    db: Session = Depends(get_db)
):
    """Отправка кода по SMS."""
    # Валидация номера
    phone = phone.strip()
    if not validate_phone_number(phone):
        return RedirectResponse(url=f"/portal/{venue_id}/auth?error=invalid_phone&mac={mac}&phone={phone}", status_code=302)
    phone = normalize_phone_number(phone)

    # Rate limiting по IP
    client_ip = request.client.host
    redis = await get_redis()
    key_ip = f"rate:sms_ip:{client_ip}"
    count_ip = await redis.incr(key_ip)
    if count_ip == 1:
        await redis.expire(key_ip, 600)
    if count_ip > 5:
        return RedirectResponse(url=f"/portal/{venue_id}/auth?error=too_many_requests&mac={mac}&phone={phone}", status_code=302)

    key_mac = f"rate:sms_mac:{mac}"
    count_mac = await redis.incr(key_mac)
    if count_mac == 1:
        await redis.expire(key_mac, 600)
    if count_mac > 3:
        return RedirectResponse(url=f"/portal/{venue_id}/auth?error=too_many_requests_mac&mac={mac}&phone={phone}", status_code=302)

    code = ''.join(random.choices(string.digits, k=4))
    expires_at = datetime.utcnow() + timedelta(minutes=5)

    sms_code = SMSCode(phone_number=phone, code=code, expires_at=expires_at, venue_id=venue_id)
    db.add(sms_code)
    db.commit()

    # Отправляем SMS через fallback
    success = await send_sms_with_fallback(db, phone, code)
    if not success:
        # Логируем, но не прерываем поток
        print(f"Warning: No SMS provider available for {phone}, code={code}")
    else:
        print(f"SMS sent to {phone}, code={code}")

    return RedirectResponse(url=f"/portal/{venue_id}/verify?phone={phone}&mac={mac}", status_code=302)

@router.get("/{venue_id}/verify", response_class=HTMLResponse)
async def verify_page(
    venue_id: int,
    request: Request,
    phone: str,
    mac: str,
    db: Session = Depends(get_db)
):
    """Страница ввода кода."""
    # Валидация номера
    if not validate_phone_number(phone):
        return RedirectResponse(url=f"/portal/{venue_id}/auth?error=invalid_phone&mac={mac}&phone={phone}", status_code=302)
    phone = normalize_phone_number(phone)

    venue = db.get(Venue, venue_id)
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")

    template = db.query(PortalTemplate).filter(
        PortalTemplate.venue_id == venue_id,
        PortalTemplate.type == "auth",
        PortalTemplate.is_active == True
    ).first()
    if not template:
        html = """
        <!DOCTYPE html>
        <html>
        <head><title>Подтверждение</title></head>
        <body>
            <h1>Введите код из SMS</h1>
            $(if error_text)
            <div class="error">$(error_text)</div>
            $(endif)
            <form method="post" action="/portal/{venue_id}/verify">
                <input type="hidden" name="phone" value="{phone}">
                <input type="hidden" name="mac" value="{mac}">
                <input type="text" name="code" placeholder="Код">
                <button type="submit">Подтвердить</button>
            </form>
        </body>
        </html>
        """
    else:
        html = template.html_content

    error_code = request.query_params.get("error", "")
    error_text = ERROR_MESSAGES.get(error_code, "")
    
    context = {
        "venue_name": venue.name,
        "phone": phone,
        "mac": mac,
        "error": error_code,
        "error_text": error_text,
        "code": "",
        "banner_url": ""
    }
    return render_template(html, context)

@router.post("/{venue_id}/verify")
async def verify_code(
    venue_id: int,
    request: Request,
    phone: str = Form(...),
    mac: str = Form(...),
    code: str = Form(...),
    email: Optional[str] = Form(None),
    full_name: Optional[str] = Form(None),
    marketing_consent: bool = Form(False),
    db: Session = Depends(get_db)
):
    """Проверка кода и редирект на welcome."""
    phone = phone.strip()
    if not validate_phone_number(phone):
        return RedirectResponse(url=f"/portal/{venue_id}/verify?error=invalid_phone&mac={mac}&phone={phone}", status_code=302)
    phone = normalize_phone_number(phone)

    client_ip = request.client.host
    redis = await get_redis()
    key_attempt = f"rate:verify_mac:{mac}"
    attempts = await redis.incr(key_attempt)
    if attempts == 1:
        await redis.expire(key_attempt, 3600)
    if attempts > 10:
        await redis.setex(f"block:mac:{mac}", 300, "1")
        return RedirectResponse(url=f"/portal/{venue_id}/auth?error=blocked&mac={mac}&phone={phone}", status_code=302)

    # Поиск кода
    sms_code = db.query(SMSCode).filter(
        SMSCode.phone_number == phone,
        SMSCode.code == code,
        SMSCode.is_used == False,
        SMSCode.expires_at > datetime.utcnow()
    ).first()
    if not sms_code:
        return RedirectResponse(url=f"/portal/{venue_id}/verify?error=invalid_code&mac={mac}&phone={phone}", status_code=302)

    sms_code.is_used = True
    db.add(sms_code)

    # Создаём или обновляем профиль
    profile = db.query(UserProfile).filter(UserProfile.mac_address == mac).first()
    if not profile:
        profile = UserProfile(
            mac_address=mac,
            phone_number=phone,
            first_seen=datetime.utcnow(),
            email=email,
            full_name=full_name,
            marketing_consent=marketing_consent
        )
        db.add(profile)
    else:
        profile.last_seen = datetime.utcnow()
        profile.phone_number = phone
        if email:
            profile.email = email
        if full_name:
            profile.full_name = full_name
        if marketing_consent is not None:
            profile.marketing_consent = marketing_consent
    db.commit()
    db.refresh(profile)

    # Авторизация в Redis
    await redis.setex(f"auth:mac:{mac}", 28800, "1")

    # Очищаем ключ попыток (опционально)
    await redis.delete(key_attempt)

    return RedirectResponse(url=f"/portal/{venue_id}/welcome?mac={mac}", status_code=302)

@router.get("/{venue_id}/welcome", response_class=HTMLResponse)
async def welcome_page(
    venue_id: int,
    mac: str,
    db: Session = Depends(get_db)
):
    """Приветственная страница с баннером."""
    venue = db.get(Venue, venue_id)
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")

    template = db.query(PortalTemplate).filter(
        PortalTemplate.venue_id == venue_id,
        PortalTemplate.type == "welcome",
        PortalTemplate.is_active == True
    ).first()
    if not template:
        html = """
        <!DOCTYPE html>
        <html>
        <head><title>Добро пожаловать</title></head>
        <body>
            <h1>Вы успешно авторизованы!</h1>
            <p>MAC: {mac}</p>
            <img src="{banner_url}" alt="Баннер">
        </body>
        </html>
        """
    else:
        html = template.html_content

    banner = db.query(Banner).filter(Banner.venue_id == venue_id, Banner.is_active == True).first()
    banner_url = banner.image_url if banner else ""

    context = {
        "venue_name": venue.name,
        "mac": mac,
        "banner_url": banner_url,
        "phone": "",
        "code": "",
        "error": ""
    }
    return render_template(html, context)