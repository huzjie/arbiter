# -*- coding: utf-8 -*-
"""预算约束路由：成本封顶时不再升级。"""
from arbiter.router.base import Tier
from arbiter.router.budget import BudgetRouter
from arbiter.budget.account import BudgetAccount
from arbiter.deciders.mock import MockDecider
from arbiter.intents import INTENT_IDS

budget = BudgetAccount(max_cost=10)  # 只够便宜层
router = BudgetRouter([
    Tier("decider", MockDecider(skill=0.5), cost=1, latency_ms=5, threshold=0.85),
    Tier("reasoner", MockDecider(skill=1.0), cost=100, latency_ms=200),
], budget)
r = router.route("随便聊聊", INTENT_IDS)
print("tier:", r.tier, "escalated:", r.escalated, "cost:", r.cost)
