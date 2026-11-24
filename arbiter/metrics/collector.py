# -*- coding: utf-8 -*-
"""指标收集：把路由过程的关键量记下来。"""
from .counter import Counter
from .latency_hist import LatencyHistogram


class MetricsCollector:
    def __init__(self):
        self.routes = Counter()
        self.escalations = Counter()
        self.cache_hits = Counter()
        self.cost_spent = 0.0
        self.latency = LatencyHistogram()

    def record(self, result):
        self.routes.inc()
        if result.escalated:
            self.escalations.inc()
        if result.cache_hit:
            self.cache_hits.inc()
        self.cost_spent += result.cost
        self.latency.observe(result.latency_ms)

    def snapshot(self):
        n = self.routes.value
        return {
            "routes": n,
            "escalation_rate": round(self.escalations.value / n, 4) if n else 0.0,
            "cache_hit_rate": round(self.cache_hits.value / n, 4) if n else 0.0,
            "total_cost": round(self.cost_spent, 2),
            "avg_latency_ms": round(self.latency.avg, 2),
        }
