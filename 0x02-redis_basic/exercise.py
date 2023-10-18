#!/usr/bin/env python3
"""Redis server"""
from typing import Union
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
