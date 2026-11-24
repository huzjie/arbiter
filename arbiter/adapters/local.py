# -*- coding: utf-8 -*-
"""本地规则 provider：零网络、零密钥，用规则引擎出结果。"""
from ..intents import INTENTS, oracle_label
from .base import Provider


class LocalProvider(Provider):
    name = "local"

    def complete(self, prompt: str, **kw) -> str:
        import json
        if "消息：" in prompt:
            query = prompt.split("消息：", 1)[1].strip().split("\n")[0].strip()
        else:
            query = prompt
        label = oracle_label(query)
        return json.dumps({"intent": label, "label": INTENTS[label]["label"]},
                          ensure_ascii=False)
