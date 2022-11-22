'''This module manages the FastAPI routers.'''

from fastapi import FastAPI, APIRouter


class APIRouters:
    '''FastAPI routers class.'''

    def include(app: FastAPI, routers: APIRouter):
        '''Add routers to the FastAPI framework.'''
        app.include_router(routers)
        return app
