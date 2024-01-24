# /app/models/storekeeper.py

from uuid import UUID
from pydantic import BaseModel, ConfigDict


class Storekeeper(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
