from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserSocialActionBase(BaseModel):
    user_profile_id: int
    action_id: int
    reward_tariff_id: Optional[int] = None
    expires_at: Optional[datetime] = None

class UserSocialActionCreate(UserSocialActionBase):
    pass

class UserSocialActionUpdate(BaseModel):
    expires_at: Optional[datetime] = None

class UserSocialActionOut(UserSocialActionBase):
    id: int
    completed_at: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True