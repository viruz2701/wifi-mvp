import random
import string
import logging
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
import httpx

from app.db.session import get_db
from app.models.venue import Venue
from app.models.portal_template import PortalTemplate
from app.models.user_profile import UserProfile
from app.models.sms_code import SMSCode
from app.models.nas_device import NASDevice, NASDeviceType
from app.core.redis_client import get_redis
from app.nas import get_nas_instance
from app.core.sms import send_sms_with_fallback

logger = logging.getLogger(__name__)

router = APIRouter()

def render_template(html: str, context: dict) -> str:
    import re
    def replace(match):
        key = match.group(1)
        return str(context.get(key, f"$({key})"))
    return re.sub(r'\$\((\w+)\)', replace, html)

@router.get("/opennds", response_class=HTMLResponse)
async def opennds_auth_page(
    request: Request,
    clientip: str = None,
    gatewayname: str = None,
    tok: str = None,
    redir: str = None,
    db: Session = Depends(get_db)
):
    """Страница авторизации для OpenNDS FAS."""
    # Определяем площадку по gatewayname (это может быть домен или IP роутера)
    venue = db.query(Venue).filter(Venue.domain == gatewayname).first()
    if not venue:
        # Если не нашли по домену, пробуем найти NAS с таким IP
        nas = db.query(NASDevice).filter(NASDevice.ip_address == gatewayname).first()
        if nas:
            venue = db.get(Venue, nas.venue_id)
    if not venue:
        return HTMLResponse("Invalid gateway", status_code=404)

    # Сохраняем данные сессии в Redis
    redis = await get_redis()
    session_key = f"opennds:session:{tok}"
    await redis.setex(session_key, 300, f"{clientip}:{gatewayname}")

    template = db.query(PortalTemplate).filter(
        PortalTemplate.venue_id == venue.id,
        PortalTemplate.type == "auth",
        PortalTemplate.is_active == True
    ).first()
    if not template:
        html = """
        <!DOCTYPE html>
        <html>
        <head><title>Авторизация</title></head>
        <body>
            <h1>Добро пожаловать в Wi-Fi</h1>
            <form method="post" action="/api/v1/portal/opennds/auth">
                <input type="hidden" name="tok" value="{tok}">
                <input type="hidden" name="clientip" value="{clientip}">
                <input type="text" name="phone" placeholder="Номер телефона">
                <button type="submit">Получить код</button>
            </form>
        </body>
        </html>
        """
    else:
        html = template.html_content

    context = {
        "venue_name": venue.name,
        "clientip": clientip,
        "tok": tok,
        "redir": redir,
        "gatewayname": gatewayname,
        "error": request.query_params.get("error", "")
    }
    return render_template(html, context)

@router.post("/opennds/auth")
async def opennds_auth_request(
    request: Request,
    tok: str = Form(...),
    clientip: str = Form(...),
    phone: str = Form(...),
    db: Session = Depends(get_db)
):
    """Отправка кода по SMS."""
    redis = await get_redis()
    session_key = f"opennds:session:{tok}"
    session_data = await redis.get(session_key)
    if not session_data:
        return HTMLResponse("Session expired", status_code=400)

    # Генерация кода
    code = ''.join(random.choices(string.digits, k=4))
    expires_at = datetime.utcnow() + timedelta(minutes=5)

    sms_code = SMSCode(
        phone_number=phone,
        code=code,
        expires_at=expires_at
        # venue_id можно определить позже
    )
    db.add(sms_code)
    db.commit()

    success = await send_sms_with_fallback(db, phone, code)
    if not success:
        logger.warning(f"No SMS provider available for {phone}, code={code}")
    else:
        logger.info(f"SMS sent to {phone}, code={code}")

    return RedirectResponse(url=f"/api/v1/portal/opennds/verify?tok={tok}&phone={phone}", status_code=302)

@router.get("/opennds/verify", response_class=HTMLResponse)
async def opennds_verify_page(
    request: Request,
    tok: str,
    phone: str,
    db: Session = Depends(get_db)
):
    """Страница ввода кода."""
    html = """
    <!DOCTYPE html>
    <html>
    <head><title>Подтверждение</title></head>
    <body>
        <h1>Введите код из SMS</h1>
        <form method="post" action="/api/v1/portal/opennds/verify">
            <input type="hidden" name="tok" value="{tok}">
            <input type="hidden" name="phone" value="{phone}">
            <input type="text" name="code" placeholder="Код">
            <button type="submit">Подтвердить</button>
        </form>
    </body>
    </html>
    """
    context = {"tok": tok, "phone": phone, "error": request.query_params.get("error", "")}
    return render_template(html, context)

@router.post("/opennds/verify")
async def opennds_verify(
    request: Request,
    tok: str = Form(...),
    phone: str = Form(...),
    code: str = Form(...),
    db: Session = Depends(get_db)
):
    """Проверка кода и активация доступа."""
    # Проверка кода
    sms_code = db.query(SMSCode).filter(
        SMSCode.phone_number == phone,
        SMSCode.code == code,
        SMSCode.is_used == False,
        SMSCode.expires_at > datetime.utcnow()
    ).first()
    if not sms_code:
        return RedirectResponse(url=f"/api/v1/portal/opennds/verify?tok={tok}&phone={phone}&error=invalid_code", status_code=302)

    sms_code.is_used = True
    db.add(sms_code)

    # Получаем данные сессии
    redis = await get_redis()
    session_key = f"opennds:session:{tok}"
    session_data = await redis.get(session_key)
    if not session_data:
        return HTMLResponse("Session expired", status_code=400)
    clientip, gatewayname = session_data.decode().split(":")

    # Находим NAS-устройство
    nas = db.query(NASDevice).filter(NASDevice.ip_address == gatewayname).first()
    if not nas:
        return HTMLResponse("NAS device not found", status_code=404)

    # Создаём профиль пользователя (без MAC)
    profile = UserProfile(
        mac_address="00:00:00:00:00:00",  # заглушка
        phone_number=phone,
        first_seen=datetime.utcnow(),
        venue_id=nas.venue_id
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)

    # Активируем доступ
    nas_instance = get_nas_instance(nas)
    if hasattr(nas_instance, 'authorize_client'):
        success = await nas_instance.authorize_client(clientip, tok)
    else:
        # fallback HTTP-запрос
        async with httpx.AsyncClient() as client:
            url = f"http://{nas.ip_address}/opennds_auth/?tok={tok}"
            resp = await client.get(url)
            success = resp.status_code == 200

    if not success:
        return HTMLResponse("Failed to authorize", status_code=500)

    # Очищаем сессию
    await redis.delete(session_key)

    return RedirectResponse(url=f"/api/v1/portal/opennds/welcome?tok={tok}", status_code=302)

@router.get("/opennds/welcome", response_class=HTMLResponse)
async def opennds_welcome(tok: str):
    """Страница приветствия."""
    html = """
    <!DOCTYPE html>
    <html>
    <head><title>Добро пожаловать</title></head>
    <body>
        <h1>Вы успешно авторизованы!</h1>
        <p>Теперь вы можете пользоваться интернетом.</p>
    </body>
    </html>
    """
    return HTMLResponse(html)