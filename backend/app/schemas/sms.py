from pydantic import BaseModel, Field, validator
from typing import Optional
from app.core.validators import validate_phone_number, normalize_phone_number

class SMSRequest(BaseModel):
    phone: str = Field(..., example="375291234567")
    mac: Optional[str] = Field(None, example="AA:BB:CC:DD:EE:FF")
    venue_id: Optional[int] = Field(None, example=1)

    @validator('phone')
    def validate_phone(cls, v):
        if not validate_phone_number(v):
            raise ValueError('Invalid phone number format. Expected international format (e.g., 375291234567 or +375291234567)')
        return normalize_phone_number(v)

class SMSVerify(BaseModel):
    phone: str
    code: str = Field(..., min_length=4, max_length=6)
    mac: str

    @validator('phone')
    def validate_phone(cls, v):
        if not validate_phone_number(v):
            raise ValueError('Invalid phone number format')
        return normalize_phone_number(v)