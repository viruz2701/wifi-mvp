from celery import shared_task
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user_profile import UserProfile
from app.models.venue import Venue
from app.core.crm import get_active_crm_providers, get_crm_adapter
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_to_crm(user_profile_id: int):
    """Отправляет данные конкретного пользователя во все активные CRM-провайдеры."""
    db = SessionLocal()
    try:
        profile = db.get(UserProfile, user_profile_id)
        if not profile:
            logger.error(f"UserProfile {user_profile_id} not found")
            return

        # Определяем, нужно ли отправлять для площадки
        if profile.venue_id:
            venue = db.get(Venue, profile.venue_id)
            if not venue or not venue.crm_enabled:
                logger.info(f"CRM disabled for venue {profile.venue_id}")
                return

        providers = get_active_crm_providers(db)
        if not providers:
            logger.info("No active CRM providers")
            return

        # Формируем данные для отправки
        data = {
            "phone": profile.phone_number,
            "email": profile.email,
            "full_name": profile.full_name,
            "marketing_consent": profile.marketing_consent,
            "first_seen": profile.first_seen.isoformat() if profile.first_seen else None,
            "mac": profile.mac_address,
        }

        for provider in providers:
            try:
                adapter = get_crm_adapter(provider)
                # Запускаем асинхронно? Но Celery задача синхронная, поэтому используем asyncio.run
                import asyncio
                success = asyncio.run(adapter.send_contact(data))
                if success:
                    logger.info(f"Sent to CRM {provider.name} (profile {user_profile_id})")
                else:
                    logger.warning(f"Failed to send to CRM {provider.name}")
            except Exception as e:
                logger.exception(f"Error sending to CRM {provider.name}: {e}")
    finally:
        db.close()

@shared_task
def bulk_export_to_crm(venue_id: int = None, from_date: str = None, to_date: str = None):
    """Массовая отправка всех подходящих профилей в CRM."""
    db = SessionLocal()
    try:
        query = db.query(UserProfile).filter(UserProfile.deleted_at.is_(None))
        if venue_id:
            query = query.filter(UserProfile.venue_id == venue_id)
        if from_date:
            query = query.filter(UserProfile.first_seen >= datetime.fromisoformat(from_date))
        if to_date:
            query = query.filter(UserProfile.first_seen <= datetime.fromisoformat(to_date))

        profiles = query.all()
        for profile in profiles:
            send_to_crm.delay(profile.id)  # запускаем отдельные задачи
    finally:
        db.close()