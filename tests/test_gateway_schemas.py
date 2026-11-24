# -*- coding: utf-8 -*-
import unittest

from arbiter.gateway.schemas import parse_request, route_response


class TestSchemas(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(parse_request('{"a": 1}'), {"a": 1})

    def test_parse_empty(self):
        self.assertEqual(parse_request(""), {})


if __name__ == "__main__":
    unittest.main()
