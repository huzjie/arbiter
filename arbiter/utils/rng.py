# -*- coding: utf-8 -*-
"""确定性随机：md5(key) 前 8 字节做种子，全项目逐位可复现。"""
import hashlib


def seed_from(*parts) -> int:
    h = hashlib.md5()
    for p in parts:
        h.update(str(p).encode("utf-8"))
    return int.from_bytes(h.digest()[:8], "big")


def deterministic_rand(seed, *parts) -> float:
    """返回 [0,1) 的确定性伪随机数，同一 (seed, parts) 恒等。"""
    s = seed_from(seed, *parts)
    return (s % 1000000) / 1000000.0


def deterministic_shuffle(seed, items):
    """Fisher-Yates，用确定性随机，返回新列表。"""
    arr = list(items)
    for i in range(len(arr) - 1, 0, -1):
        j = int(deterministic_rand(seed, "shuffle", i) * (i + 1))
        arr[i], arr[j] = arr[j], arr[i]
    return arr
