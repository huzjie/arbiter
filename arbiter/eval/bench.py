# -*- coding: utf-8 -*-
"""技能扫掠基准：决策模型 skill 从 0 扫到 1，观察各指标如何单调收敛。

这是「分层路由」最有说服力的验证：skill 越低，决策越不可靠 → 更多请求被
升级到贵 reasoner（成本省不下来）；skill 越高，决策越可信 → 更多请求就地
采纳（成本大幅下降），同时路由准确率始终被 reasoner 兜底保持在 1.0。
"""
from ..deciders import MockDecider
from ..router.base import Tier
from ..router.cascade import CascadeRouter
from .dataset import make_dataset
from .metrics import evaluate


def _make_router(skill: float, cost0=1.0, cost1=100.0, threshold=0.85):
    tiers = [
        Tier(name="decider", decider=MockDecider(skill=skill), cost=cost0,
             latency_ms=5.0, threshold=threshold),
        Tier(name="reasoner", decider=MockDecider(skill=1.0), cost=cost1,
             latency_ms=200.0),
    ]
    return CascadeRouter(tiers)


def bench_skill_sweep(seed="arbiter", steps=6, threshold=0.85):
    queries = make_dataset(seed=seed)
    rows = []
    for i in range(steps + 1):
        skill = round(i / steps, 4)
        router = _make_router(skill, threshold=threshold)
        m = evaluate(router, queries)
        m["skill"] = skill
        rows.append(m)
    return rows
