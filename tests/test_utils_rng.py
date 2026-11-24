# -*- coding: utf-8 -*-
import unittest

from arbiter.utils.rng import seed_from, deterministic_rand, deterministic_shuffle


class TestRng(unittest.TestCase):
    def test_deterministic(self):
        self.assertEqual(seed_from("a", "b"), seed_from("a", "b"))
        self.assertEqual(deterministic_rand("s", "k"), deterministic_rand("s", "k"))

    def test_range(self):
        for i in range(100):
            v = deterministic_rand("seed", i)
            self.assertGreaterEqual(v, 0.0)
            self.assertLess(v, 1.0)

    def test_shuffle_preserves_elements(self):
        items = [1, 2, 3, 4, 5]
        out = deterministic_shuffle("s", items)
        self.assertEqual(sorted(out), sorted(items))


if __name__ == "__main__":
    unittest.main()
