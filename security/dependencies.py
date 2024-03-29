'''This module manages global application dependencies.'''

import json
from fastapi import Request, status

from helpers.api_exceptions import ResponseValidationError


async def verify_request_content(request: Request):
    '''Ensure request content is JSON serializable.'''

    try:
        _json = await request.json()
    except json.decoder.JSONDecodeError:
        _json = None
    return _json


async def valid_farm_id(request: Request):
    '''Ensure farmId parameter is valid.'''

    try:
        return int(request.path_params['farmId'])
    except ValueError as exc:
        raise ResponseValidationError(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message={'farmId': 'value is not a valid string number'}
        ) from exc
