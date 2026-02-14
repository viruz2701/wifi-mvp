from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.netflow_record import netflow_record
from app.schemas.netflow_record import NetFlowRecordCreate, NetFlowRecordOut
from app.models.session import Session as DBSession

router = APIRouter()

@router.post("/records", response_model=NetFlowRecordOut)
async def create_netflow_record(
    record: NetFlowRecordCreate,
    db: Session = Depends(get_db)
):
    """
    Эндпоинт для приёма записей NetFlow от слушателя.
    """
    # Если передан session_id, можно проверить его существование
    if record.session_id:
        session = db.get(DBSession, record.session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
    return netflow_record.create(db, obj_in=record)