# -*- coding: utf-8 -*-
"""预算账户：记账成本/延迟消耗，判断是否可继续升级。"""
from dataclasses import dataclass, field


@dataclass
class BudgetAccount:
    max_cost: float = float("inf")
    max_latency_ms: float = float("inf")
    spent_cost: float = 0.0
    spent_latency_ms: float = 0.0
    n_calls: int = 0
    history: list = field(default_factory=list)

    def can_afford(self, cost: float, latency_ms: float) -> bool:
        if self.spent_cost + cost > self.max_cost:
            return False
        if self.spent_latency_ms + latency_ms > self.max_latency_ms:
            return False
        return True

    def charge(self, cost: float, latency_ms: float) -> None:
        self.spent_cost += cost
        self.spent_latency_ms += latency_ms
        self.n_calls += 1
        self.history.append({"cost": cost, "latency_ms": latency_ms})

    def reset(self) -> None:
        self.spent_cost = 0.0
        self.spent_latency_ms = 0.0
        self.n_calls = 0
        self.history = []

    @property
    def remaining_cost(self) -> float:
        return max(0.0, self.max_cost - self.spent_cost)

    @property
    def remaining_latency_ms(self) -> float:
        return max(0.0, self.max_latency_ms - self.spent_latency_ms)
