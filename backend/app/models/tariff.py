from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.sql import func
from app.models.base import BaseModel

class TariffPlan(BaseModel):
    __tablename__ = "tariff_plans"

    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False, default=0.0)
    currency = Column(String, nullable=False, default="RUB")
    duration_hours = Column(Integer, nullable=False)  # длительность действия тарифа в часах
    speed_limit_up_kbps = Column(Integer, nullable=True)  # ограничение скорости вверх (kbps)
    speed_limit_down_kbps = Column(Integer, nullable=True)  # ограничение скорости вниз (kbps)
    is_active = Column(Boolean, default=True)

# Ассоциативная таблица для связи TariffPlan и Venue (многие-ко-многим)
venue_tariff = Table(
    'venue_tariff',
    BaseModel.metadata,
    Column('venue_id', Integer, ForeignKey('venues.id'), primary_key=True),
    Column('tariff_id', Integer, ForeignKey('tariff_plans.id'), primary_key=True),
    Column('priority', Integer, default=0),  # порядок отображения
    Column('is_available', Boolean, default=True),
    Column('created_at', DateTime(timezone=True), server_default=func.now())
)

# Альтернативно можно сделать отдельную модель с дополнительными полями, но для простоты используем Table.