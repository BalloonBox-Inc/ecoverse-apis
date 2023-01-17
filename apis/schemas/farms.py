'''This module defines the HTTP request/response schemas for the /farm FastAPI routers.'''

from pydantic import BaseModel


# Responses
class FarmResponse(BaseModel):
    '''Response schema to /farm'''

    farmId: str | None = None
    groupScheme: str | None = None
    productGroup: str | None = None
    genusName: list | None = None
    speciesName: list | None = None
    country: str | None = None
    province: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    farmSize: float | None = None  # hectares
    farmRadius: float | None = None  # meters
    effectiveArea: float | None = None  # hectares
    treesPlanted: int | None = None  # estimated
    plantAge: float | None = None  # average
    farmCo2y: float | None = None  # tons per hectare per year
