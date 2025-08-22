import pytest
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import tempfile
import os

from app import app
from database import get_db
from models import Base

# Test database setup
@pytest.fixture(scope="function")
def test_db():
    # Create temporary database file
    db_fd, db_path = tempfile.mkstemp()
    database_url = f"sqlite:///{db_path}"
    
    engine = create_engine(database_url, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    yield TestingSessionLocal()
    
    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)
    app.dependency_overrides.clear()

@pytest.fixture
def client(test_db):
    return TestClient(app)

@pytest.fixture
def sample_post_data():
    return {
        "id": "test_post_123",
        "text": "This is a test post about technology trends",
        "media_type": "TEXT",
        "timestamp": "2024-01-15T10:30:00Z"
    }

@pytest.fixture
def sample_insights_data():
    return {
        "views": 1000,
        "likes": 50,
        "replies": 10,
        "reposts": 5,
        "shares": 3
    }

@pytest.fixture
def mock_openai_response():
    return {
        "choices": [{
            "message": {
                "content": "Content type: Educational. This post performed well due to relevant tech content. Suggestion: Add more specific examples."
            }
        }]
    }

# Event loop fixture for async tests
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()