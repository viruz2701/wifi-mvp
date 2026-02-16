from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import httpx
from sqlalchemy.orm import Session

from app.models.sms_provider import SMSProvider, SMSProviderType

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
                    print(f"RocketSMS error: {data.get('error')}")
                    return False
            except Exception as e:
                print(f"RocketSMS exception: {e}")
                return False

def get_sms_provider_by_type(db: Session, provider_type: SMSProviderType) -> Optional[SMSProvider]:
    """Возвращает активного провайдера указанного типа."""
    return db.query(SMSProvider).filter(
        SMSProvider.type == provider_type,
        SMSProvider.is_active == True
    ).first()

def get_active_sms_provider(db: Session) -> Optional[SMSProvider]:
    """Возвращает активного провайдера для SMS (тип rocketsms). Устаревшая функция, используйте get_sms_provider_by_type."""
    return get_sms_provider_by_type(db, SMSProviderType.ROCKETSMS)

def get_sms_adapter(provider: SMSProvider) -> SMSProviderBase:
    """Возвращает адаптер для данного провайдера."""
    if provider.type == SMSProviderType.ROCKETSMS:
        return RocketSMSAdapter(provider.config)
    elif provider.type == SMSProviderType.CALLPASSWORD:
        raise ValueError(f"Provider type {provider.type} does not support SMS sending")
    else:
        raise ValueError(f"Unknown provider type: {provider.type}")