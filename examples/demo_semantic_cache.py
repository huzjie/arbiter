# -*- coding: utf-8 -*-
"""语义缓存：相似问题直接复用结果。"""
from arbiter.cache.semantic import SemanticCache

c = SemanticCache(threshold=0.5)
c.put("我要退款", "refund")
found = c.find("我要退货")   # 语义相近，命中
print("hit:", found[1] if found else None)
