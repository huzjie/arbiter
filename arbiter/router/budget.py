# -*- coding: utf-8 -*-
"""预算路由：在成本/延迟预算约束下做级联。预算耗尽则不再升级、就地采纳。"""
from typing import List, Optional

from .base import Tier, RouteResult
from ..budget.account import BudgetAccount


class BudgetRouter:
    def __init__(self, tiers: List[Tier], budget: BudgetAccount = None):
        self.tiers = list(tiers)
        self.tiers[-1].is_final = True
        self.tiers[-1].threshold = 0.0
        self.budget = budget or BudgetAccount()
        self.full_cost = self.tiers[-1].cost
        self.full_latency_ms = self.tiers[-1].latency_ms

    def route(self, query: str, options: Optional[List[str]] = None) -> RouteResult:
        opts = [str(o) for o in options] if options else []
        res = RouteResult(query=query, options=opts,
                          full_cost=self.full_cost,
                          full_latency_ms=self.full_latency_ms)
        if not opts:
            return res
        for idx, tier in enumerate(self.tiers):
            # 预算检查：升级前先问「还付得起吗」
            if idx > 0 and not self.budget.can_afford(tier.cost, tier.latency_ms):
                # 预算耗尽：就地采纳当前已算出的最佳（上一层的决策）
                res.escalated = False
                res.tier = res.path[-1] if res.path else tier.name
                return res
            res.path.append(tier.name)
            res.cost += tier.cost
            res.latency_ms += tier.latency_ms
            self.budget.charge(tier.cost, tier.latency_ms)
            r = tier.decider.decide(query, opts)
            res.final_option = r.top_option
            res.final_index = r.top_index
            res.confidence = r.confidence
            if tier.is_final or r.confidence >= tier.threshold:
                res.tier = tier.name
                res.escalated = idx > 0
                return res
        return res
