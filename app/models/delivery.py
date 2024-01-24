# /app/models/delivery.py

import enum
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict

from .deliveryman import Deliveryman 


class DeliveryStatuses(enum.Enum):
    CREATED = 'created'
    ACTIVATED = 'activated'
    DONE = 'done'
    CANCELED = 'canceled'


class Delivery(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    address: str
    date: datetime
    status: DeliveryStatuses
    deliveryman: Deliveryman | None = None


class CreateDeliveryRequest(BaseModel):
    order_id: UUID
    address: str
    date: str
