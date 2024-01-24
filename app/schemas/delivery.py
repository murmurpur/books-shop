# /app/schemas/order.py

from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID

from app.schemas.base_schema import Base
from app.models.order import OrderStatuses


class Order(Base):
    __tablename__ = 'orders'

    id = Column(UUID(as_uuid=True), primary_key=True)
    address = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    status = Column(Enum(OrderStatuses), nullable=False)
    storekeeper_id = Column(UUID(as_uuid=True), nullable=True)
