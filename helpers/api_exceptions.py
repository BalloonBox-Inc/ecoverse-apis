'''This module manages FastAPI exception messages.'''

from fastapi import HTTPException


class ExceptionFormatter(Exception):
    '''Create a custom exception.'''

    def __init__(self, status_code: HTTPException, message: str):
        self.status_code = status_code
        self.message = message
