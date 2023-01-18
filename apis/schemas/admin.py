'''This module defines the HTTP request/response schemas for the /admin and /token FastAPI routers.'''

from pydantic import BaseModel
from datetime import datetime


# Dependencies
class AccessTokenData(BaseModel):
    '''Dependency schema to access token.'''

    username: str | None = None


class Admin(BaseModel):
    '''Dependency schema to admin.'''

    username: str
    is_active: bool | None = None


# Requests
class CreateAdminRequest(BaseModel):
    '''Router schema to /admin/create'''

    username: str
    password: str


class UpdateAdminRequest(Admin):
    '''Router schema to /admin/update'''


# Responses
class AccessTokenResponse(BaseModel):
    '''Response schema to /token'''

    access_token: str | None = None
    token_type: str | None = None


class CreateAdminResponse(BaseModel):
    '''Response schema to /admin/create'''

    username: str | None = None
    is_active: bool | None = None
    created_at: datetime | None = None


class RetrieveAdminsResponse(BaseModel):
    '''Response schema to /admin'''

    username: str | None = None
    is_active: bool | None = None
    updated_at: datetime | None = None


class UpdateAdminResponse(RetrieveAdminsResponse):
    '''Response schema to /admin/update'''
    pass
