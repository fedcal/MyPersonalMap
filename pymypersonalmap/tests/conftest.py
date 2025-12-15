"""
Pytest Configuration and Fixtures

Shared fixtures for testing across the application.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pymypersonalmap.database.session import Base
from pymypersonalmap.models.user import User
from pymypersonalmap.models.labels import Label
from pymypersonalmap.models.marker import Marker


@pytest.fixture(scope="function")
def test_db():
    """
    Create a temporary in-memory SQLite database for testing

    This fixture creates a fresh database for each test function,
    ensuring test isolation.
    """
    # Create in-memory SQLite database
    engine = create_engine("sqlite:///:memory:", echo=False)

    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Create session factory
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Provide session
    db = TestSessionLocal()

    yield db

    # Cleanup
    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def sample_user(test_db):
    """Create a sample user for testing"""
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_password_here"
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


@pytest.fixture(scope="function")
def sample_labels(test_db):
    """Create sample labels for testing"""
    labels = [
        Label(name="Urbex", color="#FF5733", icon="building", is_system=True),
        Label(name="Restaurant", color="#33FF57", icon="utensils", is_system=True),
        Label(name="Photo Spot", color="#3357FF", icon="camera", is_system=False),
    ]
    for label in labels:
        test_db.add(label)
    test_db.commit()

    for label in labels:
        test_db.refresh(label)

    return labels


@pytest.fixture(scope="function")
def sample_marker(test_db, sample_user):
    """Create a sample marker for testing"""
    marker = Marker(
        title="Duomo di Milano",
        description="Gothic cathedral in Milan",
        latitude=45.4642,
        longitude=9.1900,
        address="Piazza del Duomo, Milano, Italy",
        is_favorite=False,
        user_id=sample_user.idUser
    )
    test_db.add(marker)
    test_db.commit()
    test_db.refresh(marker)
    return marker
