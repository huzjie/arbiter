# -*- coding: utf-8 -*-
"""集成决策：多个决策模型投票/平均，降低单模型噪声。"""
from typing import List, Sequence

from .base import Decider, DeciderResult
from ..utils.math_util import softmax


class EnsembleDecider(Decider):
    name = "ensemble"

    def __init__(self, members: List[Decider], weights: List[float] = None):
        self.members = members
        self.weights = weights or [1.0] * len(members)

    def decide(self, query: str, options: Sequence[str], temperature: float = 1.0) -> DeciderResult:
        opts = [str(o) for o in options]
        n = len(opts)
        agg = [0.0] * n
        for m, w in zip(self.members, self.weights):
            r = m.decide(query, opts, temperature)
            for i, p in enumerate(r.probs):
                agg[i] += w * p
        probs = softmax(agg, temperature)
        top = max(range(n), key=lambda i: probs[i])
        return DeciderResult(query=query, options=opts, probs=probs,
                             top_index=top, top_option=opts[top],
                             confidence=probs[top], source=self.name)

    def _score(self, query, options):
        return [0.0] * len(options)
