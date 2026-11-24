# -*- coding: utf-8 -*-
import unittest

from arbiter.config.validator import validate_policy
from arbiter.utils.errors import ConfigError


class TestValidator(unittest.TestCase):
    def test_ok(self):
        validate_policy({"tiers": [{"name": "d", "type": "mock"}]})

    def test_missing_tiers(self):
        with self.assertRaises(ConfigError):
            validate_policy({})

    def test_bad_skill(self):
        with self.assertRaises(ConfigError):
            validate_policy({"tiers": [{"name": "d", "type": "mock", "skill": 2.0}]})


if __name__ == "__main__":
    unittest.main()
