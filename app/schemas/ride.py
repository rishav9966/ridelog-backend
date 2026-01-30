from pydantic import BaseModel


class RideCreate(BaseModel):
    distance: float
    duration: int
    city: str


class RideResponse(BaseModel):
    id: int
    distance: float
    duration: int
    city: str

    class Config:
        from_attributes = True
