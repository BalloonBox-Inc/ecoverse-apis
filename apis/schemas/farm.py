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
class FarmFinder(BaseModel):
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

    FarmId: str | None = None
    UnitNumber: str | None = None
    PolygonArea: float | None = None
    EffectiveArea: float | None = None
    PlannedPlantDT: str | None = None
    PlantDT: str | None = None
    IsActive: bool | None = None
    Latitude: float | None = None
    Longitude: float | None = None
    Province: str | None = None
    FarmSize: float | None = None
    IsSuspended: bool | None = None
    GroupSchemeName: str | None = None
    ProductGroupDescription: str | None = None
    GenusName: str | None = None
    SpeciesName: str | None = None
    CarbonSequestered: float | None = None
