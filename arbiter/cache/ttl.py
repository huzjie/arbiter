# -*- coding: utf-8 -*-
"""TTL 缓存：带过期时间的 LRU。"""
import time

from .lru import LRUCache


class TTLCache:
    def __init__(self, capacity: int = 1000, ttl_seconds: float = 300.0):
        self._cache = LRUCache(capacity)
        self.ttl = ttl_seconds

    def get(self, key):
        entry = self._cache.get(key)
        if entry is None:
            return None
        val, expires = entry
        if time.time() > expires:
            return None
        return val

    def put(self, key, value) -> None:
        self._cache.put(key, (value, time.time() + self.ttl))

    def __len__(self):
        return len(self._cache)
