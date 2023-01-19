'''This module defines all database tables.'''

from sqlalchemy import Column, Boolean, Integer, Float, String, DateTime, JSON, PickleType
from sqlalchemy.ext.mutable import MutableList
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


class FarmsTable(Base):
    '''Define farms as a database table.'''

    __tablename__ = 'farms'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    GroupScheme = Column(String, nullable=False)
    Country = Column(String, nullable=False)
    Province = Column(String, nullable=False)
    Latitude = Column(Float, nullable=False)
    Longitude = Column(Float, nullable=False)
    FarmId = Column(String, nullable=False)
    FarmSize = Column(Float, nullable=False)
    UnitNumber = Column(String, nullable=False)
    EffectiveArea = Column(Float, nullable=False)
    AreaTypeName = Column(String, nullable=False)
    ProductGroup = Column(String, nullable=False)
    GenusName = Column(String, nullable=False)
    SpeciesName = Column(String, nullable=False)
    PlantAge = Column(Float, nullable=False)
    SphaSurvival = Column(Float, nullable=False)
    PlannedPlantDT = Column(String, nullable=False)
    IsActive = Column(Boolean, nullable=False)
    CreatedAt = Column(DateTime(timezone=True), server_default=func.now())
    UpdatedAt = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class NFTsTable(Base):

    '''Define nfts as a database table.'''

    __tablename__ = 'nfts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nftId = Column(String, unique=True, nullable=False)
    nftName = Column(String, nullable=False)
    nftArea = Column(Float, nullable=False)
    nftValueSol = Column(Float, nullable=False)
    geolocation = Column(JSON, nullable=False)
    tileCount = Column(Integer, nullable=False)
    carbonUrl = Column(String, nullable=False)
    mintStatus = Column(Boolean, nullable=False)
    mintStartDate = Column(DateTime(timezone=True), nullable=False)
    mintEndDate = Column(DateTime(timezone=True), nullable=False)
    farmId = Column(String, nullable=False)
    scientificName = Column(MutableList.as_mutable(PickleType), default=[], nullable=False)
    plantStatus = Column(String, nullable=False)
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class PricingTable(Base):

    '''Define pricing as a database table.'''

    __tablename__ = 'pricing'

    id = Column(Integer, primary_key=True, autoincrement=True)
    groupScheme = Column(String, unique=True, nullable=False)
    hectareUsd = Column(Float, nullable=False)
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
