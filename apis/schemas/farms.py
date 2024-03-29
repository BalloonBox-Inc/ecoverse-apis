'''This module defines the HTTP request/response schemas for the /farm FastAPI routers.'''

from pydantic import BaseModel


# Responses
class FarmResponse(BaseModel):
    '''Response schema to /farm'''

    farmId: str | None = None
    groupScheme: str | None = None
    country: str | None = None
    province: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    isFscCertified: bool | None = None
    hectareUsd: float | None = None
    farmSize: float | None = None  # hectares
    farmRadius: float | None = None  # meters
    effectiveArea: float | None = None  # hectares
    treesPlanted: int | None = None  # estimated
    plantAge: float | None = None  # average
    farmCo2y: float | None = None  # tons per hectare per year
    productGroup: list | None = None
    scientificName: list | None = None


class FarmListResponse(BaseModel):
    '''Response schema to /farm'''

    items: list[FarmResponse] | None = []
    total: int | None = None
