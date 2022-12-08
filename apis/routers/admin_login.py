'''This module is part of the /admin FastAPI router.'''

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from apis.schemas.admin import AccessTokenResponse
from database.session import get_db
from security.admin import authenticate_admin
from security.tokens import JSONWebToken


router = APIRouter()


@router.post('/token', response_model=AccessTokenResponse)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    '''
    Get login access token.

        :param username [str]: Admin username.
        :param password [str]: Admin password.
    '''

    # authenticate admin login
    admin = authenticate_admin(db=db, username=form_data.username, password=form_data.password)

    # create JWT token
    access_token = JSONWebToken.create(data={'username': admin.username})

    return AccessTokenResponse(
        accessToken=access_token,
        tokenType='Bearer'
    )
