from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.social_action import social_action
from app.crud.venue_social_action import venue_social_action
from app.schemas.social_action import SocialActionCreate, SocialActionUpdate, SocialActionOut
from app.schemas.venue_social_action import VenueSocialActionCreate, VenueSocialActionUpdate, VenueSocialActionOut
from app.core.dependencies import get_current_superuser, get_current_venue_owner_or_admin
from app.models.user import User
from app.models.social_action import SocialActionType, SocialNetwork

router = APIRouter(prefix="/social", tags=["social"])

# ---------- Социальные действия (только для админа) ----------
@router.get("/types", response_model=List[str])
def get_action_types():
    return [t.value for t in SocialActionType]

@router.get("/networks", response_model=List[str])
def get_networks():
    return [n.value for n in SocialNetwork]

@router.get("/actions", response_model=List[SocialActionOut])
def read_actions(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_superuser),
):
    return social_action.get_multi(db, skip=skip, limit=limit)

@router.post("/actions", response_model=SocialActionOut)
def create_action(
    action_in: SocialActionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
):
    return social_action.create(db, obj_in=action_in)

@router.get("/actions/{id}", response_model=SocialActionOut)
def read_action(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
):
    action = social_action.get(db, id=id)
    if not action:
        raise HTTPException(status_code=404, detail="Action not found")
    return action

@router.put("/actions/{id}", response_model=SocialActionOut)
def update_action(
    id: int,
    action_in: SocialActionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
):
    action = social_action.get(db, id=id)
    if not action:
        raise HTTPException(status_code=404, detail="Action not found")
    return social_action.update(db, db_obj=action, obj_in=action_in)

@router.delete("/actions/{id}", response_model=SocialActionOut)
def delete_action(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
):
    action = social_action.remove(db, id=id)
    if not action:
        raise HTTPException(status_code=404, detail="Action not found")
    return action

# ---------- Привязка действий к площадке (доступно владельцу площадки) ----------
@router.get("/venue/{venue_id}/actions", response_model=List[VenueSocialActionOut])
def read_venue_actions(
    venue_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_venue_owner_or_admin),
):
    # Проверка прав: пользователь должен иметь доступ к этой площадке
    if current_user.role == "venue_owner" and current_user.venue_id != venue_id:
        raise HTTPException(status_code=403, detail="Access denied")
    return venue_social_action.get_by_venue(db, venue_id)

@router.post("/venue/{venue_id}/actions", response_model=VenueSocialActionOut)
def add_venue_action(
    venue_id: int,
    action_in: VenueSocialActionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_venue_owner_or_admin),
):
    if action_in.venue_id != venue_id:
        raise HTTPException(status_code=400, detail="venue_id mismatch")
    if current_user.role == "venue_owner" and current_user.venue_id != venue_id:
        raise HTTPException(status_code=403, detail="Access denied")
    # Проверить существование action
    action = social_action.get(db, id=action_in.action_id)
    if not action:
        raise HTTPException(status_code=404, detail="Action not found")
    return venue_social_action.create(db, obj_in=action_in)

@router.put("/venue/actions/{id}", response_model=VenueSocialActionOut)
def update_venue_action(
    id: int,
    action_in: VenueSocialActionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_venue_owner_or_admin),
):
    venue_action = venue_social_action.get(db, id=id)
    if not venue_action:
        raise HTTPException(status_code=404, detail="Venue action not found")
    # Проверка прав
    if current_user.role == "venue_owner" and current_user.venue_id != venue_action.venue_id:
        raise HTTPException(status_code=403, detail="Access denied")
    return venue_social_action.update(db, db_obj=venue_action, obj_in=action_in)

@router.delete("/venue/actions/{id}", response_model=VenueSocialActionOut)
def delete_venue_action(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_venue_owner_or_admin),
):
    venue_action = venue_social_action.get(db, id=id)
    if not venue_action:
        raise HTTPException(status_code=404, detail="Venue action not found")
    if current_user.role == "venue_owner" and current_user.venue_id != venue_action.venue_id:
        raise HTTPException(status_code=403, detail="Access denied")
    return venue_social_action.remove(db, id=id)