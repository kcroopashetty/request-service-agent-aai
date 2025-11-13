"""Simple in-memory cache for improved performance"""
from functools import wraps
from datetime import datetime, timedelta
from typing import Any, Callable

class SimpleCache:
    def __init__(self):
        self._cache = {}
        self._expiry = {}
    
    def get(self, key: str) -> Any:
        if key in self._cache:
            if datetime.now() < self._expiry.get(key, datetime.min):
                return self._cache[key]
            else:
                del self._cache[key]
                del self._expiry[key]
        return None
    
    def set(self, key: str, value: Any, ttl_seconds: int = 300):
        self._cache[key] = value
        self._expiry[key] = datetime.now() + timedelta(seconds=ttl_seconds)
    
    def clear(self):
        self._cache.clear()
        self._expiry.clear()

cache = SimpleCache()

def cached(ttl_seconds: int = 300):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            result = await func(*args, **kwargs)
            cache.set(cache_key, result, ttl_seconds)
            return result
        return wrapper
    return decorator
