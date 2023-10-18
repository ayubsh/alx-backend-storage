#!/usr/bin/env python3
"""Redis server"""
from typing import Union, Callable
import uuid
import redis


class Cache:
    def __init__(self):
        """initialses the redis store
        """
        self._redis = redis.Redis()
        self._redis.flushdb(True)

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
