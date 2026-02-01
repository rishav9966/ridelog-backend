from pydantic import BaseModel
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
