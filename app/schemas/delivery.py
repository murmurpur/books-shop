# /app/schemas/delivery.py

from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID

from app.schemas.base_schema import Base
from app.models.delivery import DeliveryStatuses


class Delivery(Base):
    __tablename__ = 'deliveries'

    id = Column(UUID(as_uuid=True), primary_key=True)
    address = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    status = Column(Enum(DeliveryStatuses), nullable=False)
    deliveryman_id = Column(UUID(as_uuid=True), nullable=True)
