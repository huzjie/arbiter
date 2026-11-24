# -*- coding: utf-8 -*-
import unittest

from arbiter.cache.route_cache import RouteCache


class TestRouteCache(unittest.TestCase):
    def test_hit(self):
        c = RouteCache()
        c.put("q", ["a", "b"], "result")
        self.assertEqual(c.get("q", ["a", "b"]), "result")
        self.assertIsNone(c.get("q", ["a", "c"]))


if __name__ == "__main__":
    unittest.main()
