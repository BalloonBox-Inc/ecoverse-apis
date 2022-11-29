'''This module initiates the FastAPI application and the Database session.'''

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi_pagination import add_pagination

from config import get_settings
from apis.middleware import api_routers
from database.startup import start_database
from helpers.api_routers import APIRouters
from helpers.api_throttling import Throttling
from helpers.api_exceptions import ResponseValidationError, request_exception_handler, response_exception_handler


def start_application():
    '''Initiate the FastAPI application.'''

    settings = get_settings()

    app = FastAPI(title=settings.APP.PROJECT_NAME, version=settings.APP.PROJECT_VERSION)
    app = Throttling.enable(app)
    app = APIRouters.include(app, api_routers)

    app.add_exception_handler(RequestValidationError, request_exception_handler)
    app.add_exception_handler(ResponseValidationError, response_exception_handler)

    add_pagination(app)
    start_database()

    return app


app = start_application()
