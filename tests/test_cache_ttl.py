# -*- coding: utf-8 -*-
import unittest
import time

from arbiter.cache.ttl import TTLCache


class TestTTL(unittest.TestCase):
    def test_expiry(self):
        c = TTLCache(ttl_seconds=0.05)
        c.put("a", 1)
        self.assertEqual(c.get("a"), 1)
        time.sleep(0.06)
        self.assertIsNone(c.get("a"))


if __name__ == "__main__":
    unittest.main()
