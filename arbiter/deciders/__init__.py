# -*- coding: utf-8 -*-
from .base import Decider, DeciderResult
from .mock import MockDecider
from .rule import RuleDecider
from .naive_bayes import NaiveBayesDecider
from .tfidf_linear import TfidfLinearDecider
from .threshold import ThresholdDecider
from .ensemble import EnsembleDecider
from .llm import LLMDecider

__all__ = [
    "Decider", "DeciderResult", "MockDecider", "RuleDecider",
    "NaiveBayesDecider", "TfidfLinearDecider", "ThresholdDecider",
    "EnsembleDecider", "LLMDecider",
]


def build(decider_type: str, **kw):
    """按类型名构造决策模型。"""
    t = decider_type.lower()
    if t == "mock":
        return MockDecider(**kw)
    if t == "rule":
        return RuleDecider(**kw)
    if t == "naive_bayes":
        return NaiveBayesDecider(**kw)
    if t == "tfidf":
        return TfidfLinearDecider(**kw)
    if t == "llm":
        return LLMDecider(**kw)
    raise ValueError(f"未知决策模型类型: {decider_type}")
