'''This module is part of the /farm FastAPI router.'''

from fastapi import APIRouter, BackgroundTasks, Depends, status
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from config import get_settings
from helpers.misc import AppSettings, FileManagement
# from helpers.api_exceptions import ResponseValidationError # TODO: add exceptions
from database import crud, models
from database.session import get_db
from security.admin import get_current_active_admin
from security.dependencies import valid_farm_id
from models.farm_proof_of_service import FarmProofOfService


router = APIRouter(dependencies=[Depends(get_current_active_admin)])


@router.get('/satellite/{farmId}', dependencies=[Depends(valid_farm_id)], status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def show_farm_satellite_view(
    background_task: BackgroundTasks,
    farmId: str,
    db: Session = Depends(get_db),
    settings: AppSettings = Depends(get_settings)
):
    '''Retrieves a satellite image from a given farm.'''

    farm = crud.get_object(
        db=db,
        table=models.FarmsTable,
        column=models.FarmsTable.FarmId,
        value=farmId,
        exc_message='Unable to find farm.'
    )

    html = FarmProofOfService.satellite_mapbox(
        farm_id=farmId,
        lat=farm.Latitude,
        lng=farm.Longitude,
        settings=settings
    )

    background_task.add_task(
        FileManagement.remove_file,
        filename=html
    )

    return FileManagement.read_file(html)
