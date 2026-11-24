# -*- coding: utf-8 -*-
"""置信度门控包装：置信不够就标记「需要升级」，让上层路由升级到更贵的 tier。"""
from typing import Sequence

from .base import Decider, DeciderResult


class ThresholdDecider(Decider):
    name = "threshold"

    def __init__(self, base: Decider, threshold: float = 0.85):
        self.base = base
        self.threshold = threshold

    def decide(self, query: str, options: Sequence[str], temperature: float = 1.0) -> DeciderResult:
        r = self.base.decide(query, options, temperature)
        r.source = f"{self.base.name}:threshold"
        r.confidence = r.probs[r.top_index] if r.probs else 0.0
        r.needs_escalation = r.confidence < self.threshold
        return r

    def _score(self, query, options):
        return self.base._score(query, options)
