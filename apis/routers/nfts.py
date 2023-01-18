'''This module is part of the /farms FastAPI router.'''

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from helpers.misc import DataAggregator, DatabaseFormatter, ResponseFormatter
# from helpers.api_exceptions import ResponseValidationError # TODO: add exceptions
from database import crud, models
from database.session import get_db
from apis.schemas.nfts import CreateNFTRequest, CreateNFTResponse, FindNFTResponse
from security.admin import get_current_active_admin


router = APIRouter()  # dependencies=[Depends(get_current_active_admin)]) # TODO: fix dependency


@router.post('', status_code=status.HTTP_200_OK, response_model=CreateNFTResponse)
async def create_nft(
    item: CreateNFTRequest,
    db: Session = Depends(get_db)
):
    '''Stores a NFT in the database.'''

    # check if object already exists
    nft_object = db.query(models.NFTsTable).filter(models.NFTsTable.NftId == item.nftId).first()
    if not nft_object:
        crud.create_object(
            db=db,
            data=models.NFTsTable(
                NftId=item.nftId,
                NftName=item.nftName,
                NftArea=item.nftArea,
                NftValueSol=item.nftValueSol,
                Geolocation=item.geolocation,
                TileCount=item.tileCount,
                CarbonUrl=item.carbonUrl,
                MintStatus=item.mintStatus,
                MintStartDate=item.mintStartDate,
                MintEndDate=item.mintEndDate,
                FarmId=item.farmId,
                GenusName=item.genusName,
                SpeciesName=item.speciesName,
                PlantStatus=item.plantStatus
            ),
            exc_message='Unable to create NFT.'
        )
    else:
        update = ResponseFormatter.obj_list_case_converter(
            data=[
                DataAggregator.dict_mismatch(
                    d1=DatabaseFormatter.nft_table(data=nft_object.__dict__),
                    d2=item.__dict__
                )
            ],
            format='pascal'
        )[0]
        if update:  # TODO: not working
            crud.update_object(
                db=db,
                table=models.NFTsTable,
                column=models.NFTsTable.NftId,
                value=item.nftId,
                data=update,
                exc_message='Unable to update NFT.'
            )

    return CreateNFTResponse(
        nft=item.nftName,
        status='Success'
    )


@router.get('/{nftId}', status_code=status.HTTP_200_OK, response_model=FindNFTResponse)
async def find_nft(
    nftId: str,
    db: Session = Depends(get_db)
):
    '''Retrieves a NFT from the database.'''
    nft_object = crud.get_object(
        db=db,
        table=models.NFTsTable,
        column=models.NFTsTable.NftId,
        value=nftId,
        exc_message='Unable to find NFT.'
    )

    resp = DatabaseFormatter.nft_table(data=nft_object.__dict__)

    return FindNFTResponse(
        nftId=resp['nftId'],
        nftName=resp['nftName'],
        nftArea=resp['nftArea'],
        nftValueSol=resp['nftValueSol'],
        geolocation=resp['geolocation'],
        tileCount=resp['tileCount'],
        carbonUrl=resp['carbonUrl'],
        mintStatus=resp['mintStatus'],
        mintStartDate=resp['mintStartDate'],
        mintEndDate=resp['mintEndDate'],
        farmId=resp['farmId'],
        genusName=resp['genusName'],
        speciesName=resp['speciesName'],
        plantStatus=resp['plantStatus']
    )
