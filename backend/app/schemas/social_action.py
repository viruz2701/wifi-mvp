from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional, Any, Dict
from app.models.social_action import SocialActionType, SocialNetwork

class SocialActionBase(BaseModel):
    name: str
    description: Optional[str] = None
    type: SocialActionType
    network: SocialNetwork
    config: Dict[str, Any] = {}
    is_active: bool = True

    # Валидаторы для приведения к нижнему регистру (Pydantic v2)
    @field_validator('type', mode='before')
    @classmethod
    def validate_type(cls, v: Any) -> Any:
        if isinstance(v, str):
            return v.lower()
        return v

    @field_validator('network', mode='before')
    @classmethod
    def validate_network(cls, v: Any) -> Any:
        if isinstance(v, str):
            return v.lower()
        return v

class SocialActionCreate(SocialActionBase):
    pass

class SocialActionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[SocialActionType] = None
    network: Optional[SocialNetwork] = None
    config: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

    @field_validator('type', mode='before')
    @classmethod
    def validate_type(cls, v: Any) -> Any:
        if v is not None and isinstance(v, str):
            return v.lower()
        return v

    @field_validator('network', mode='before')
    @classmethod
    def validate_network(cls, v: Any) -> Any:
        if v is not None and isinstance(v, str):
            return v.lower()
        return v

class SocialActionOut(SocialActionBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True