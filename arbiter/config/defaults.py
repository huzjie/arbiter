# -*- coding: utf-8 -*-
"""默认策略：单级 decider + 置信度门控，置信不够升级到 reasoner。"""

DEFAULT_POLICY = {
    "name": "default",
    "tiers": [
        {
            "name": "decider",
            "type": "mock",          # mock / rule / naive_bayes / tfidf / llm
            "skill": 0.95,           # mock 后端：决策准确率（0~1）
            "cost": 1,               # 单次调用成本（归一化单位）
            "latency_ms": 5,         # 单次调用延迟（ms）
            "threshold": 0.85,       # 置信度门控：top1 概率 >= 阈值才信任
            "temperature": 1.0,      # 决策 softmax 温度
        },
        {
            "name": "reasoner",
            "type": "mock",
            "skill": 1.0,            # reasoner 视为近完美（oracle）
            "cost": 100,             # 大模型贵 100x
            "latency_ms": 200,
        },
    ],
    "budget": {
        "enabled": False,
        "max_cost": 5000,            # 每次 route 的成本上限
        "max_latency_ms": 10000,
    },
    "cache": {
        "enabled": True,
        "backend": "lru",
        "capacity": 1000,
        "ttl_seconds": 300,
        "semantic_threshold": 0.92,  # 语义缓存命中相似度阈值
    },
    "intents": ["refund", "consult", "complaint", "order",
                "shipping", "invoice", "account", "cancel"],
}
