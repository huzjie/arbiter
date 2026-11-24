# -*- coding: utf-8 -*-
"""最小路由示例。"""
from arbiter.api import Arbiter

a = Arbiter()
for q in ["我要退款", "这个怎么用", "帮我开个发票", "随便聊聊"]:
    r = a.route(q)
    print(f"{q!r} -> {r.final_option} (tier={r.tier}, "
          f"conf={r.confidence:.3f}, cost_saved={r.cost_saved:.1%})")
