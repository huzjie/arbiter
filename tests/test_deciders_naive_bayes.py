# -*- coding: utf-8 -*-
import unittest

from arbiter.deciders.naive_bayes import NaiveBayesDecider


class TestNaiveBayes(unittest.TestCase):
    def test_fit_predict(self):
        samples = [("我要退款", "refund"), ("退款流程", "refund"),
                   ("怎么使用", "consult"), ("使用说明", "consult")]
        d = NaiveBayesDecider().fit(samples)
        r = d.decide("怎么退款", ["refund", "consult"])
        self.assertEqual(r.top_option, "refund")


if __name__ == "__main__":
    unittest.main()
