# -*- coding: utf-8 -*-
"""各 tier 定价：把「成本/延迟」从代码里抽出来，方便按真实模型报价调整。"""

DEFAULT_PRICING = {
    "decider": {"cost": 1, "latency_ms": 5},
    "reasoner": {"cost": 100, "latency_ms": 200},
    "llm-small": {"cost": 10, "latency_ms": 40},
    "llm-large": {"cost": 100, "latency_ms": 300},
}


class Pricing:
    def __init__(self, table=None):
        self.table = dict(table or DEFAULT_PRICING)

    def cost(self, tier_name: str) -> float:
        return self.table.get(tier_name, {}).get("cost", 1.0)

    def latency_ms(self, tier_name: str) -> float:
        return self.table.get(tier_name, {}).get("latency_ms", 5.0)
