from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.services.user import UserService
from app.services.ride import RideService


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)


def get_ride_service(db: Session = Depends(get_db)) -> RideService:
    return RideService(db)
