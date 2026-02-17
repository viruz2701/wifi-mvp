from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date, datetime
from app.db.session import get_db
from app.models.nas_status_history import NASStatusHistory
from app.models.nas_device import NASDevice
from app.core.dependencies import get_current_superuser

router = APIRouter()

@router.get("/nas-status-history")
def get_nas_status_history(
    db: Session = Depends(get_db),
    nas_device_id: Optional[int] = Query(None),
    from_date: Optional[date] = Query(None),
    to_date: Optional[date] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user = Depends(get_current_superuser)
):
    query = db.query(NASStatusHistory)
    if nas_device_id:
        query = query.filter(NASStatusHistory.nas_device_id == nas_device_id)
    if from_date:
        query = query.filter(NASStatusHistory.checked_at >= datetime.combine(from_date, datetime.min.time()))
    if to_date:
        query = query.filter(NASStatusHistory.checked_at <= datetime.combine(to_date, datetime.max.time()))
    query = query.order_by(NASStatusHistory.checked_at.desc())
    return query.offset(skip).limit(limit).all()