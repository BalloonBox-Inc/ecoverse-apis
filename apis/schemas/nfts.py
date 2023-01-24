'''This module defines the HTTP request/response schemas for the /nft FastAPI routers.'''

from datetime import datetime
from pydantic import BaseModel


# Requests
class NFTRequest(BaseModel):
    '''Request schema to /nft/*'''

    nftId: str
    nftName: str
    nftArea: float
    nftValueSol: float
    geolocation: dict
    tileCount: int
    carbonUrl: str
    mintStartDate: datetime
    mintEndDate: datetime
    farmId: str
    scientificName: list
    plantStatus: str


# Responses
class NFT(BaseModel):
    '''Standard NFT schema.'''

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
    scientificName: list | None = None
    plantStatus: str | None = None


class NFTResponse(BaseModel):
    '''Response schema to /nft/*'''

    status: str | None = None
    data: NFT | None = None
