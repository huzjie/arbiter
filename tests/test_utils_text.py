# -*- coding: utf-8 -*-
import unittest

from arbiter.utils.text import tokenize


class TestText(unittest.TestCase):
    def test_english(self):
        self.assertIn("refund", tokenize("refund my order"))

    def test_chinese_bigram(self):
        toks = tokenize("我要退款")
        self.assertIn("退款", toks)

    def test_stopword_removed(self):
        toks = tokenize("的")
        self.assertEqual(toks, [])


if __name__ == "__main__":
    unittest.main()
