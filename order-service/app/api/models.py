from pydantic import BaseModel
from typing import List, Optional

class orderIn(BaseModel):
    name: str
    plot: str
    genres: List[str]
    casts_id: List[int]


class orderOut(orderIn):
    id: int


class orderUpdate(orderIn):
    name: Optional[str] = None
    plot: Optional[str] = None
    genres: Optional[List[str]] = None
    casts_id: Optional[List[int]] = None