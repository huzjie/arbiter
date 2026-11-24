# -*- coding: utf-8 -*-
"""特征哈希：把任意 token 稳定映射到 [0, dim)。"""
import hashlib


def feature_hash(token: str, dim: int = 65536) -> int:
    h = hashlib.md5(token.encode("utf-8")).digest()
    return int.from_bytes(h[:8], "big") % dim
