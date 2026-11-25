import uuid
import pytest
import os

from main import app
from database import get_db

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User

load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

test_engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autocommit=False,
    autoflush=False
)


@pytest.fixture
def test_email():
    return f"test_{uuid.uuid4().hex}@example.com"


@pytest.fixture
def authenticated_client(test_email):
    from fastapi.testclient import TestClient

    client = TestClient(app)

    client.post(
        "/register",
        json={
            "name": "Test User",
            "email": test_email,
            "password": "TestPassword123"
        }
    )

    db = TestingSessionLocal()

    try:
        test_user = db.query(User).filter(
            User.email == test_email
        ).first()

        test_user.role = "admin"
        db.commit()

    finally:
        db.close()
    login_response = client.post(
        "/login",
        json={
            "email": test_email,
            "password": "TestPassword123"
        }
    )

    token = login_response.json()["access_token"]

    client.headers.update({
        "Authorization": f"Bearer {token}"
    })

    return client


@pytest.fixture
def normal_user_client(test_email):
    from fastapi.testclient import TestClient

    client = TestClient(app)

    # Register a normal user
    register_response = client.post(
        "/register",
        json={
            "name": "Normal Test User",
            "email": test_email,
            "password": "TestPassword123"
        }
    )

    assert register_response.status_code == 201

    # Login
    login_response = client.post(
        "/login",
        json={
            "email": test_email,
            "password": "TestPassword123"
        }
    )

    assert login_response.status_code == 200

    # Attach JWT
    token = login_response.json()["access_token"]

    client.headers.update({
        "Authorization": f"Bearer {token}"
    })

    return client


@pytest.fixture
def test_department(authenticated_client):
    response = authenticated_client.post(
        "/departments",
        json={
            "name": f"Department_{uuid.uuid4().hex[:8]}"
        }
    )

    assert response.status_code == 201

    return response.json()


@pytest.fixture
def student_email():
    return f"student_{uuid.uuid4().hex}@example.com"


@pytest.fixture
def test_student(authenticated_client, test_department, student_email):
    response = authenticated_client.post(
        "/students",
        json={
            "name": "Test Student",
            "age": 22,
            "course": "Computer Science",
            "email": student_email,
            "department_id": test_department["id"]
        }
    )

    assert response.status_code == 201

    return response.json()


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    print(Base.metadata.tables.keys())
    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    yield

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)