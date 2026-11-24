# -*- coding: utf-8 -*-
import unittest

from arbiter.adapters.factory import build_provider


class TestFactory(unittest.TestCase):
    def test_mock(self):
        self.assertEqual(build_provider("mock").name, "mock")

    def test_local(self):
        self.assertEqual(build_provider("local").name, "local")


if __name__ == "__main__":
    unittest.main()
