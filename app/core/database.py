from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings


# The engine is the main connection point between SQLAlchemy and the database.
# In this project, it knows how to talk to the SQLite database from settings.
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# SessionLocal is a factory that creates new database sessions.
# Each session is used to talk to the database during one request or task.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the parent class future SQLAlchemy models will inherit from.
# We define it now so the project is ready for models in a later phase.
Base = declarative_base()


def get_db() -> Generator:
    # get_db is a FastAPI dependency that provides a database session.
    # It opens a session, gives it to the route, and then closes it safely.
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
