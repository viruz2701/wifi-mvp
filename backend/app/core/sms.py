from app.models.sms_provider import SMSProvider
from sqlalchemy.orm import Session
import httpx

class SMSAdapter:
    def __init__(self, provider: SMSProvider):
        self.provider = provider

    async def send(self, phone: str, code: str, mac: str = None) -> bool:
        # Заглушка – реальная интеграция с RocketSMS
        print(f"Sending SMS to {phone}: code={code}")
        return True

def get_sms_provider(db: Session) -> SMSProvider | None:
    return db.query(SMSProvider).filter(SMSProvider.is_active == True).first()