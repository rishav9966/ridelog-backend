from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
from datetime import datetime


class RideCreate(BaseModel):
    distance: float
    duration: int
    city: str


class RideResponse(BaseModel):
    id: int
    distance: float
    duration: int
    city: str
    created_at: datetime

    class Config:
        from_attributes = True

class RideOrderChoice(str, Enum):
    asc = "asc"
    desc = "desc"

class RideOrderByChoice(str, Enum):
    created_at = "created_at"
    distance = "distance"
    duration = "duration"


class PaginatedRideResponse(BaseModel):
    items: Optional[List[RideResponse]] = None
    total: int|None = None
    limit: int
    offset: int
