"""
Database Session Management

SQLAlchemy database session configuration and management.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pymypersonalmap.config.settings import database_url, DB_ECHO

# Create SQLAlchemy engine
engine = create_engine(
    database_url,
    echo=DB_ECHO,
    pool_pre_ping=True,
    pool_recycle=3600,
)

# Create SessionLocal class
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Create Base class for models
Base = declarative_base()


def get_db():
    """
    Dependency to get database session

    Usage in FastAPI:
        @app.get("/items")
        def get_items(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database

    Creates all tables defined in models.
    """
    from pymypersonalmap.models import user, marker, labels, marker_label  # Import all models
    Base.metadata.create_all(bind=engine)


def drop_db():
    """
    Drop all database tables

    WARNING: This will delete all data!
    """
    Base.metadata.drop_all(bind=engine)
