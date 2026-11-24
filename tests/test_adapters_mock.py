# -*- coding: utf-8 -*-
import json
import unittest

from arbiter.adapters.mock import MockProvider


class TestMockProvider(unittest.TestCase):
    def test_complete(self):
        p = MockProvider()
        out = p.complete("消息：我要退款")
        self.assertEqual(json.loads(out)["intent"], "refund")


if __name__ == "__main__":
    unittest.main()
