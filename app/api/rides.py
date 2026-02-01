from fastapi import APIRouter, Depends
from app.schemas.ride import RideCreate, RideResponse
from app.schemas.analytics import RideAnalyticsResponse
from app.services.ride import RideService
from app.deps import get_ride_service
from app.core.auth import get_current_user
from app.db.models.user import User

router = APIRouter(prefix="/rides", tags=["Rides"])


@router.post("/", response_model=RideResponse)
def create_ride(
    ride: RideCreate,
    service: RideService = Depends(get_ride_service),
    current_user: User = Depends(get_current_user),
):
    return service.create_ride(current_user.id, ride)


@router.get("/", response_model=list[RideResponse])
def my_rides(
    service: RideService = Depends(get_ride_service),
    current_user: User = Depends(get_current_user),
):
    return service.list_my_rides(current_user.id)


@router.get("/analytics", response_model=RideAnalyticsResponse)
def ride_analytics(
    service: RideService = Depends(get_ride_service),
    current_user: User = Depends(get_current_user)
):
    return service.get_my_analytics(current_user.id)
