'''This module manages admin authentication.'''

from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError

from apis.schemas.admin import AccessTokenData, Admin
from database import crud, models
from database.session import get_db
from security.hashing import SecureHash
from security.tokens import JSONWebToken
from config import get_settings


settings = get_settings()
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl=f'{settings.API.PREFIX}/token')


def get_admin(db: Session, username: str):
    '''Retrieve admin from the database.'''
    return crud.get_object(
        db=db,
        table=models.AdminsTable,
        column=models.AdminsTable.username,
        value=username,
        exc_message='Unable to find admin.'
    )


def authenticate_admin(db: Session, username: str, password: str):
    '''Authenticate admin credentials (username and password).'''
    admin = get_admin(db=db, username=username)
    if not admin or not SecureHash.verify(signature=password, hashed=admin.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return admin


async def get_current_admin(db: Session = Depends(get_db), token: str = Depends(OAUTH2_SCHEME)):
    '''Ensure admin JWT is valid.'''
    creds_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = JSONWebToken.decode(token)
        username = payload.get('username')
        if username is None:
            raise creds_exception
        token_data = AccessTokenData(username=username)
    except JWTError as e:
        raise creds_exception from e
    user = get_admin(db=db, username=token_data.username)
    return user


async def get_current_active_admin(current_admin: Admin = Depends(get_current_admin)):
    '''Ensure admin is active.'''
    if not current_admin.is_active:
        raise HTTPException(status_code=400, detail='Inactive user')
    return current_admin
