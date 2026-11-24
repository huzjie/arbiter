# -*- coding: utf-8 -*-
from ..config.loader import load_config, merge_defaults
from ..config.validator import validate_policy


def load(path: str) -> dict:
    cfg = load_config(path)
    policy = cfg.get("policy", cfg)
    return merge_defaults(policy)


def parse_tiers(policy: dict) -> list:
    validate_policy(policy)
    return policy["tiers"]
