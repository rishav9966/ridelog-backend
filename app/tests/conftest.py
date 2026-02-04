import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base import Base
from app.db.deps import get_db
from app.core.config import settings
from app.core.security import hash_password

from app.db.models.user import User

# -------------
# Test DB Setup
# -------------

TEST_DB_URL = "sqlite:///.test.db"

engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# -------------
# DB Fixtures
# -------------

@pytest.fixture(scope="session")
def db_engine():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()

    session = TestingSessionLocal(bind=connection)

    try: 
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()

# -------------
# Dependency overrides
# -------------

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# -------------------------
# Test user fixture
# -------------------------

@pytest.fixture(scope="function")
def test_user(db_session):
    user = User(
        email="test@example.com",
        name="Test User",
        hashed_password=hash_password("Str0ng!Pass123"),
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


# -------------------------
# Auth header fixture
# -------------------------

@pytest.fixture(scope="function")
def auth_headers(client, test_user):
    response = client.post(
        "/users/login",
        json={
            "email": "test@example.com",
            "password": "Str0ng!Pass123",
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}
