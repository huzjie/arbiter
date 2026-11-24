# -*- coding: utf-8 -*-
"""级联路由：便宜 tier 打分，置信不够逐级升级到更贵的 tier。

核心思想（对应 AWS Strands Decider 的「大模型推理 + 小决策模型高频判断」）：
- 小决策模型在封闭选项集上打分，top1 置信度 >= 阈值 → 直接采纳（便宜路径）；
- 置信度不足 → 升级到下一层更贵/更强的 tier，直到末层 reasoner 兜底。
"""
from typing import List, Optional

from .base import Tier, RouteResult
from ..utils.errors import RoutingError


class CascadeRouter:
    def __init__(self, tiers: List[Tier]):
        if not tiers:
            raise RoutingError("CascadeRouter 至少需要一个 tier")
        self.tiers = list(tiers)
        # 末层标记为 final（恒信任）
        self.tiers[-1].is_final = True
        self.tiers[-1].threshold = 0.0
        # 基线 = 所有请求都直接走末层 reasoner（不用决策模型）
        self.full_cost = self.tiers[-1].cost
        self.full_latency_ms = self.tiers[-1].latency_ms

    def route(self, query: str, options: Optional[List[str]] = None) -> RouteResult:
        opts = [str(o) for o in options] if options else []
        res = RouteResult(query=query, options=opts)
        res.full_cost = self.full_cost
        res.full_latency_ms = self.full_latency_ms
        if not opts:
            return res

        for idx, tier in enumerate(self.tiers):
            res.path.append(tier.name)
            res.cost += tier.cost
            res.latency_ms += tier.latency_ms
            r = tier.decider.decide(query, opts)
            if tier.is_final or r.confidence >= tier.threshold:
                res.final_option = r.top_option
                res.final_index = r.top_index
                res.confidence = r.confidence
                res.tier = tier.name
                res.escalated = idx > 0
                return res
        # 理论上不会走到这里（末层 is_final 恒返回）
        raise RoutingError("路由未终止：末层未标记为 final")
