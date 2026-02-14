from pydantic import BaseModel, Field
from typing import Optional

class SMSRequest(BaseModel):
    phone: str = Field(..., example="71234567890")
    mac: Optional[str] = Field(None, example="AA:BB:CC:DD:EE:FF")

class SMSVerify(BaseModel):
    phone: str
    code: str = Field(..., min_length=4, max_length=6)
    mac: str