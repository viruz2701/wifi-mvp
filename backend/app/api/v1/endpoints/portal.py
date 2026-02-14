from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import re
from app.db.session import get_db
from app.models.venue import Venue
from app.models.portal_template import PortalTemplate
from app.models.user_profile import UserProfile
from app.models.banner import Banner
from app.crud.sms_code import sms_code as crud_sms_code
from app.core.redis_client import get_redis
from app.core.sms import get_sms_provider, SMSAdapter
from app.schemas.sms import SMSRequest, SMSVerify
import random
import string

router = APIRouter()

def render_template(html: str, context: dict) -> str:
    """Заменяет макросы вида $(name) на значения из context."""
    def replace(match):
        key = match.group(1)
        return str(context.get(key, f"$({key})"))
    return re.sub(r'\$\((\w+)\)', replace, html)

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
        # fallback на простейший шаблон
        html = """
        <!DOCTYPE html>
        <html>
        <head><title>Авторизация</title></head>
        <body>
            <h1>Добро пожаловать в Wi-Fi</h1>
            <form method="post" action="/portal/{venue_id}/auth">
                <input type="hidden" name="mac" value="{mac}">
                <input type="text" name="phone" placeholder="Номер телефона">
                <button type="submit">Получить код</button>
            </form>
        </body>
        </html>
        """
    else:
        html = template.html_content

    mac = request.query_params.get("mac", "")
    dst = request.query_params.get("dst", "")
    context = {
        "venue_name": venue.name,
        "mac": mac,
        "dst": dst,
        "error": request.query_params.get("error", ""),
        "phone": "",
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
    # Rate limiting по IP
    client_ip = request.client.host
    redis = await get_redis()
    key_ip = f"rate:sms_ip:{client_ip}"
    count_ip = await redis.incr(key_ip)
    if count_ip == 1:
        await redis.expire(key_ip, 600)  # 10 минут
    if count_ip > 5:
        return RedirectResponse(url=f"/portal/{venue_id}/auth?error=too_many_requests&mac={mac}", status_code=302)

    # Rate limiting по MAC (опционально)
    key_mac = f"rate:sms_mac:{mac}"
    count_mac = await redis.incr(key_mac)
    if count_mac == 1:
        await redis.expire(key_mac, 600)
    if count_mac > 3:
        return RedirectResponse(url=f"/portal/{venue_id}/auth?error=too_many_requests_mac&mac={mac}", status_code=302)

    # Генерация кода
    code = ''.join(random.choices(string.digits, k=4))
    expires_at = datetime.utcnow() + timedelta(minutes=5)

    # Сохраняем код в БД
    sms_code = SMSCode(phone_number=phone, code=code, expires_at=expires_at, venue_id=venue_id )
    db.add(sms_code)
    db.commit()

    # Отправка SMS (через адаптер)
    provider = get_sms_provider(db)
    if provider:
        adapter = SMSAdapter(provider)
        await adapter.send(phone, code, mac)
    else:
        print(f"SMS to {phone}: code={code}")

    # Перенаправляем на страницу ввода кода
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
    venue = db.get(Venue, venue_id)
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")

    template = db.query(PortalTemplate).filter(
        PortalTemplate.venue_id == venue_id,
        PortalTemplate.type == "auth",  # можно использовать отдельный тип "verify", но для простоты оставим auth
        PortalTemplate.is_active == True
    ).first()
    # fallback, если нет шаблона
    if not template:
        html = """
        <!DOCTYPE html>
        <html>
        <head><title>Подтверждение</title></head>
        <body>
            <h1>Введите код из SMS</h1>
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

    context = {
        "venue_name": venue.name,
        "phone": phone,
        "mac": mac,
        "error": request.query_params.get("error", ""),
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
    db: Session = Depends(get_db)
):
    """Проверка кода и редирект на welcome."""
    # Rate limiting по MAC для попыток ввода кода
    client_ip = request.client.host
    redis = await get_redis()
    key_attempt = f"rate:verify_mac:{mac}"
    attempts = await redis.incr(key_attempt)
    if attempts == 1:
        await redis.expire(key_attempt, 3600)  # 1 час
    if attempts > 10:
        await redis.setex(f"block:mac:{mac}", 300, "1")  # блокировка на 5 минут
        return RedirectResponse(url=f"/portal/{venue_id}/auth?error=blocked&mac={mac}", status_code=302)

    # Проверяем код в БД
    sms_code = db.query(SMSCode).filter(
        SMSCode.phone_number == phone,
        SMSCode.code == code,
        SMSCode.is_used == False,
        SMSCode.expires_at > datetime.utcnow()
    ).first()
    if not sms_code:
        # Неверный код
        return RedirectResponse(url=f"/portal/{venue_id}/verify?phone={phone}&mac={mac}&error=invalid_code", status_code=302)

    # Помечаем как использованный
    sms_code.is_used = True
    db.add(sms_code)

    # Создаём/обновляем профиль пользователя
    profile = db.query(UserProfile).filter(UserProfile.mac_address == mac).first()
    if not profile:
        profile = UserProfile(mac_address=mac, phone_number=phone, first_seen=datetime.utcnow())
        db.add(profile)
    else:
        profile.last_seen = datetime.utcnow()
        profile.phone_number = phone
    db.commit()
    db.refresh(profile)

    # Сохраняем в Redis авторизацию для RADIUS
    await redis.setex(f"auth:mac:{mac}", 28800, "1")

    # Редирект на приветственную страницу
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

    # Берём баннер для площадки (первый активный)
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