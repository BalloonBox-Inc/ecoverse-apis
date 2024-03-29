'''This module manages the HTTP Cross-Origin Resource Sharing (CORS) mechanism.'''

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


class CrossOrigin:
    '''FastAPI CORS class.'''

    def enable(app: FastAPI) -> FastAPI:
        '''Enable CORS to allow a server to indicate any origins from which a browser should permit loading resources.'''
        app.add_middleware(
            CORSMiddleware,
            allow_origins=['http://localhost:3000', 'http://localhost:8000'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*']
        )
        return app
