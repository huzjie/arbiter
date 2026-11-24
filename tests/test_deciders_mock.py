# -*- coding: utf-8 -*-
import unittest

from arbiter.deciders.mock import MockDecider
from arbiter.intents import INTENT_IDS


class TestMockDecider(unittest.TestCase):
    def test_perfect_decider(self):
        d = MockDecider(skill=1.0)
        r = d.decide("我要退款", INTENT_IDS)
        self.assertEqual(r.top_option, "refund")
        self.assertGreater(r.confidence, 0.8)

    def test_confidence_monotonic_in_skill(self):
        lo = MockDecider(skill=0.1).decide("我要退款", INTENT_IDS).confidence
        hi = MockDecider(skill=0.9).decide("我要退款", INTENT_IDS).confidence
        self.assertLess(lo, hi)


if __name__ == "__main__":
    unittest.main()
