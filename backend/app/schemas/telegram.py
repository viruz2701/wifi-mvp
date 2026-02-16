from pydantic import BaseModel, validator
from app.core.validators import validate_phone_number, normalize_phone_number

class TelegramCallback(BaseModel):
    state: str
    phone: str
    chat_id: int

    @validator('phone')
    def validate_phone(cls, v):
        if not validate_phone_number(v):
            raise ValueError('Invalid phone number format')
        return normalize_phone_number(v)