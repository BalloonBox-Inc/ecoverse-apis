'''This module is part of the /farms FastAPI router.'''

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from config import get_settings
from helpers.misc import AppSettings
# from helpers.api_exceptions import ResponseValidationError # TODO: add exceptions
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

    data = FarmData.retrieve_farms(db=db, settings=settings)

    return FarmListResponse(
        items=data,
        total=len(data)
    )
