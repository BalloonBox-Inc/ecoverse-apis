'''This module is part of the /farm FastAPI router.'''

import pymssql
from fastapi import APIRouter, Depends, status
from fastapi_pagination import Page, paginate

from config import get_settings
from helpers.misc import AppSettings, ResponseFormatter
# from helpers.api_exceptions import ResponseValidationError
from database.external import MSSQLDatabase
from apis.schemas.farm import Farm, FarmResponse
from security.dependencies import valid_farm_id
from model.carbon_sequestration import CarbonSequestration
from model.plantation_metrics import PlantationMetrics


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

    # query farms
    query = settings.SQL_QUERY.farm_finder
    query = query.format(
        bool(item.status == 'Active'),
        item.resource,
        item.minSize,
        item.maxSize
    )  # TODO: add item.country and item.certifiedFSC into SQL query

    # fetch data
    data = MSSQLDatabase.query(conn=db, query=query)

    # calculate CO2 sequestration
    metrics = settings.PLANTATION_METRICS.plantationMetrics
    for farm in data:
        spha = farm['SphaSurvival']
        if not spha:
            spha = 1  # TODO: update spha

        tree = PlantationMetrics.tree(data=farm, metrics=metrics)
        co2 = CarbonSequestration.tons_per_hectare_per_year(tree=tree, spha=spha*0.9, age=farm['PlantAge'], settings=settings)
        farm['CarbonSequestered'] = co2

    # format response
    data = ResponseFormatter.obj_list_to_camel_case(data=data)

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

    # query farm
    query = settings.SQL_QUERY.farm
    query = query.format(farmId)

    # fetch data
    data = MSSQLDatabase.query(conn=db, query=query)

    # calculate CO2 sequestration
    metrics = settings.PLANTATION_METRICS.plantationMetrics
    for farm in data:
        spha = farm['SphaSurvival']
        if not spha:
            spha = 1  # TODO: update spha

        tree = PlantationMetrics.tree(data=farm, metrics=metrics)
        co2 = CarbonSequestration.tons_per_hectare_per_year(tree=tree, spha=spha*0.9, age=farm['PlantAge'], settings=settings)
        farm['CarbonSequestered'] = co2

    # format response
    data = ResponseFormatter.obj_list_to_camel_case(data=data)

    return paginate(data)
