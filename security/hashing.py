''' This module manages encryption authentication.'''

import hashlib
import hmac

from config import get_settings


settings = get_settings()


class SecureHash:
    '''Secure Hash Algorithm (SHA) class.'''

    def create(text: str):
        '''Create a encripted hash.'''
        key = settings.SECURITY.JWT_SECRET_KEY.encode('utf-8')
        return hmac.new(key=key, msg=text.encode('utf-8'), digestmod=hashlib.sha3_512).hexdigest()

    def verify(signature: str, hashed: str):
        '''Verify if signature-hashed pair is valid.'''
        return bool(hashed == SecureHash.create(signature))
