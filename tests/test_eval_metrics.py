# -*- coding: utf-8 -*-
import unittest

from arbiter.eval.metrics import evaluate
from arbiter.eval.bench import _make_router
from arbiter.eval.dataset import make_dataset


class TestMetrics(unittest.TestCase):
    def test_monotonic_cost_saved(self):
        queries = make_dataset()
        lo = evaluate(_make_router(0.3), queries)["avg_cost_saved"]
        hi = evaluate(_make_router(1.0), queries)["avg_cost_saved"]
        self.assertLess(lo, hi)

    def test_routing_accuracy_high(self):
        queries = make_dataset()
        m = evaluate(_make_router(1.0), queries)
        self.assertGreater(m["routing_accuracy"], 0.9)


if __name__ == "__main__":
    unittest.main()
