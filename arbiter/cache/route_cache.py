# -*- coding: utf-8 -*-
"""路由缓存：相同输入直接复用上一次的完整路由结果（连决策都不跑）。"""
from .lru import LRUCache


class RouteCache:
    def __init__(self, capacity: int = 1000, key_fn=None):
        self._cache = LRUCache(capacity)
        self.key_fn = key_fn or (lambda query, options: (query, tuple(options)))

    def get(self, query, options):
        key = self.key_fn(query, options)
        return self._cache.get(key)

    def put(self, query, options, result) -> None:
        key = self.key_fn(query, options)
        self._cache.put(key, result)

    def __len__(self):
        return len(self._cache)
