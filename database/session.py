'''This module creates the database engine and a session for each instance as a generator.'''

from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from config import get_settings


settings = get_settings()
engine = create_engine(settings.DATABASE.BASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator:
    '''Database generator.'''
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
