from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import httpx
import logging
import asyncio
from sqlalchemy.orm import Session

from app.models.sms_provider import SMSProvider, SMSProviderType

logger = logging.getLogger(__name__)

class SMSProviderBase(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @abstractmethod
    async def send(self, phone: str, message: str) -> bool:
        pass

class RocketSMSAdapter(SMSProviderBase):
    async def send(self, phone: str, message: str) -> bool:
        username = self.config.get("username")
        password_md5 = self.config.get("password_md5")
        sender = self.config.get("sender")
        url = "https://api.rocketsms.by/simple/send"
        params = {
            "username": username,
            "password": password_md5,
            "phone": phone,
            "text": message,
            "sender": sender,
            "priority": "true"
        }
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(url, params=params)
                resp.raise_for_status()
                data = resp.json()
                if "id" in data:
                    return True
                else:
                    logger.error(f"RocketSMS error: {data.get('error')}")
                    return False
            except Exception as e:
                logger.exception(f"RocketSMS exception: {e}")
                return False

class WebSmsAdapter(SMSProviderBase):
    """Адаптер для WebSMS.by (https://cabinet.websms.by/public/client/apidoc/)"""
    
    # Общий семафор для ограничения 5 запросов в секунду (на все экземпляры)
    _semaphore = asyncio.Semaphore(5)
    
    async def send(self, phone: str, message: str) -> bool:
        # Ожидаем доступный слот
        async with self._semaphore:
            # Минимальный интервал 0.2 сек
            await asyncio.sleep(0.2)
            
            user = self.config.get("user")
            apikey = self.config.get("apikey")
            sender = self.config.get("sender")  # опционально
            
            # Убираем '+' из номера, если есть
            clean_phone = phone.replace("+", "")
            
            params = {
                "user": user,
                "apikey": apikey,
                "phone": clean_phone,
                "text": message,
            }
            if sender:
                params["sender"] = sender
            
            url = "https://cabinet.websms.by/api/send/sms"
            
            async with httpx.AsyncClient() as client:
                try:
                    resp = await client.get(url, params=params, timeout=10)
                    resp.raise_for_status()
                    data = resp.json()
                    
                    # Успех: status == true
                    if data.get("status") is True:
                        logger.info(f"WebSMS: SMS sent to {phone}, id={data.get('id')}")
                        return True
                    else:
                        error_code = data.get("code")
                        error_msg = data.get("message", "Unknown error")
                        logger.error(f"WebSMS error {error_code}: {error_msg}")
                        return False
                except httpx.HTTPStatusError as e:
                    logger.error(f"WebSMS HTTP error: {e.response.status_code} {e.response.text}")
                    return False
                except Exception as e:
                    logger.exception(f"WebSMS unexpected error: {e}")
                    return False

def get_sms_adapter(provider: SMSProvider) -> SMSProviderBase:
    """Возвращает адаптер для данного провайдера."""
    if provider.type == SMSProviderType.ROCKETSMS:
        return RocketSMSAdapter(provider.config)
    elif provider.type == SMSProviderType.CALLPASSWORD:
        raise ValueError(f"Provider type {provider.type} does not support SMS sending")
    elif provider.type == SMSProviderType.WEBSMS:
        return WebSmsAdapter(provider.config)
    else:
        raise ValueError(f"Unknown provider type: {provider.type}")

def get_active_sms_providers(db: Session) -> List[SMSProvider]:
    """Возвращает всех активных SMS-провайдеров, отсортированных по приоритету (меньше = выше)."""
    return db.query(SMSProvider).filter(
        SMSProvider.is_active == True,
        SMSProvider.type != SMSProviderType.CALLPASSWORD  # исключаем типы, не умеющие отправлять SMS
    ).order_by(SMSProvider.priority.asc()).all()

async def send_sms_with_fallback(db: Session, phone: str, message: str) -> bool:
    """
    Пытается отправить SMS через всех активных провайдеров по очереди.
    Возвращает True, если хотя бы одна отправка успешна.
    """
    providers = get_active_sms_providers(db)
    if not providers:
        logger.error("No active SMS providers available")
        return False

    for provider in providers:
        try:
            adapter = get_sms_adapter(provider)
            success = await adapter.send(phone, message)
            if success:
                logger.info(f"SMS sent via {provider.name} (type={provider.type})")
                return True
            else:
                logger.warning(f"SMS sending failed via {provider.name}, trying next...")
        except Exception as e:
            logger.exception(f"Error with provider {provider.name}: {e}")
            continue

    logger.error("All SMS providers failed")
    return False