# -*- coding: utf-8 -*-
"""置信度门控：直观看到「置信不够 → 需要升级」。"""
from arbiter.deciders.threshold import ThresholdDecider
from arbiter.deciders.mock import MockDecider
from arbiter.intents import INTENT_IDS

for skill in (0.2, 0.9):
    t = ThresholdDecider(MockDecider(skill=skill), threshold=0.85)
    r = t.decide("随便说说", INTENT_IDS)
    print(f"skill={skill} conf={r.confidence:.3f} needs_escalation={r.needs_escalation}")
