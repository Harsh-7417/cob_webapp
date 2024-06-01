"""To maintain database initial setup,configuration and connections"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Base

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, pool_size=5, echo=False)  # set echo to True if we want to debug
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    """Create the database table(s) available in model.py
    This function will be executed once at application startup and will create table(s) if they do not exist in DB
    """
    with engine.begin() as conn:
        Base.metadata.create_all(conn)


def get_db_session():
    """Yield a database session from connection pool"""
    with SessionLocal() as session:
        yield session
