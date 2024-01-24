# /app/models/order.py

import enum
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.models.storekeeper import Storekeeper 


class OrderStatuses(enum.Enum):
    CREATED = 'created'
    ACTIVATED = 'activated'
    DONE = 'done'
    CANCELED = 'canceled'


class Order(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    address: str
    date: datetime
    status: OrderStatuses
    storekeeper: Storekeeper | None = None


class CreateOrderRequest(BaseModel):
    order_id: UUID
    address: str
    date: str
