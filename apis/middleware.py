'''This module includes routers into the FastAPI framework.'''

from fastapi import APIRouter

from config import get_settings
from apis.routers import admin_login, admin_mgmt, farms


api_routers = APIRouter()

settings = get_settings()
router_prefix = f'{settings.API.PREFIX}'


# Access Token
api_routers.include_router(admin_login.router, prefix=router_prefix, tags=['Access Token'])

# Admin
api_routers.include_router(admin_mgmt.router, prefix=f'{router_prefix}/admin', tags=['Admin'], include_in_schema=False)

# Farms
api_routers.include_router(farms.router, prefix=f'{router_prefix}/farms', tags=['Farms'])
