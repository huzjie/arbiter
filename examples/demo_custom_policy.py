# -*- coding: utf-8 -*-
"""自定义策略：多级 tier + 阈值 + 预算。"""
from arbiter.api import Arbiter

policy = {
    "tiers": [
        {"name": "rules", "type": "rule", "cost": 0, "latency_ms": 1, "threshold": 0.9},
        {"name": "small", "type": "mock", "skill": 0.9, "cost": 10, "latency_ms": 40, "threshold": 0.85},
        {"name": "large", "type": "mock", "skill": 1.0, "cost": 100, "latency_ms": 300},
    ],
    "intents": ["refund", "consult", "complaint", "order",
                "shipping", "invoice", "account", "cancel"],
}
a = Arbiter(policy)
r = a.route("我要退款")
print("final:", r.final_option, "path:", r.path, "cost_saved:", r.cost_saved)
