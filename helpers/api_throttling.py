'''This module manages the application throttling control.'''

from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address


class Throttling:
    '''Throttling limiter class.'''

    def enable(app: FastAPI) -> FastAPI:
        '''Enable a limiter to control the amount of requests per minute based on IP address.'''
        limiter = Limiter(key_func=get_remote_address, default_limits=['2/second', '20/minute',])
        app.state.limiter = limiter
        app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
        app.add_middleware(SlowAPIMiddleware)
        return app

    def disable(app: FastAPI) -> FastAPI:
        '''Disable throttling limiter.'''
        limiter = Limiter(key_func=get_remote_address, enabled=False)
        app.state.limiter = limiter
        return app
