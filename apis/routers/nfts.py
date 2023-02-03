'''This module is part of the /farms FastAPI router.'''
import datetime
import json
from fastapi import APIRouter, BackgroundTasks, Depends, status
from sqlalchemy.orm import Session

from config import get_settings
from helpers.misc import AppSettings, DataAggregator, DataFormatter
from helpers.api_exceptions import ResponseValidationError
from database import crud, models
from database.session import get_db
from apis.schemas.nfts import NFTRequest, NFTResponse, NFTCO2Response
from models.blockchain import BlockchainRequest
from models.farm_data_transformation import FarmData
from models.carbon_sequestration import NftCarbonSequestration
from security.admin import get_current_active_admin


router = APIRouter(dependencies=[Depends(get_current_active_admin)])


@router.post('/create', status_code=status.HTTP_200_OK, response_model=NFTResponse)
async def create_nft(
    background_task: BackgroundTasks,
    item: NFTRequest,
    db: Session = Depends(get_db),
    settings: AppSettings = Depends(get_settings)
):
    '''Creates a NFT object in the database.'''

    item.geolocation = json.loads(item.geolocation)

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
            mintStatus=False,
            mintStartDate=item.mintStartDate,
            mintEndDate=item.mintEndDate,
            farmId=item.farmId,
            scientificName=item.scientificName,
            plantStatus=item.plantStatus
        ),
        exc_message='Unable to create NFT.'
    )

    update = DataFormatter.dictionary(data=item.__dict__, name='NFT')
    background_task.add_task(
        BlockchainRequest.request_update,
        req_type='NFT',
        data=update,
        settings=settings
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


@router.get('/{nftId}', status_code=status.HTTP_200_OK, response_model=NFTCO2Response)
async def get_nft_carbon_sequestered(
    nftId: str,
    db: Session = Depends(get_db),
    settings: AppSettings = Depends(get_settings)
):
    '''Calculates carbon sequestered in real-time of a given NFT in tons.'''

    nft = crud.get_object(
        db=db,
        table=models.NFTsTable,
        column=models.NFTsTable.nftId,
        value=nftId,
        exc_message='Unable to find NFT.'
    )

    farms = FarmData.retrieve_farms(db=db, settings=settings)
    try:
        farm = [d for d in farms if d['farmId'] == nft.farmId][0]
    except (KeyError, IndexError) as exc:
        raise ResponseValidationError(
            status_code=status.HTTP_400_BAD_REQUEST,
            message='Unable to find NFT.'
        ) from exc

    # calculate timedelta in seconds
    period = DataAggregator.date_difference_in_seconds(
        start=nft.mintStartDate,
        end=datetime.datetime.now(datetime.timezone.utc)
    )

    # NFT carbon sequestered in tons
    nft_co2 = NftCarbonSequestration.nft_carbon_sequestration(
        nft_area=nft.nftArea,
        farm_spha=farm['sphaSurvival'],
        trees_co2=farm['plantCo2'],
        period=period,
        settings=settings
    )

    resp = nft.__dict__
    resp['co2Tons'] = nft_co2

    return NFTCO2Response(
        status='Success',
        data=resp
    )
