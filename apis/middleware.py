'''This module includes routers into the FastAPI framework.'''

from fastapi import APIRouter

from config import get_settings
from apis.routers import admin_login, admin_mgmt, farm


settings = get_settings()
api_routers = APIRouter()


# Admin
admin_schema = False  # pylint: disable=[C0103]
router_prefix = f'{settings.API.PREFIX}/admin'
tags = ['Admin']
api_routers.include_router(admin_login.router, prefix=router_prefix, tags=tags, include_in_schema=admin_schema)
api_routers.include_router(admin_mgmt.router, prefix=router_prefix, tags=tags, include_in_schema=admin_schema)


# Farm
router_prefix = f'{settings.API.PREFIX}/farm'
tags = ['Farm']
api_routers.include_router(farm.router, prefix=router_prefix, tags=tags)
