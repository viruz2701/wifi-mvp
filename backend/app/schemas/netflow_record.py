from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NetFlowRecordBase(BaseModel):
    
    src_ip: str
    dst_ip: str
    bytes: int
    packets: int
    src_port: Optional[int] = None
    dst_port: Optional[int] = None
    protocol: Optional[int] = None
    flow_start: Optional[datetime] = None
    flow_end: Optional[datetime] = None
    
class NetFlowRecordUpdate(BaseModel):
    pass

class NetFlowRecordCreate(NetFlowRecordBase):
    session_id: Optional[int] = None

class NetFlowRecordOut(NetFlowRecordBase):
    id: int
    time: datetime
    session_id: Optional[int]

    class Config:
        from_attributes = True