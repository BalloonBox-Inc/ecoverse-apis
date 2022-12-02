'''This module defines the HTTP request/response schemas for the /farm FastAPI routers.'''

from enum import Enum
from pydantic import BaseModel, ConstrainedFloat, PositiveFloat


# Enumerations
class Latitude(ConstrainedFloat):
    '''Allowed latitude range values.'''
    ge = -90  # greater than or equal to
    le = 90  # less than or equal to


class Longitude(ConstrainedFloat):
    '''Allowed longitude range values.'''
    ge = -180  # greater than or equal to
    le = 180  # less than or equal to


class Country(str, Enum):
    '''Allowed country values.'''

    CANADA = 'Canada'
    THAILAND = 'Thailand'


class ResourceType(str, Enum):
    '''Allowed resource type values.'''

    ECOVERSE = 'Ecoverse'
    RUBBER = 'Rubber'


class Status(str, Enum):
    '''Allowed plantation status values.'''

    ACTIVE = 'Active'
    PLANNED = 'Planned'


# Requests
class Farm(BaseModel):
    '''Request schema to /farm'''

    country: Country
    resource: ResourceType
    status: Status
    minSize: PositiveFloat | None = 0.001
    maxSize: PositiveFloat | None = 1_000_000
    certifiedFSC: bool


# Responses
class FarmResponse(BaseModel):
    '''Response schema to /farm/*'''

    farmId: str | None = None
    groupScheme: str | None = None
    productGroup: str | None = None
    genusName: str | list | None = None
    speciesName: str | list | None = None
    province: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    farmSize: float | None = None  # hectares
    farmRadius: float | None = None  # meters
    unitNumber: int | None = None  # farm units count
    effectiveArea: float | None = None  # hectares
    sphaSurvival: float | None = None  # stems per hectare
    plantAge: float | None = None  # average
    carbonSequesteredPerYear: float | None = None  # tons per hectare per year
    carbonSequesteredPerDay: float | None = None  # tons per hectare per day
