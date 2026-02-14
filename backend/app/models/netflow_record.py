from sqlalchemy import Column, Integer, BigInteger, DateTime, String, ForeignKey
from sqlalchemy.sql import func
from app.models.base import BaseModel

class NetFlowRecord(BaseModel):
    __tablename__ = "netflow_records"

    time = Column(DateTime(timezone=True), server_default=func.now(), primary_key=True)  # время записи
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=True)  # может быть NULL, если сессия не найдена
    src_ip = Column(String(45), nullable=False)
    dst_ip = Column(String(45), nullable=False)
    bytes = Column(BigInteger, nullable=False)
    packets = Column(BigInteger, nullable=False)
    src_port = Column(Integer, nullable=True)
    dst_port = Column(Integer, nullable=True)
    protocol = Column(Integer, nullable=True)
    flow_start = Column(DateTime(timezone=True), nullable=True)
    flow_end = Column(DateTime(timezone=True), nullable=True)