# -*- coding: utf-8 -*-
"""规则决策模型：零成本、可解释。"""
from arbiter.deciders.rule import RuleDecider
from arbiter.intents import INTENT_IDS

d = RuleDecider()
r = d.decide("我要退款退货", INTENT_IDS)
print("top:", r.top_option, "probs:", dict(zip(r.options, [round(p, 3) for p in r.probs])))
