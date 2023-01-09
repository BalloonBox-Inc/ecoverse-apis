'''This module manages FastAPI exception messages.'''

from fastapi import HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class ResponseValidationError(Exception):
    '''Create a custom exception.'''

    def __init__(self, status_code: HTTPException, message: str):
        self.status_code = status_code
        self.message = message


async def request_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:  # pylint: disable=[W0613]
    '''Ensure that the parameters passed by the HTTP request follow the defined schemas.'''
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            dict(
                error=True,
                message={d['loc'][-1]: d['msg'] for d in exc.errors()}
            )
        )
    )


async def response_exception_handler(request: Request, exc: ResponseValidationError) -> JSONResponse:  # pylint: disable=[W0613]
    '''Ensure exception responses are standardized.'''
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(
            dict(
                error=True,
                message=exc.message
            )
        )
    )
