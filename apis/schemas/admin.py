'''This module defines the HTTP request schemas for the /admin FastAPI routers.'''

from pydantic import BaseModel


class AccessTokenData(BaseModel):
    '''Admin access token schema for dependencies.'''

    username: str | None = None


class Admin(BaseModel):
    '''Admin schema for dependencies.'''

    username: str
    is_active: bool | None = None


class CreateAdmin(BaseModel):
    '''Router schema to admin/create'''

    username: str
    password: str


class UpdateAdmin(Admin):
    '''Router schema to admin/update'''


class AdminResponse(BaseModel):
    '''A admin profile response model.'''

    message: str
    data: dict


class AdminsResponse(BaseModel):
    '''Multiple admin profiles response model.'''

    message: str
    data: list
