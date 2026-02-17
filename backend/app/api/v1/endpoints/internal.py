from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.setting import setting as crud_setting

router = APIRouter()

def is_internal_request(request: Request) -> bool:
    client_host = request.client.host
    # Разрешаем запросы из внутренней сети Docker (172.x.x.x) и localhost
    allowed_networks = ["172.", "127.0.0.1", "::1"]
    return any(client_host.startswith(net) for net in allowed_networks)

@router.get("/internal/telegram-settings")
async def get_telegram_settings(request: Request, db: Session = Depends(get_db)):
    if not is_internal_request(request):
        raise HTTPException(status_code=403, detail="Forbidden")
    # Ключи, которые нужны боту
    keys = ["telegram_bot_token", "telegram_bot_username", "telegram_bot_webhook_url"]
    settings = {}
    for key in keys:
        setting = crud_setting.get_by_key(db, key=key)
        settings[key] = setting.value if setting else None
    return settings