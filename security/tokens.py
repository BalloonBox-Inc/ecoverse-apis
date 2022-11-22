'''This module manages the creation of JWTs.'''

from datetime import datetime, timedelta
from jose import jwt

from config import get_settings


settings = get_settings()


class JSONWebToken:
    '''JSON Web Token (JWT) class.'''

    def create(data: dict):
        '''Create a JWT token.'''
        expire = datetime.utcnow() + timedelta(minutes=int(settings.SECURITY.JWT_EXPIRE_MINUTES))
        to_encode = data.copy()
        to_encode.update({'exp': expire})
        return jwt.encode(to_encode, settings.SECURITY.JWT_SECRET_KEY, algorithm=settings.SECURITY.JWT_ALGORITHM)

    def decode(token: str):
        '''Decode a JWT token.'''
        return jwt.decode(token, settings.SECURITY.JWT_SECRET_KEY, algorithms=[settings.SECURITY.JWT_ALGORITHM])
