'''This module is part of the /farms FastAPI router.'''

from fastapi import APIRouter, BackgroundTasks, Depends, status
from sqlalchemy.orm import Session

from helpers.misc import DataAggregator
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


@router.post('/update', status_code=status.HTTP_200_OK, response_model=NFTResponse)
async def update_nft(
    item: NFTRequest,
    db: Session = Depends(get_db)
):
    '''Updates a NFT object in the database.'''

    nft = crud.get_object(
        db=db,
        table=models.NFTsTable,
        column=models.NFTsTable.nftId,
        value=item.nftId,
        exc_message='Unable to find NFT.'
    )

    update = DataAggregator.dict_mismatch(d1=nft.__dict__, d2=item.__dict__)
    if update:
        crud.update_object(
            db=db,
            table=models.NFTsTable,
            column=models.NFTsTable.nftId,
            value=item.nftId,
            data=update,
            exc_message='Unable to update NFT.'
        )

    return NFTResponse(
        status='Success',
        data=item.__dict__
    )
