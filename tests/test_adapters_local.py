# -*- coding: utf-8 -*-
import json
import unittest

from arbiter.adapters.local import LocalProvider


class TestLocalProvider(unittest.TestCase):
    def test_complete(self):
        p = LocalProvider()
        out = p.complete("消息：帮我开发票")
        self.assertEqual(json.loads(out)["intent"], "invoice")


if __name__ == "__main__":
    unittest.main()
