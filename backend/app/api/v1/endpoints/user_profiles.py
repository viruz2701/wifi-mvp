from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.user_profile import user_profile
from app.schemas.user_profile import UserProfileCreate, UserProfileUpdate, UserProfileOut
from app.core.dependencies import get_current_superuser, get_current_active_user
from app.models.user import User
from app.models.user_profile import UserProfile

router = APIRouter()

@router.get("", response_model=List[UserProfileOut])
def read_profiles(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    venue_id: Optional[int] = Query(None),
    mac: Optional[str] = Query(None),
    phone: Optional[str] = Query(None),
    is_blocked: Optional[bool] = Query(None),
    current_user: User = Depends(get_current_active_user),
):
    query = db.query(UserProfile)
    if venue_id:
        query = query.filter(UserProfile.venue_id == venue_id)
    if mac:
        query = query.filter(UserProfile.mac_address.ilike(f"%{mac}%"))
    if phone:
        query = query.filter(UserProfile.phone_number == phone)
    if is_blocked is not None:
        query = query.filter(UserProfile.is_blocked == is_blocked)
    return query.offset(skip).limit(limit).all()

@router.get("/", response_model=List[UserProfileOut])
def read_profiles_with_slash(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    venue_id: Optional[int] = Query(None),
    mac: Optional[str] = Query(None),
    phone: Optional[str] = Query(None),
    is_blocked: Optional[bool] = Query(None),
    current_user: User = Depends(get_current_active_user),
):
    query = db.query(UserProfile)
    if venue_id:
        query = query.filter(UserProfile.venue_id == venue_id)
    if mac:
        query = query.filter(UserProfile.mac_address.ilike(f"%{mac}%"))
    if phone:
        query = query.filter(UserProfile.phone_number == phone)
    if is_blocked is not None:
        query = query.filter(UserProfile.is_blocked == is_blocked)
    return query.offset(skip).limit(limit).all()

@router.post("/", response_model=UserProfileOut)
def create_profile(
    profile_in: UserProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
):
    return user_profile.create(db, obj_in=profile_in)

@router.get("/{id}", response_model=UserProfileOut)
def read_profile(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    profile = user_profile.get(db, id=id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.put("/{id}", response_model=UserProfileOut)
def update_profile(
    id: int,
    profile_in: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
):
    profile = user_profile.get(db, id=id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return user_profile.update(db, db_obj=profile, obj_in=profile_in)

@router.delete("/{id}", response_model=UserProfileOut)
def delete_profile(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
):
    profile = user_profile.remove(db, id=id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile
