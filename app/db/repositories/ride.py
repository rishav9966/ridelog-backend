from sqlalchemy.orm import Session
from app.db.models.ride import Ride
from app.schemas.ride import RideCreate


class RideRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: int, ride: RideCreate) -> Ride:
        db_ride = Ride(
            distance=ride.distance,
            duration=ride.duration,
            city=ride.city,
            user_id=user_id,
        )
        self.db.add(db_ride)
        self.db.flush()
        return db_ride

    def list_by_user(self, user_id: int):
        return self.db.query(Ride).filter(Ride.user_id == user_id).all()
