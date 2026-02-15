from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import shutil
from pathlib import Path
from app.db.session import get_db
from app.crud.banner import banner as crud_banner
from app.crud.venue import venue as crud_venue
from app.schemas.banner import BannerCreate, BannerUpdate, BannerOut
from app.core.dependencies import get_current_superuser, get_current_active_user
from app.models.user import User
from app.tasks.banner import increment_clicks
from app.models.banner import Banner  # <-- добавлен импорт модели

router = APIRouter()

UPLOAD_DIR = Path("/app/static/banners")

# GET /banners (без слеша)
@router.get("", response_model=List[BannerOut])
def read_banners(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    venue_id: int = Query(..., description="ID площадки"),
    current_user: User = Depends(get_current_active_user),
):
    """Список баннеров для площадки"""
    banners = db.query(Banner).filter(
        Banner.venue_id == venue_id,
        Banner.deleted_at.is_(None)
    ).offset(skip).limit(limit).all()
    return banners

# GET /banners/ (со слешем) – для обратной совместимости
@router.get("/", response_model=List[BannerOut])
def read_banners_with_slash(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    venue_id: int = Query(..., description="ID площадки"),
    current_user: User = Depends(get_current_active_user),
):
    banners = db.query(Banner).filter(
        Banner.venue_id == venue_id,
        Banner.deleted_at.is_(None)
    ).offset(skip).limit(limit).all()
    return banners

# POST /banners/ (со слешем) – создание баннера
@router.post("/", response_model=BannerOut)
def create_banner(
    banner_in: BannerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
):
    """Создать баннер (изображение загружается отдельно)"""
    venue = crud_venue.get(db, id=banner_in.venue_id)
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")
    return crud_banner.create(db, obj_in=banner_in)

# POST /banners (без слеша) – создание баннера (для совместимости)
@router.post("", response_model=BannerOut)
def create_banner_without_slash(
    banner_in: BannerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
):
    return create_banner(banner_in, db, current_user)

# POST /banners/{id}/upload – загрузка изображения
@router.post("/{id}/upload")
async def upload_banner_image(
    id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
):
    banner = crud_banner.get(db, id=id)
    if not banner:
        raise HTTPException(status_code=404, detail="Banner not found")
    dest_dir = UPLOAD_DIR / str(banner.venue_id)
    dest_dir.mkdir(parents=True, exist_ok=True)
    filename = file.filename.replace(" ", "_")
    file_path = dest_dir / filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    image_url = f"/static/banners/{banner.venue_id}/{filename}"
    crud_banner.update(db, db_obj=banner, obj_in={"image_url": image_url})
    return {"message": "Image uploaded", "image_url": image_url}

# GET /banners/{id} – получение баннера по ID
@router.get("/{id}", response_model=BannerOut)
def read_banner(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    banner = crud_banner.get(db, id=id)
    if not banner:
        raise HTTPException(status_code=404, detail="Banner not found")
    return banner

# PUT /banners/{id} – обновление баннера
@router.put("/{id}", response_model=BannerOut)
def update_banner(
    id: int,
    banner_in: BannerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
):
    banner = crud_banner.get(db, id=id)
    if not banner:
        raise HTTPException(status_code=404, detail="Banner not found")
    return crud_banner.update(db, db_obj=banner, obj_in=banner_in)

# DELETE /banners/{id} – удаление баннера
@router.delete("/{id}", response_model=BannerOut)
def delete_banner(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
):
    banner = crud_banner.remove(db, id=id)
    if not banner:
        raise HTTPException(status_code=404, detail="Banner not found")
    return banner

# GET /banners/{id}/click – редирект и учёт клика
@router.get("/{id}/click")
async def click_banner(
    id: int,
    db: Session = Depends(get_db),
):
    banner = crud_banner.get(db, id=id)
    if not banner:
        raise HTTPException(status_code=404, detail="Banner not found")
    increment_clicks.delay(id)
    return RedirectResponse(url=banner.target_url)