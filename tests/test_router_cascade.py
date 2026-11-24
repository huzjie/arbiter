# -*- coding: utf-8 -*-
import unittest

from arbiter.router.base import Tier
from arbiter.router.cascade import CascadeRouter
from arbiter.deciders.mock import MockDecider
from arbiter.intents import INTENT_IDS


def _router(skill, threshold=0.85):
    return CascadeRouter([
        Tier("decider", MockDecider(skill=skill), cost=1, latency_ms=5, threshold=threshold),
        Tier("reasoner", MockDecider(skill=1.0), cost=100, latency_ms=200),
    ])


class TestCascadeRouter(unittest.TestCase):
    def test_no_escalation_when_confident(self):
        r = _router(1.0).route("我要退款", INTENT_IDS)
        self.assertEqual(r.tier, "decider")
        self.assertFalse(r.escalated)
        self.assertAlmostEqual(r.cost_saved, 0.99, places=2)

    def test_escalation_when_uncertain(self):
        r = _router(0.1).route("随便说说", INTENT_IDS)
        self.assertEqual(r.tier, "reasoner")
        self.assertTrue(r.escalated)

    def test_full_cost_is_reasoner(self):
        r = _router(1.0).route("我要退款", INTENT_IDS)
        self.assertEqual(r.full_cost, 100)


if __name__ == "__main__":
    unittest.main()
