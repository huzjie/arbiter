# -*- coding: utf-8 -*-
"""LLM 决策模型：调真实模型在封闭选项上打分（返回概率分布）。"""
from typing import List, Sequence

from .base import Decider, DeciderResult
from ..utils.math_util import softmax

_SCORING_PROMPT = (
    "你是意图分类器。给定用户消息，从下列选项中选择最合适的一个，"
    "并给出每个选项的匹配度分数（0-100）。只输出 JSON，形如 "
    '{"scores": {"选项A": 90, "选项B": 10}}。\n'
    "选项：{options}\n消息：{query}"
)


class LLMDecider(Decider):
    name = "llm"

    def __init__(self, provider, prompt: str = None, temperature: float = 1.0):
        self.provider = provider
        self.prompt = prompt or _SCORING_PROMPT
        self.temperature = temperature

    def _score(self, query: str, options: List[str]) -> List[float]:
        import json
        opts_text = ", ".join(options)
        prompt = self.prompt.format(options=opts_text, query=query)
        text = self.provider.complete(prompt)
        try:
            data = json.loads(text)
            raw = data.get("scores", data)
            scores = [float(raw.get(o, 0.0)) for o in options]
        except Exception:
            scores = [0.0] * len(options)
            scores[0] = 1.0
        return scores
