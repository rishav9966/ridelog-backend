from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RideAnalyticsResponse(BaseModel):
    total_rides: int
    total_distance: int
    total_duration: int
    longest_ride: float
    average_distance: float
    last_ride_at: Optional[datetime]
