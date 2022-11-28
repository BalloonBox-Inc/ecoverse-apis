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

    THAILAND = 'Thailand'


class ResourceType(str, Enum):
    '''Allowed resource type values.'''

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
    unitNumber: str | None = None
    polygonArea: float | None = None
    effectiveArea: float | None = None
    plannedPlantDt: str | None = None
    plantDt: str | None = None
    isActive: bool | None = None
    latitude: float | None = None
    longitude: float | None = None
    province: str | None = None
    farmSize: float | None = None
    isSuspended: bool | None = None
    groupSchemeName: str | None = None
    productGroupDescription: str | None = None
    genusName: str | None = None
    speciesName: str | None = None
    carbonSequestered: float | None = None
