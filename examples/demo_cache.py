# -*- coding: utf-8 -*-
"""路由缓存：相同输入直接复用结果。"""
from arbiter.api import Arbiter

a = Arbiter()
r1 = a.route("我要退款")
r2 = a.route("我要退款")  # 命中缓存
print("first:", r1.final_option, "cache_hit:", r1.cache_hit)
print("second:", r2.final_option, "cache_hit:", r2.cache_hit)
