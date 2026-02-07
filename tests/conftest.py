"""
Pytest configuration and fixtures
"""
import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Set test database URL
os.environ["DATABASE_URL"] = "mysql+pymysql://admin:password@localhost:3306/social_commerce_test"
os.environ["JWT_SECRET_KEY"] = "test-secret-key-for-testing-only"
os.environ["ENVIRONMENT"] = "test"

from backend.shared.database.connection import Base, get_db

# Create test database engine
TEST_DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create test client with database override"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    # Import app after setting up test environment
    from backend.services.user_service.src.main import app
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def test_user():
    """Test user data"""
    return {
        "email": "test@example.com",
        "username": "testuser",
        "full_name": "Test User",
        "password": "testpass123",
        "is_creator": False
    }


@pytest.fixture
def auth_token(client, test_user):
    """Get authentication token for test user"""
    # Register user
    client.post("/register", json=test_user)
    
    # Login
    response = client.post(
        "/token",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
        }
    )
    return response.json()["access_token"]
