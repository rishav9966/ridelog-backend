from sqlalchemy.orm import Session
from app.db.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user: UserCreate) -> User:
        db_user = User(
            email=user.email,
            name=user.name,
            hashed_password=hash_password(user.password),
        )
        self.db.add(db_user)
        self.db.flush()
        return db_user

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()
