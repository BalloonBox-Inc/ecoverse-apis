'''This module defines all database tables.'''

from sqlalchemy import Column, Boolean, Integer, String, DateTime
from sqlalchemy.sql import func
from database.session import Base


class AdminsTable(Base):
    '''Define admins as a database table.'''

    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
