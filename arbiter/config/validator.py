# -*- coding: utf-8 -*-
"""策略校验：字段存在性 + 取值范围。"""
from ..utils.errors import ConfigError

_VALID_DECIDER_TYPES = {"mock", "rule", "naive_bayes", "tfidf", "llm"}


def validate_policy(policy: dict) -> None:
    if not isinstance(policy, dict):
        raise ConfigError("policy 必须是 dict")
    tiers = policy.get("tiers")
    if not tiers or not isinstance(tiers, list) or len(tiers) < 1:
        raise ConfigError("policy.tiers 至少需要一个 tier")
    for i, t in enumerate(tiers):
        if not isinstance(t, dict):
            raise ConfigError(f"tier[{i}] 必须是 dict")
        if not t.get("name"):
            raise ConfigError(f"tier[{i}] 缺少 name")
        tt = t.get("type", "mock")
        if tt not in _VALID_DECIDER_TYPES:
            raise ConfigError(f"tier[{i}].type 非法: {tt}")
        if "skill" in t and not (0.0 <= float(t["skill"]) <= 1.0):
            raise ConfigError(f"tier[{i}].skill 必须在 [0,1]")
        if "threshold" in t and not (0.0 <= float(t["threshold"]) <= 1.0):
            raise ConfigError(f"tier[{i}].threshold 必须在 [0,1]")
