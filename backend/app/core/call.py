from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import httpx
import hashlib
import hmac
import time
import json
from app.models.sms_provider import SMSProvider, SMSProviderType

class CallProviderBase(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @abstractmethod
    async def initiate_call(self, phone: str, user_data: str, callback_url: str) -> Dict[str, Any]:
        """Инициирует звонок и возвращает данные для отображения пользователю (номер для звонка, QR-код и т.д.)"""
        pass

class CallPasswordAdapter(CallProviderBase):
    """Адаптер для сервиса CallPassword от New-Tel"""
    
    BASE_URL = "https://api.new-tel.net"
    
    def _generate_auth_token(self, timestamp: int) -> str:
        """Генерирует Bearer токен согласно документации"""
        # Формируем строку для подписи
        api_key = self.config.get("api_key")
        api_secret = self.config.get("api_secret")
        
        # Согласно документации, токен включает ключ, timestamp и SHA-256 подпись
        # Точный формат нужно уточнить, но предположим:
        message = f"{api_key}{timestamp}"
        signature = hmac.new(
            api_secret.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return f"{api_key}.{timestamp}.{signature}"
    
    async def initiate_call(self, phone: str, user_data: str, callback_url: str) -> Dict[str, Any]:
        timestamp = int(time.time())
        token = self._generate_auth_token(timestamp)
        
        url = f"{self.BASE_URL}/call-password-id/start-waiting-mode-busy"
        
        payload = {
            "callbackLink": callback_url,
            "clientNumber": phone,
            "timeout": self.config.get("timeout", 60),
            "userData": user_data
        }
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            
            # Ожидаем, что API вернет объект callDetails
            # Из документации: возвращает callId, confirmationNumber, qrCodeUri
            return {
                "call_id": data.get("callDetails", {}).get("callId"),
                "confirmation_number": data.get("callDetails", {}).get("confirmationNumber"),
                "qr_code_uri": data.get("callDetails", {}).get("qrCodeUri"),
                "raw_response": data
            }

def get_call_provider(provider: SMSProvider) -> CallProviderBase:
    """Фабрика для получения адаптера звонков по типу провайдера"""
    if provider.type == SMSProviderType.CALLPASSWORD:
        return CallPasswordAdapter(provider.config)
    else:
        raise ValueError(f"Provider {provider.type} does not support calls")