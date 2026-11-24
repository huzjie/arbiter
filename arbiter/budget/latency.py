# -*- coding: utf-8 -*-
"""延迟预算。"""
from .account import BudgetAccount


class LatencyBudget(BudgetAccount):
    def __init__(self, max_latency_ms: float):
        super().__init__(max_latency_ms=max_latency_ms)
