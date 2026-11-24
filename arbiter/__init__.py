# -*- coding: utf-8 -*-
"""arbiter —— 分层决策路由网关（Hierarchical Decision Router）。

把「大模型负责推理、小决策模型负责高频判断」的分层架构，落成一个
零依赖、填配置就能跑的决策路由层：便宜的小决策模型在封闭选项集上
打分选路，置信度不够才升级到贵的大模型，从而把成本降下来、速度提上去。

对应热点：AWS Strands Decider v2 决策模型家族。
"""
from .version import __version__

__all__ = ["__version__", "route", "decide", "Arbiter"]


def _lazy():
    from .router.cascade import CascadeRouter
    return CascadeRouter


def route(query, options=None, policy=None, **kw):
    """便捷入口：一次调用完成「决策 + 路由」。"""
    from .api import Arbiter
    a = Arbiter(policy)
    return a.route(query, options, **kw)


def decide(query, options=None, **kw):
    """便捷入口：只在当前层做一次决策打分。"""
    from .api import Arbiter
    a = Arbiter()
    return a.decide(query, options, **kw)


__all__ = ["__version__", "route", "decide"]
