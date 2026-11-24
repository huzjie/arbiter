# -*- coding: utf-8 -*-
"""成本预算：单例阈值 + 记账。"""
from .account import BudgetAccount


class CostBudget(BudgetAccount):
    def __init__(self, max_cost: float):
        super().__init__(max_cost=max_cost)
