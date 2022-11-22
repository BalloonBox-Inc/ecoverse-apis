'''This module includes routers into the FastAPI framework.'''

from fastapi import APIRouter

from config import get_settings
from apis.routers import admin_login, admin_mgmt


settings = get_settings()
api_routers = APIRouter()
prefix = f'api/v{settings.APP.PROJECT_VERSION.split(".")[0]}'


# Admin
admin_schema = True  # pylint: disable=[C0103]
router_prefix = f'{prefix}/admin/'
tags = ['Admin']
api_routers.include_router(admin_login.router, prefix=router_prefix, tags=tags, include_in_schema=admin_schema)
api_routers.include_router(admin_mgmt.router, prefix=router_prefix, tags=tags, include_in_schema=admin_schema)
