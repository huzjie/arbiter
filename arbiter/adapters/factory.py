# -*- coding: utf-8 -*-
"""provider 工厂。"""
from .mock import MockProvider
from .local import LocalProvider
from .openai import OpenAIProvider
from .anthropic import AnthropicProvider


def build_provider(ptype: str, **kw):
    t = (ptype or "mock").lower()
    if t == "mock":
        return MockProvider(**kw)
    if t == "local":
        return LocalProvider()
    if t in ("openai", "openai_compat"):
        return OpenAIProvider(**kw)
    if t == "anthropic":
        return AnthropicProvider(**kw)
    raise ValueError(f"未知 provider: {ptype}")
