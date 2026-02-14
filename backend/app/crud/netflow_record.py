from app.crud.base import CRUDBase
from app.models.netflow_record import NetFlowRecord
from app.schemas.netflow_record import NetFlowRecordCreate, NetFlowRecordUpdate

class CRUDNetFlowRecord(CRUDBase[NetFlowRecord, NetFlowRecordCreate, NetFlowRecordUpdate]):
    pass

netflow_record = CRUDNetFlowRecord(NetFlowRecord)