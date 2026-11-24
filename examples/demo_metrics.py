# -*- coding: utf-8 -*-
"""可观测指标：记录路由过程。"""
from arbiter.api import Arbiter
from arbiter.metrics.collector import MetricsCollector

a = Arbiter()
m = MetricsCollector()
for q in ["我要退款", "这个怎么用", "随便聊聊", "帮我开发票"]:
    r = a.route(q)
    m.record(r)
print(m.snapshot())
