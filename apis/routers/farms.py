'''This module is part of the /farms FastAPI router.'''

from fastapi import APIRouter, Depends, status
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session

from config import get_settings
from helpers.misc import AppSettings, DataFormatter
# from helpers.api_exceptions import ResponseValidationError # TODO: add exceptions
from database import crud, models
from database.session import get_db
from apis.schemas.farms import FarmResponse
from security.admin import get_current_active_admin
from models.farm_data_transformation import FarmData


router = APIRouter(dependencies=[Depends(get_current_active_admin)])


@router.get('', status_code=status.HTTP_200_OK, response_model=Page[FarmResponse])
async def retrieve_farms(
    db: Session = Depends(get_db),
    settings: AppSettings = Depends(get_settings)
):
    '''Retrieves all farms.'''

    # extract
    data = crud.get_table(
        db=db,
        table=models.FarmsTable
    )
    data = DataFormatter.class_to_dict_list(data)

    # transform
    data = FarmData.add_tree_co2(data=data, settings=settings)
    data = FarmData.groupby_farm_unit(data=data)
    data = FarmData.groupby_farm_id(data=data)
    data = FarmData.add_farm_radius(data=data, settings=settings)
    data = FarmData.add_farm_co2(data=data, settings=settings)
    data = FarmData.response_format(data=data)

    return paginate(data)