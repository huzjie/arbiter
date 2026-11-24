# -*- coding: utf-8 -*-
import unittest

from arbiter.budget.pricing import Pricing


class TestPricing(unittest.TestCase):
    def test_default(self):
        p = Pricing()
        self.assertEqual(p.cost("reasoner"), 100)

    def test_custom(self):
        p = Pricing({"decider": {"cost": 5, "latency_ms": 1}})
        self.assertEqual(p.cost("decider"), 5)


if __name__ == "__main__":
    unittest.main()
