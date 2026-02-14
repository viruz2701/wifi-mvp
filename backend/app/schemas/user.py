from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    role: str = "admin"
    venue_id: Optional[int] = None

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: int
    hashed_password: str
    created_at: datetime

    class Config:
        from_attributes = True

class UserOut(UserBase):
    id: int
    created_at: datetime