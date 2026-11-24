# -*- coding: utf-8 -*-
import unittest

from arbiter.cache.semantic import SemanticCache


class TestSemanticCache(unittest.TestCase):
    def test_similar_hit(self):
        c = SemanticCache(threshold=0.5)
        c.put("我要退款", "refund")
        found = c.find("我要退货")
        self.assertIsNotNone(found)
        self.assertEqual(found[1], "refund")


if __name__ == "__main__":
    unittest.main()
