from sqlalchemy.orm import Session
from app.schemas.ride import RideCreate, RideOrderChoice, RideOrderByChoice
from app.schemas.analytics import RideAnalyticsResponse
from app.db.repositories.ride import RideRepository


class RideService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = RideRepository(db)

    def create_ride(self, user_id: int, ride: RideCreate):
        new_ride = self.repo.create(user_id, ride)
        self.db.commit()
        self.db.refresh(new_ride)
        return new_ride

    def list_my_rides(
        self,
        user_id: int,
        limit: int,
        offset: int,
        order_by: RideOrderByChoice,
        order: RideOrderChoice,
    ):
        return self.repo.list_by_user(user_id, limit, offset, order_by, order)

    def get_my_analytics(self, user_id: int) -> RideAnalyticsResponse:
        analytics = self.repo.get_user_analytics(user_id)
        return RideAnalyticsResponse(
            total_rides=analytics.total_rides,
            total_distance=analytics.total_distance,
            total_duration=analytics.total_duration,
            longest_ride=analytics.longest_ride,
            average_distance=analytics.average_distance,
            last_ride_at=analytics.last_ride_at
        )
