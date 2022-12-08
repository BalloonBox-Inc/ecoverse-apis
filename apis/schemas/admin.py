'''This module defines the HTTP request/response schemas for the /admin and /token FastAPI routers.'''

from pydantic import BaseModel


# Dependencies
class AccessTokenData(BaseModel):
    '''Admin access token schema for dependencies.'''

    username: str | None = None


class Admin(BaseModel):
    '''Admin schema for dependencies.'''

    username: str
    is_active: bool | None = None


# Requests
class CreateAdmin(BaseModel):
    '''Router schema to /admin/create'''

    username: str
    password: str


class UpdateAdmin(Admin):
    '''Router schema to /admin/update'''


# Responses
class AccessTokenResponse(BaseModel):
    '''Response schema to /token'''

    accessToken: str | None = None
    tokenType: str | None = None


class AdminResponse(BaseModel):
    '''Response schema to /admin/*'''

    message: str | None = None
    data: dict | None = None


class AdminsResponse(BaseModel):
    '''Response schema to /admin'''

    message: str | None = None
    data: list | None = None
