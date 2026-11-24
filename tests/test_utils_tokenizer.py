# -*- coding: utf-8 -*-
import unittest

from arbiter.utils.tokenizer import estimate_tokens


class TestTokenizer(unittest.TestCase):
    def test_chinese_one_char_one_token(self):
        self.assertEqual(estimate_tokens("你好"), 2)

    def test_empty(self):
        self.assertEqual(estimate_tokens(""), 0)

    def test_english(self):
        self.assertGreater(estimate_tokens("hello world"), 0)


if __name__ == "__main__":
    unittest.main()
