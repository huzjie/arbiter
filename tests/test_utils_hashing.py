# -*- coding: utf-8 -*-
import unittest

from arbiter.utils.hashing import feature_hash


class TestHashing(unittest.TestCase):
    def test_stable(self):
        self.assertEqual(feature_hash("abc"), feature_hash("abc"))

    def test_in_range(self):
        self.assertLess(feature_hash("xyz", 1024), 1024)


if __name__ == "__main__":
    unittest.main()
