'''This module is part of the /farm FastAPI router.'''

import pymssql

from fastapi import APIRouter, Depends, status
from fastapi_pagination import Page, paginate

from config import get_settings
from helpers.misc import AppSettings
# from helpers.api_exceptions import ResponseValidationError # TODO: add exceptions
from database.external import MSSQLDatabase
from apis.schemas.farm import Farm, FarmResponse
from security.dependencies import valid_farm_id
from models.farm_data_transformation import FarmData


router = APIRouter()


@router.post('', status_code=status.HTTP_200_OK, response_model=Page[FarmResponse])
async def find_farms(
    item: Farm,
    db: pymssql = Depends(MSSQLDatabase.connect),
    settings: AppSettings = Depends(get_settings)
):
    '''
    Retrieves all farms that meet the requested requirements.

        :returns [FarmResponse]: Farm profiles.
    '''

    # query ALL farms
    query = settings.SQL_QUERY.farm_finder
    query = query.format(
        bool(item.status == 'Active'),
        item.resource,
        item.minSize,
        item.maxSize
    )  # TODO: add item.country and item.certifiedFSC into SQL query

    # extract
    data = MSSQLDatabase.query(conn=db, query=query)

    # transform
    data = FarmData.groupby_farm_id(data=data)
    data = FarmData.calc_radius(data=data, settings=settings)
    data = FarmData.calc_co2(data=data, settings=settings)
    data = FarmData.format(data=data)

    # load
    return paginate(data)


@router.get('/{farmId}', status_code=status.HTTP_200_OK, response_model=Page[FarmResponse])
async def find_farm(
    farmId: str = Depends(valid_farm_id),
    db: pymssql = Depends(MSSQLDatabase.connect),
    settings: AppSettings = Depends(get_settings)
):  # pylint: disable=[C0103]
    '''
    Retrieves a farm data.

        :returns [FarmResponse]: Farm profile.
    '''

    # query A farm
    query = settings.SQL_QUERY.farm
    query = query.format(farmId)

    # extract
    data = MSSQLDatabase.query(conn=db, query=query)

    # transform
    data = FarmData.groupby_farm_id(data=data)
    data = FarmData.calc_radius(data=data, settings=settings)
    data = FarmData.calc_co2(data=data, settings=settings)
    data = FarmData.format(data=data)

    # load
    return paginate(data)
