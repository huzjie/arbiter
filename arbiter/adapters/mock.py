# -*- coding: utf-8 -*-
"""确定性 mock provider：离线验证网关/适配器链路，逐位可复现。"""
from ..utils.rng import seed_from
from ..intents import INTENTS
from .base import Provider


class MockProvider(Provider):
    name = "mock"

    def __init__(self, skill: float = 1.0, seed: str = "arbiter"):
        self.skill = skill
        self.seed = seed

    def complete(self, prompt: str, **kw) -> str:
        # 从 prompt 里挖出「消息」，返回其意图标签（模拟大模型分类输出）
        import json
        if "消息：" in prompt:
            query = prompt.split("消息：", 1)[1].strip().split("\n")[0].strip()
        else:
            query = prompt
        from ..intents import oracle_label
        label = oracle_label(query)
        return json.dumps({"intent": label, "label": INTENTS[label]["label"]},
                          ensure_ascii=False)
