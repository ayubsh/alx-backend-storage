#!/usr/bin/env python3
"""Redis server"""
from typing import Union, Callable, Any
import uuid
import redis
from functools import wraps


def count_calls(method: Callable) -> Callable:
    '''keeps count of the number of calls made
    in cache
    '''
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        '''calls the given func
        after incr its call val
        '''
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return invoker

class Cache:
    def __init__(self):
        """initialses the redis store
        """
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """creates redis store
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Callable = None) -> Union[str, bytes, int, float]:
        """gets vlu from redis data storege
        """
        result = self._redis.get(key)
        if result is None:
            return None

        if fn is not None:
            return fn(result)

            return result

    def get_str(self, key: str) -> str:
        """gets str value from
        redis store
        """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """gets int value
        from redis store
        """
        return self.get(key, lambda x: int(x))
