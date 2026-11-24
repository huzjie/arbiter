# -*- coding: utf-8 -*-
import unittest

from arbiter.api import Arbiter


class TestApi(unittest.TestCase):
    def test_route(self):
        a = Arbiter()
        r = a.route("我要退款")
        self.assertEqual(r.final_option, "refund")

    def test_cache_hit(self):
        a = Arbiter()
        r1 = a.route("我要退款")
        r2 = a.route("我要退款")
        self.assertTrue(r2.cache_hit)

    def test_decide(self):
        a = Arbiter()
        r = a.decide("我要退款")
        self.assertEqual(r.top_option, "refund")


if __name__ == "__main__":
    unittest.main()
