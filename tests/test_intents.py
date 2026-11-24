# -*- coding: utf-8 -*-
import unittest

from arbiter.intents import INTENTS, INTENT_IDS, oracle_label, oracle_index


class TestIntents(unittest.TestCase):
    def test_oracle_label_refund(self):
        self.assertEqual(oracle_label("我要退款"), "refund")

    def test_oracle_label_consult(self):
        self.assertEqual(oracle_label("这个怎么用"), "consult")

    def test_oracle_index_maps(self):
        opts = list(INTENT_IDS)
        self.assertEqual(opts[oracle_index("我要退款", opts)], "refund")

    def test_intent_count(self):
        self.assertEqual(len(INTENT_IDS), 8)


if __name__ == "__main__":
    unittest.main()
