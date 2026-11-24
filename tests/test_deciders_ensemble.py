# -*- coding: utf-8 -*-
import unittest

from arbiter.deciders.ensemble import EnsembleDecider
from arbiter.deciders.mock import MockDecider
from arbiter.intents import INTENT_IDS


class TestEnsemble(unittest.TestCase):
    def test_ensemble_perfect(self):
        e = EnsembleDecider([MockDecider(skill=1.0), MockDecider(skill=1.0)])
        r = e.decide("我要退款", INTENT_IDS)
        self.assertEqual(r.top_option, "refund")


if __name__ == "__main__":
    unittest.main()
