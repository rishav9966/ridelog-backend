from sqlalchemy.orm import Session
from app.schemas.ride import RideCreate
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

    def list_my_rides(self, user_id: int):
        return self.repo.list_by_user(user_id)
