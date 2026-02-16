import os
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.portal_template import PortalTemplate
from app.core.dependencies import get_current_superuser

router = APIRouter()

TEMPLATES_DIR = Path("/app/static/templates")

@router.get("/builtin-templates")
def get_builtin_templates(current_user = Depends(get_current_superuser)):
    """
    Возвращает список доступных предустановленных шаблонов.
    """
    if not TEMPLATES_DIR.exists():
        return []
    
    templates = []
    for template_dir in TEMPLATES_DIR.iterdir():
        if template_dir.is_dir():
            auth_file = template_dir / "auth.html"
            welcome_file = template_dir / "welcome.html"
            style_file = template_dir / "style.css"
            
            if auth_file.exists() and welcome_file.exists():
                # Можно добавить preview, если есть изображение
                preview = None
                preview_path = template_dir / "preview.jpg"
                if preview_path.exists():
                    preview = f"/static/templates/{template_dir.name}/preview.jpg"
                
                templates.append({
                    "id": template_dir.name,
                    "name": template_dir.name.capitalize(),
                    "type": "auth",
                    "preview": preview
                })
    
    return templates

@router.post("/builtin-templates/{template_id}/import")
def import_builtin_template(
    template_id: str,
    venue_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser)
):
    """
    Импортирует предустановленный шаблон для указанной площадки.
    Создаёт записи в таблице portal_templates для типов auth и welcome.
    """
    template_dir = TEMPLATES_DIR / template_id
    if not template_dir.exists():
        raise HTTPException(status_code=404, detail="Template not found")
    
    auth_file = template_dir / "auth.html"
    welcome_file = template_dir / "welcome.html"
    
    if not auth_file.exists() or not welcome_file.exists():
        raise HTTPException(status_code=404, detail="Template files missing")
    
    # Читаем содержимое
    auth_html = auth_file.read_text(encoding="utf-8")
    welcome_html = welcome_file.read_text(encoding="utf-8")
    
    # Создаём записи в БД
    auth_template = PortalTemplate(
        venue_id=venue_id,
        type="auth",
        html_content=auth_html,
        is_active=False  # по умолчанию не активен
    )
    welcome_template = PortalTemplate(
        venue_id=venue_id,
        type="welcome",
        html_content=welcome_html,
        is_active=False
    )
    
    db.add(auth_template)
    db.add(welcome_template)
    db.commit()
    db.refresh(auth_template)
    db.refresh(welcome_template)
    
    return {
        "message": "Templates imported",
        "auth_id": auth_template.id,
        "welcome_id": welcome_template.id
    }