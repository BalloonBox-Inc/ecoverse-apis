'''This module defines the HTTP request/response schemas for the /nft FastAPI routers.'''

from pydantic import BaseModel
from datetime import datetime


# Requests
class CreateNFTRequest(BaseModel):
    '''Request schema to /nft'''

    nftId: str
    nftName: str
    nftArea: float
    nftValueSol: float
    geolocation: dict
    tileCount: int
    carbonUrl: str
    mintStatus: bool
    mintStartDate: datetime
    mintEndDate: datetime
    farmId: str
    genusName: list
    speciesName: list
    plantStatus: str


# Responses
class CreateNFTResponse(BaseModel):
    '''Response schema to /nft'''

    nft: str | None = None
    status: str | None = None


class FindNFTResponse(BaseModel):
    '''Response schema to /nft/{nftId}'''

    nftId: str | None = None
    nftName: str | None = None
    nftArea: float | None = None
    nftValueSol: float | None = None
    geolocation: dict | None = None
    tileCount: int | None = None
    carbonUrl: str | None = None
    mintStatus: bool | None = None
    mintStartDate: datetime | None = None
    mintEndDate: datetime | None = None
    farmId: str | None = None
    genusName: list | None = None
    speciesName: list | None = None
    plantStatus: str | None = None
