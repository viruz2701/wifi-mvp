from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
import os
import shutil
from pathlib import Path
from app.db.session import get_db
from app.crud.portal_template import portal_template as crud_template
from app.crud.venue import venue as crud_venue
from app.schemas.portal_template import PortalTemplateCreate, PortalTemplateUpdate, PortalTemplateOut
from app.core.dependencies import get_current_superuser

router = APIRouter()

UPLOAD_DIR = Path("/app/static/uploads")  # внутри контейнера

@router.get("/", response_model=List[PortalTemplateOut])
def read_templates(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user = Depends(get_current_superuser),
):
    return crud_template.get_multi(db, skip=skip, limit=limit)

@router.post("/", response_model=PortalTemplateOut)
def create_template(
    template_in: PortalTemplateCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    # Проверяем, существует ли площадка
    venue = crud_venue.get(db, id=template_in.venue_id)
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")
    return crud_template.create(db, obj_in=template_in)

@router.post("/{id}/upload")
async def upload_template_file(
    id: int,
    file_type: str = Query(..., regex="^(css|js|image)$"),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    """Загрузка CSS, JS или изображения для шаблона."""
    template = crud_template.get(db, id=id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    # Определяем подпапку
    subfolder = file_type  # css, js, images
    dest_dir = UPLOAD_DIR / str(template.venue_id) / subfolder
    dest_dir.mkdir(parents=True, exist_ok=True)

    # Генерируем безопасное имя файла
    filename = file.filename.replace(" ", "_")
    file_path = dest_dir / filename

    # Сохраняем файл
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Обновляем список файлов в шаблоне
    update_data = {}
    if file_type == "css":
        update_data["css_files"] = template.css_files + [f"/static/{template.venue_id}/{subfolder}/{filename}"]
    elif file_type == "js":
        update_data["js_files"] = template.js_files + [f"/static/{template.venue_id}/{subfolder}/{filename}"]
    else:  # image
        update_data["images"] = template.images + [f"/static/{template.venue_id}/{subfolder}/{filename}"]

    crud_template.update(db, db_obj=template, obj_in=update_data)
    return {"message": "File uploaded", "path": update_data}

@router.get("/{id}", response_model=PortalTemplateOut)
def read_template(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    template = crud_template.get(db, id=id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template

@router.put("/{id}", response_model=PortalTemplateOut)
def update_template(
    id: int,
    template_in: PortalTemplateUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    template = crud_template.get(db, id=id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return crud_template.update(db, db_obj=template, obj_in=template_in)

@router.delete("/{id}", response_model=PortalTemplateOut)
def delete_template(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    template = crud_template.remove(db, id=id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template
import os
from pathlib import Path

@router.delete("/{id}/files")
async def delete_template_file(
    id: int,
    file_path: str = Query(..., description="Полный путь к файлу (например, /static/1/css/style.css)"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    """Удалить загруженный файл (CSS, JS или изображение) и убрать его из списков шаблона."""
    template = crud_template.get(db, id=id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    # Преобразуем /static/... в локальный путь внутри контейнера
    # Например, /static/1/css/style.css -> /app/static/1/css/style.css
    local_path = file_path.replace("/static", "/app/static")
    full_path = Path(local_path)

    if not full_path.exists():
        raise HTTPException(status_code=404, detail="File not found on disk")

    # Удаляем файл
    os.remove(full_path)

    # Убираем путь из соответствующего списка в модели
    update_data = {}
    if "css" in file_path:
        new_list = [p for p in template.css_files if p != file_path]
        update_data["css_files"] = new_list
    elif "js" in file_path:
        new_list = [p for p in template.js_files if p != file_path]
        update_data["js_files"] = new_list
    elif "images" in file_path:
        new_list = [p for p in template.images if p != file_path]
        update_data["images"] = new_list
    else:
        raise HTTPException(status_code=400, detail="Unknown file type")

    crud_template.update(db, db_obj=template, obj_in=update_data)
    return {"message": "File deleted", "file_path": file_path}