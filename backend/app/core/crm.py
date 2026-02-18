from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import httpx
import logging
from sqlalchemy.orm import Session

from app.models.crm_provider import CRMProvider, CRMProviderType

logger = logging.getLogger(__name__)

class CRMProviderBase(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @abstractmethod
    async def send_contact(self, data: Dict[str, Any]) -> bool:
        """Отправляет контактные данные в CRM."""
        pass

class Bitrix24Adapter(CRMProviderBase):
    async def send_contact(self, data: Dict[str, Any]) -> bool:
        webhook_url = self.config.get("webhook_url")
        if not webhook_url:
            logger.error("Bitrix24: webhook_url not configured")
            return False

        entity_type = self.config.get("entity_type", "CONTACT")
        field_mapping = self.config.get("field_mapping", {})

        # Преобразуем поля согласно маппингу
        mapped_data = {}
        for our_field, crm_field in field_mapping.items():
            if our_field in data:
                mapped_data[crm_field] = data[our_field]

        # Обязательные поля для контакта Bitrix24
        if "NAME" not in mapped_data and "full_name" in data:
            mapped_data["NAME"] = data["full_name"]
        if "PHONE" not in mapped_data and "phone" in data:
            mapped_data["PHONE"] = [{"VALUE": data["phone"], "VALUE_TYPE": "WORK"}]
        if "EMAIL" not in mapped_data and "email" in data:
            mapped_data["EMAIL"] = [{"VALUE": data["email"], "VALUE_TYPE": "WORK"}]

        # Если маркетинговое согласие, можно добавить в UF или заметку
        if data.get("marketing_consent"):
            mapped_data["COMMENTS"] = "Согласие на рекламу получено"

        url = f"{webhook_url}crm.contact.add.json"
        payload = {"fields": mapped_data, "params": {"REGISTER_SONET_EVENT": "Y"}}

        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(url, json=payload, timeout=10)
                resp.raise_for_status()
                result = resp.json()
                if result.get("result"):
                    logger.info(f"Bitrix24: contact added, ID={result['result']}")
                    return True
                else:
                    logger.error(f"Bitrix24 error: {result}")
                    return False
            except Exception as e:
                logger.exception(f"Bitrix24 exception: {e}")
                return False

def get_crm_adapter(provider: CRMProvider) -> CRMProviderBase:
    if provider.type == CRMProviderType.BITRIX24:
        return Bitrix24Adapter(provider.config)
    else:
        raise ValueError(f"Unknown CRM provider type: {provider.type}")

def get_active_crm_providers(db: Session) -> List[CRMProvider]:
    """Возвращает все активные CRM-провайдеры, отсортированные по приоритету."""
    return db.query(CRMProvider).filter(
        CRMProvider.is_active == True,
        CRMProvider.deleted_at.is_(None)
    ).order_by(CRMProvider.priority.asc()).all()