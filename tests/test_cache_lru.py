# -*- coding: utf-8 -*-
import unittest

from arbiter.cache.lru import LRUCache


class TestLRU(unittest.TestCase):
    def test_eviction(self):
        c = LRUCache(capacity=2)
        c.put("a", 1)
        c.put("b", 2)
        c.get("a")  # 让 a 变最近
        c.put("c", 3)
        self.assertIsNone(c.get("b"))
        self.assertEqual(c.get("a"), 1)
        self.assertEqual(c.get("c"), 3)


if __name__ == "__main__":
    unittest.main()
