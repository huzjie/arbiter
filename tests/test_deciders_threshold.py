# -*- coding: utf-8 -*-
import unittest

from arbiter.deciders.threshold import ThresholdDecider
from arbiter.deciders.mock import MockDecider
from arbiter.intents import INTENT_IDS


class TestThreshold(unittest.TestCase):
    def test_escalation_flag(self):
        base = MockDecider(skill=0.2)
        t = ThresholdDecider(base, threshold=0.9)
        r = t.decide("随便说说", INTENT_IDS)
        self.assertTrue(r.needs_escalation)


if __name__ == "__main__":
    unittest.main()
