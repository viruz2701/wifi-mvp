from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.db.session import get_db
from app.core.redis_client import get_redis
from app.core.social import get_social_adapter
from app.crud.social_action import social_action
from app.crud.venue_social_action import venue_social_action
from app.crud.user_social_action import user_social_action
from app.crud.user_profile import user_profile
from app.models.user_profile import UserProfile
from app.schemas.user_social_action import UserSocialActionCreate

router = APIRouter(prefix="/social", tags=["social"])

@router.post("/verify")
async def verify_social_action(
    action_id: int,
    network_user_id: str,
    mac: str,
    venue_id: int,
    db: Session = Depends(get_db)
):
    """Проверяет выполнение социального действия и выдаёт награду."""
    # Получаем действие
    action = social_action.get(db, id=action_id)
    if not action or not action.is_active:
        raise HTTPException(status_code=404, detail="Action not found or inactive")

    # Проверяем, доступно ли действие для данной площадки
    venue_action = db.query(venue_social_action.model).filter(
        venue_social_action.model.venue_id == venue_id,
        venue_social_action.model.action_id == action_id
    ).first()
    if not venue_action:
        raise HTTPException(status_code=400, detail="This action is not available for this venue")

    # Получаем профиль пользователя
    profile = db.query(UserProfile).filter(UserProfile.mac_address == mac).first()
    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found")

    # Проверяем, не выполнял ли пользователь уже это действие
    existing = user_social_action.get_by_user_and_action(db, profile.id, action_id)
    if existing:
        raise HTTPException(status_code=400, detail="Action already completed")

    # Проверяем через адаптер
    adapter = get_social_adapter(action)
    verified = await adapter.verify(network_user_id)
    if not verified:
        raise HTTPException(status_code=400, detail="Action verification failed")

    # Выдаём награду
    tariff_id = venue_action.reward_tariff_id
    expires_at = None
    if tariff_id and venue_action.reward_duration_hours:
        expires_at = datetime.utcnow() + timedelta(hours=venue_action.reward_duration_hours)
        # Обновляем профиль с новым тарифом
        profile.current_tariff_id = tariff_id
        profile.tariff_expires_at = expires_at
        db.add(profile)

    # Сохраняем выполнение
    user_action = UserSocialActionCreate(
        user_profile_id=profile.id,
        action_id=action_id,
        reward_tariff_id=tariff_id,
        expires_at=expires_at
    )
    user_social_action.create(db, obj_in=user_action)

    # Сохраняем в Redis для быстрого доступа (если нужно)
    redis = await get_redis()
    await redis.setex(f"auth:mac:{mac}", 28800, "1")

    return {
        "success": True,
        "tariff_id": tariff_id,
        "expires_at": expires_at.isoformat() if expires_at else None
    }