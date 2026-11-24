# -*- coding: utf-8 -*-
"""评估指标：路由准确率、决策准确率、成本节省、速度提升、升级率。"""
from ..intents import INTENT_IDS


def evaluate(router, queries) -> dict:
    """queries: [(query, true_label), ...]。"""
    n = len(queries)
    if n == 0:
        return {}
    opts = list(INTENT_IDS)
    routing_correct = 0
    decision_correct = 0
    escalated = 0
    total_cost = 0.0
    total_full = 0.0
    total_lat = 0.0
    total_full_lat = 0.0
    cache_hits = 0

    for query, true in queries:
        res = router.route(query, opts)
        routing_correct += 1 if res.options[res.final_index] == true else 0
        if res.path:
            first = router.tiers[0].decider.decide(query, opts)
            decision_correct += 1 if first.top_option == true else 0
        escalated += 1 if res.escalated else 0
        total_cost += res.cost
        total_full += res.full_cost
        total_lat += res.latency_ms
        total_full_lat += res.full_latency_ms
        cache_hits += 1 if res.cache_hit else 0

    return {
        "n_queries": n,
        "routing_accuracy": round(routing_correct / n, 6),
        "decision_accuracy": round(decision_correct / n, 6),
        "escalation_rate": round(escalated / n, 6),
        "avg_cost_saved": round(max(0.0, 1.0 - total_cost / total_full), 6) if total_full else 0.0,
        "avg_speedup": round(total_full_lat / total_lat, 6) if total_lat else 0.0,
        "cache_hit_rate": round(cache_hits / n, 6),
    }
