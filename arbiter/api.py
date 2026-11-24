# -*- coding: utf-8 -*-
"""Arbiter 门面：把策略配置组装成可调用的路由网关。"""
from .config.defaults import DEFAULT_POLICY
from .config.loader import merge_defaults
from .config.validator import validate_policy
from .deciders import build as build_decider
from .router.base import Tier
from .router.cascade import CascadeRouter
from .cache.route_cache import RouteCache


class Arbiter:
    def __init__(self, policy=None):
        self.policy = merge_defaults(policy or {})
        validate_policy(self.policy)
        self.tiers = []
        for t in self.policy["tiers"]:
            self.tiers.append(Tier(
                name=t["name"],
                decider=build_decider(t.get("type", "mock"),
                                      skill=t.get("skill", 0.9)),
                cost=float(t.get("cost", 1.0)),
                latency_ms=float(t.get("latency_ms", 5.0)),
                threshold=float(t.get("threshold", 0.85)),
            ))
        self.router = CascadeRouter(self.tiers)
        cache_cfg = self.policy.get("cache", {})
        self.cache = RouteCache(capacity=cache_cfg.get("capacity", 1000))             if cache_cfg.get("enabled", True) else None

    @property
    def intents(self):
        return list(self.policy.get("intents", []))

    def route(self, query, options=None, **kw):
        opts = list(options) if options else self.intents
        if self.cache is not None:
            hit = self.cache.get(query, opts)
            if hit is not None:
                hit.cache_hit = True
                return hit
        res = self.router.route(query, opts)
        if self.cache is not None:
            self.cache.put(query, opts, res)
        return res

    def decide(self, query, options=None, **kw):
        opts = list(options) if options else self.intents
        return self.tiers[0].decider.decide(query, opts)
