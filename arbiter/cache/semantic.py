# -*- coding: utf-8 -*-
"""语义缓存：TF-IDF 余弦相似度命中，相似问题直接复用上次结果。"""
import math
from collections import defaultdict

from ..utils.text import tokenize
from ..utils.hashing import feature_hash
from .ttl import TTLCache


def _cosine(a: dict, b: dict) -> float:
    if not a or not b:
        return 0.0
    common = set(a) & set(b)
    dot = sum(a[k] * b[k] for k in common)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


class SemanticCache(TTLCache):
    def __init__(self, capacity=1000, ttl_seconds=300.0, threshold=0.92, dim=65536):
        super().__init__(capacity, ttl_seconds)
        self.threshold = threshold
        self.dim = dim
        self._vecs = {}  # key -> vec

    def _vec(self, text: str):
        tf = defaultdict(float)
        for tok in tokenize(text):
            tf[feature_hash(tok, self.dim)] += 1.0
        return tf

    def put(self, key, value) -> None:
        super().put(key, value)
        self._vecs[key] = self._vec(key)

    def find(self, query: str):
        """返回相似度最高的缓存项 (key, value, sim)，低于阈值返回 None。"""
        qv = self._vec(query)
        best_key, best_val, best_sim = None, None, 0.0
        for key in self._cache._data:
            val = self.get(key)
            if val is None:
                continue
            sim = _cosine(qv, self._vecs.get(key, {}))
            if sim > best_sim:
                best_key, best_val, best_sim = key, val, sim
        if best_key is not None and best_sim >= self.threshold:
            return best_key, best_val, best_sim
        return None
