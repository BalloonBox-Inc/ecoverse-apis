'''This module uses the lru_cache decorator to create an object only once, instead of doing it for each request.
Learn more at https://fastapi.tiangolo.com/it/advanced/settings/#creating-the-settings-only-once-with-lru_cache'''

from typing import Any, Callable, TypeVar
from functools import lru_cache, wraps
from datetime import datetime, timedelta


T = TypeVar('T')


def timed_lru_cache(seconds: int, maxsize: int = 128) -> Callable[..., Callable[..., T]]:
    '''Set up a refresh time and space for the lru_cache decorator.'''

    def decorator(func: Any) -> Any:
        '''Wrap the decorated function with the lru_cache decorator.'''
        func = lru_cache(maxsize=maxsize)(func)
        func.lifetime = timedelta(seconds=seconds)
        func.expiration = datetime.utcnow() + func.lifetime

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            '''Before accessing an entry in the cache, it clears the cache and
            recomputes the lifetime and expiration date if the current date is past the expiration date.'''
            if datetime.utcnow() >= func.expiration:
                func.cache_clear()
                func.expiration = datetime.utcnow() + func.lifetime
            return func(*args, **kwargs)
        return wrapper
    return decorator
