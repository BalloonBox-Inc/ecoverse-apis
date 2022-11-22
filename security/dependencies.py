'''This module manages global application dependencies.'''

import json
from fastapi import Request


async def verify_request_content(request: Request):
    '''Ensure request content is JSON serializable.'''

    try:
        _json = await request.json()
    except json.decoder.JSONDecodeError:
        _json = None
    return _json
