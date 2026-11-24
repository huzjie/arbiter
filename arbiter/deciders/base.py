# -*- coding: utf-8 -*-
"""决策模型抽象：在封闭选项集上打分，不生成文本。"""
from dataclasses import dataclass, field
from typing import List, Sequence

from ..utils.math_util import softmax


@dataclass
class DeciderResult:
    query: str
    options: List[str]
    scores: List[float] = field(default_factory=list)   # 原始分数（越大越像）
    probs: List[float] = field(default_factory=list)     # softmax 概率
    top_index: int = 0
    top_option: str = ""
    confidence: float = 0.0                               # top1 概率
    source: str = ""                                      # 决策模型来源

    def as_dict(self):
        return {
            "query": self.query,
            "options": self.options,
            "scores": self.scores,
            "probs": [round(p, 6) for p in self.probs],
            "top_index": self.top_index,
            "top_option": self.top_option,
            "confidence": round(self.confidence, 6),
            "source": self.source,
        }


class Decider:
    """决策模型基类。子类实现 _score(query, options) -> List[float]。"""

    name = "base"

    def decide(self, query: str, options: Sequence[str], temperature: float = 1.0) -> DeciderResult:
        opts = [str(o) for o in options]
        if not opts:
            return DeciderResult(query=query, options=[])
        scores = self._score(query, opts)
        probs = softmax(scores, temperature)
        top = max(range(len(probs)), key=lambda i: probs[i])
        return DeciderResult(
            query=query, options=opts, scores=scores, probs=probs,
            top_index=top, top_option=opts[top], confidence=probs[top],
            source=self.name,
        )

    def _score(self, query: str, options: List[str]) -> List[float]:
        raise NotImplementedError
