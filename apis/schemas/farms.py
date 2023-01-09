'''This module defines the HTTP request/response schemas for the /farms FastAPI routers.'''

from pydantic import BaseModel


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
    farmCo2y: float | None = None  # tons per hectare per year
    farmCo2d: float | None = None  # tons per hectare per day