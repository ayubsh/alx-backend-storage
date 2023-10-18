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

def call_history(method: Callable) -> Callable:
    '''call history
    '''
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        '''calls keeps track of call history
        '''
        in_key = '{}:inputs'.format(method.__qualname__)
        out_key = '{}:outputs'.format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(in_key, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(out_key, output)
        return output
    return invoker

def replay(fn: Callable) -> None:
    '''function to display the history of
    calls of a particular function
    '''
    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_store = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    fxn_name = fn.__qualname__
    in_key = '{}:inputs'.format(fxn_name)
    out_key = '{}:outputs'.format(fxn_name)
    fxn_call_count = 0
    if redis_store.exists(fxn_name) != 0:
        fxn_call_count = int(redis_store.get(fxn_name))
    print('{} was called {} times:'.format(fxn_name, fxn_call_count))
    fxn_inputs = redis_store.lrange(in_key, 0, -1)
    fxn_outputs = redis_store.lrange(out_key, 0, -1)
    for fxn_input, fxn_output in zip(fxn_inputs, fxn_outputs):
        print('{}(*{}) -> {}'.format(
            fxn_name,
            fxn_input.decode("utf-8"),
            fxn_output,
        ))

class Cache:
    def __init__(self):
        """initialses the redis store
        """
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @count_calls
    @call_history
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
