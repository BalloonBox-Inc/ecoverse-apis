'''This module is part of the /farms FastAPI router.'''

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from config import get_settings
from helpers.misc import AppSettings, DataFormatter
# from helpers.api_exceptions import ResponseValidationError # TODO: add exceptions
from database import crud, models
from database.session import get_db
from apis.schemas.farms import FarmListResponse
from security.admin import get_current_active_admin
from models.farm_data_transformation import FarmData


router = APIRouter(dependencies=[Depends(get_current_active_admin)])


@router.get('', status_code=status.HTTP_200_OK, response_model=FarmListResponse)
async def retrieve_farms(
    db: Session = Depends(get_db),
    settings: AppSettings = Depends(get_settings)
):
    '''Retrieves all farms.'''

    # extract
    farm = DataFormatter.class_to_dict_list(
        lst=crud.get_table(
            db=db,
            table=models.FarmsTable
        )
    )

    ha = DataFormatter.class_to_dict_list(
        lst=crud.get_table(
            db=db,
            table=models.PricingTable
        )
    )

    # transform
    data = FarmData.add_tree_co2(data=farm, settings=settings)
    data = FarmData.groupby_farm_id(data=data)
    data = FarmData.add_scientific_name(data=data)
    data = FarmData.add_farm_radius(data=data, settings=settings)
    data = FarmData.add_farm_co2(data=data, settings=settings)
    data = FarmData.add_trees_planted(data=data)
    data = FarmData.add_hectare_price(data=data, ha=ha)
    data = FarmData.response_format(data=data)

    # TODO: this data must come from the source partners, remove it after it
    for d in data:
        if d['groupScheme'] == 'Sri Trang Thailand':
            d['isFscCertified'] = True
        else:
            d['isFscCertified'] = False

    return FarmListResponse(
        items=data,
        total=len(data)
    )
