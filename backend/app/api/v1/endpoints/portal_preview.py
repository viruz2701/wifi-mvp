from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.portal_template import PortalTemplate
from app.core.dependencies import get_current_superuser

router = APIRouter()

def render_template(html: str, context: dict) -> str:
    import re
    def replace(match):
        key = match.group(1)
        return str(context.get(key, f"$({key})"))
    return re.sub(r'\$\((\w+)\)', replace, html)

@router.get("/preview/{template_id}", response_class=HTMLResponse)
def preview_template(
    template_id: int,
    venue_id: int = Query(..., description="ID площадки для подстановки имени"),
    mac: str = Query("AA:BB:CC:DD:EE:FF", description="Тестовый MAC"),
    phone: str = Query("71234567890", description="Тестовый телефон"),
    error: str = Query("", description="Тестовое сообщение об ошибке"),
    banner_url: str = Query("/static/test_banner.jpg", description="URL тестового баннера"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),  # только админ
):
    """Предпросмотр шаблона с подстановкой тестовых данных."""
    template = db.get(PortalTemplate, template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    # Получаем имя площадки (необязательно, но для макроса $(venue_name))
    venue = db.get(Venue, venue_id)
    venue_name = venue.name if venue else "Тестовая площадка"

    context = {
        "venue_name": venue_name,
        "mac": mac,
        "phone": phone,
        "error": error,
        "banner_url": banner_url,
        "code": "1234",        # тестовый код
        "dst": "http://example.com",
        "year": "2026"
    }
    return render_template(template.html_content, context)