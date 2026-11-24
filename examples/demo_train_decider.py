# -*- coding: utf-8 -*-
"""训练决策模型：朴素贝叶斯 / TF-IDF。"""
from arbiter.deciders.naive_bayes import NaiveBayesDecider
from arbiter.deciders.tfidf_linear import TfidfLinearDecider

samples = [
    ("我要退款", "refund"), ("退货退款", "refund"), ("退款流程", "refund"),
    ("怎么使用", "consult"), ("使用说明", "consult"), ("怎么操作", "consult"),
    ("开发票", "invoice"), ("报销发票", "invoice"), ("发票抬头", "invoice"),
]

for cls in (NaiveBayesDecider, TfidfLinearDecider):
    d = cls().fit(samples)
    r = d.decide("我要申请退款", ["refund", "consult", "invoice"])
    print(cls.__name__, "->", r.top_option, round(r.confidence, 3))
