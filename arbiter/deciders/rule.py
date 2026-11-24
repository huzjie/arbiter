# -*- coding: utf-8 -*-
"""规则决策模型：关键词命中打分。零成本、可解释、无训练。"""
from typing import List

from ..intents import INTENTS, INTENT_LABELS
from .base import Decider


class RuleDecider(Decider):
    name = "rule"

    def __init__(self, keyword_map=None):
        # 默认用内置意图关键词；可传入自定义 {option: [kw, ...]}
        self.keyword_map = keyword_map

    def _kw_for(self, opt: str) -> List[str]:
        if self.keyword_map:
            return self.keyword_map.get(opt, [])
        for iid, meta in INTENTS.items():
            if opt == iid or opt == meta["label"]:
                return meta["keywords"]
        return []

    def _score(self, query: str, options: List[str]) -> List[float]:
        scores = []
        for opt in options:
            kws = self._kw_for(opt)
            hit = sum(1 for kw in kws if kw in query)
            scores.append(float(hit))
        return scores
