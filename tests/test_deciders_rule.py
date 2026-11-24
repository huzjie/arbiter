# -*- coding: utf-8 -*-
import unittest

from arbiter.deciders.rule import RuleDecider
from arbiter.intents import INTENT_IDS


class TestRuleDecider(unittest.TestCase):
    def test_keyword_hit(self):
        d = RuleDecider()
        r = d.decide("我要退款退货", INTENT_IDS)
        self.assertEqual(r.top_option, "refund")

    def test_no_hit_uniform(self):
        d = RuleDecider()
        r = d.decide("随便说点什么", INTENT_IDS)
        self.assertEqual(len(r.probs), len(INTENT_IDS))


if __name__ == "__main__":
    unittest.main()
