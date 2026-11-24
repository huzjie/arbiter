# -*- coding: utf-8 -*-
"""路由抽象：Tier 定义 + RouteResult 结果结构。"""
from dataclasses import dataclass, field
from typing import List


@dataclass
class Tier:
    name: str
    decider: object = None               # 决策模型（Decider）
    cost: float = 1.0                    # 单次调用成本（归一化）
    latency_ms: float = 5.0              # 单次调用延迟
    threshold: float = 0.85              # 置信度门控（末层忽略）
    is_final: bool = False               # 末层（reasoner），恒信任

    @property
    def is_terminal(self) -> bool:
        return self.is_final


@dataclass
class RouteResult:
    query: str
    options: List[str]
    final_option: str = ""
    final_index: int = 0
    confidence: float = 0.0
    tier: str = ""                       # 最终由哪一层拍板
    path: List[str] = field(default_factory=list)   # 经过的 tier 序列
    escalated: bool = False              # 是否离开了首层
    cost: float = 0.0                    # 实际总成本
    latency_ms: float = 0.0              # 实际总延迟
    full_cost: float = 0.0               # 全走末层的成本
    full_latency_ms: float = 0.0
    cache_hit: bool = False

    @property
    def cost_saved(self) -> float:
        if self.full_cost <= 0:
            return 0.0
        return round(max(0.0, 1.0 - self.cost / self.full_cost), 6)

    @property
    def speedup(self) -> float:
        if self.latency_ms <= 0:
            return 0.0
        return round(self.full_latency_ms / self.latency_ms, 6)

    def as_dict(self):
        return {
            "query": self.query,
            "options": self.options,
            "final_option": self.final_option,
            "final_index": self.final_index,
            "confidence": round(self.confidence, 6),
            "tier": self.tier,
            "path": self.path,
            "escalated": self.escalated,
            "cost": self.cost,
            "latency_ms": self.latency_ms,
            "full_cost": self.full_cost,
            "cost_saved": self.cost_saved,
            "speedup": self.speedup,
            "cache_hit": self.cache_hit,
        }
