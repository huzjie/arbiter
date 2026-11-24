# -*- coding: utf-8 -*-
import tempfile
import unittest

from arbiter.config.loader import load_config, merge_defaults


class TestConfigLoader(unittest.TestCase):
    def test_merge_defaults(self):
        merged = merge_defaults({"name": "x"})
        self.assertEqual(merged["name"], "x")
        self.assertIn("tiers", merged)

    def test_load_yaml(self):
        with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as f:
            f.write("name: test\ntiers:\n  - name: d\n    type: mock\n")
            path = f.name
        cfg = load_config(path)
        self.assertEqual(cfg["name"], "test")


if __name__ == "__main__":
    unittest.main()
