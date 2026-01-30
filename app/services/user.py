from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin
from app.db.repositories.user import UserRepository
from app.core.security import verify_password, create_access_token


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = UserRepository(db)

    def create_user(self, user: UserCreate):
        if self.repo.get_by_email(user.email):
            raise ValueError("Email already registered")

        new_user = self.repo.create(user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def login(self, credentials: UserLogin):
        user = self.repo.get_by_email(credentials.email)
        if not user or not verify_password(credentials.password, user.hashed_password):
            raise ValueError("Invalid credentials")

        return create_access_token({"sub": str(user.id)})
