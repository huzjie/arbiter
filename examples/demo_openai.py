# -*- coding: utf-8 -*-
"""接真实 OpenAI 兼容模型（把 decider/reasoner 换成真实 provider）。

使用前设置环境变量 OPENAI_BASE_URL / OPENAI_API_KEY，或改下面的参数。
"""
import os

from arbiter.api import Arbiter
from arbiter.adapters.openai import OpenAIProvider
from arbiter.deciders.llm import LLMDecider
from arbiter.router.base import Tier
from arbiter.router.cascade import CascadeRouter

# 用同一个 provider 构造小决策模型与大兜底模型
small = LLMDecider(OpenAIProvider(model=os.environ.get("SMALL_MODEL", "gpt-4o-mini")))
large = LLMDecider(OpenAIProvider(model=os.environ.get("LARGE_MODEL", "gpt-4o")))

router = CascadeRouter([
    Tier("decider", small, cost=10, latency_ms=40, threshold=0.85),
    Tier("reasoner", large, cost=100, latency_ms=300),
])
r = router.route("我要退款", ["refund", "consult", "invoice"])
print("final:", r.final_option, "tier:", r.tier)
