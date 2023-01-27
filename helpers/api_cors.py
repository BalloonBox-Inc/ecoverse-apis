'''This module manages the HTTP Cross-Origin Resource Sharing (CORS) mechanism.'''

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


class CrossOrigin:
    '''FastAPI CORS class.'''

    def enable(app: FastAPI) -> FastAPI:
        '''Enable CORS to allow a server to indicate any origins from which a browser should permit loading resources.'''
        app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['GET', 'POST'],
            allow_headers=['Content-Type']
        )
        return app
