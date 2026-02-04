from sqlalchemy.orm import Session
from sqlalchemy import func, desc, select
from app.db.models.ride import Ride
from app.schemas.ride import RideCreate, RideOrderByChoice, RideOrderChoice


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

    def list_by_user(
        self,
        user_id: int,
        limit: int,
        offset: int,
        order_by: RideOrderByChoice,
        order: RideOrderChoice,
    ):
        if order == RideOrderChoice.desc:
            return (
                self.db.query(Ride)
                .filter(Ride.user_id == user_id)
                .order_by(desc(order_by))
                .limit(limit)
                .offset(offset)
                .all()
            )
        return (
            self.db.query(Ride)
            .filter(Ride.user_id == user_id)
            .order_by(desc(order_by))
            .limit(limit)
            .offset(offset)
            .all()
        )

    def get_user_analytics(self, user_id: int):
        return (
            self.db.query(
                func.count(Ride.id).label("total_rides"),
                func.coalesce(func.sum(Ride.distance), 0).label("total_distance"),
                func.coalesce(func.sum(Ride.duration), 0).label("total_duration"),
                func.coalesce(func.max(Ride.distance), 0).label("longest_ride"),
                func.coalesce(func.avg(Ride.distance), 0).label("average_distance"),
                func.max(Ride.created_at).label("last_ride_at"),
            )
            .filter(Ride.user_id == user_id)
            .one()
        )

    def get_rides_count(self, user_id: int):
        return (
            self.db.execute(select(func.count()).select_from(Ride).where(Ride.user_id==user_id))
            .scalar()
        )
