# -*- coding: utf-8 -*-
import unittest

from arbiter.policy.loader import parse_tiers


class TestPolicyLoader(unittest.TestCase):
    def test_parse_tiers(self):
        tiers = parse_tiers({"tiers": [{"name": "d", "type": "mock"}]})
        self.assertEqual(len(tiers), 1)


if __name__ == "__main__":
    unittest.main()
