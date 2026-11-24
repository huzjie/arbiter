# -*- coding: utf-8 -*-
"""集成决策：多模型投票降噪。"""
from arbiter.deciders.ensemble import EnsembleDecider
from arbiter.deciders.mock import MockDecider
from arbiter.deciders.rule import RuleDecider
from arbiter.intents import INTENT_IDS

e = EnsembleDecider([RuleDecider(), MockDecider(skill=0.9), MockDecider(skill=0.9)])
r = e.decide("我要退款", INTENT_IDS)
print("ensemble ->", r.top_option, round(r.confidence, 3))
