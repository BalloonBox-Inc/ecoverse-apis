'''This module is part of the /farms FastAPI router.'''

from fastapi import APIRouter, BackgroundTasks, Depends, status
from sqlalchemy.orm import Session

# from helpers.api_exceptions import ResponseValidationError # TODO: add exceptions
from database import crud, models
from database.session import get_db
from apis.schemas.nfts import NFTRequest, NFTResponse
from models.blockchain import BlockchainRequest
from security.admin import get_current_active_admin


router = APIRouter(dependencies=[Depends(get_current_active_admin)])


@router.post('/create', status_code=status.HTTP_200_OK, response_model=NFTResponse)
async def create_nft(
    background_task: BackgroundTasks,
    item: NFTRequest,
    db: Session = Depends(get_db)
):
    '''Creates a NFT object in the database.'''

    crud.create_object(
        db=db,
        data=models.NFTsTable(
            nftId=item.nftId,
            nftName=item.nftName,
            nftArea=item.nftArea,
            nftValueSol=item.nftValueSol,
            geolocation=item.geolocation,
            tileCount=item.tileCount,
            carbonUrl=item.carbonUrl,
            mintStatus=item.mintStatus,
            mintStartDate=item.mintStartDate,
            mintEndDate=item.mintEndDate,
            farmId=item.farmId,
            scientificName=item.scientificName,
            plantStatus=item.plantStatus
        ),
        exc_message='Unable to create NFT.'
    )

    background_task.add_task(
        BlockchainRequest.request_update,
        req_type='NFT',
        data=item.__dict__
    )

    return NFTResponse(
        status='Success',
        data=item.__dict__
    )


@router.post('/update/{nftId}', status_code=status.HTTP_200_OK, response_model=NFTResponse)
async def update_nft(
    nftId: str,
    db: Session = Depends(get_db)
):
    '''Updates a NFT mint status to True in the database.'''

    crud.update_object(
        db=db,
        table=models.NFTsTable,
        column=models.NFTsTable.nftId,
        value=nftId,
        data={'mintStatus': True},
        exc_message='Unable to update NFT.'
    )

    nft = crud.get_object(
        db=db,
        table=models.NFTsTable,
        column=models.NFTsTable.nftId,
        value=nftId,
        exc_message='Unable to find NFT.'
    )

    return NFTResponse(
        status='Success',
        data=nft.__dict__
    )
