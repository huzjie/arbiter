# -*- coding: utf-8 -*-
import math


def softmax(scores, temperature=1.0):
    """数值稳定的 softmax。temperature 越大分布越平。"""
    if temperature <= 0:
        temperature = 1e-6
    xs = [s / temperature for s in scores]
    m = max(xs)
    exps = [math.exp(x - m) for x in xs]
    total = sum(exps)
    if total == 0:
        n = len(scores)
        return [1.0 / n] * n
    return [e / total for e in exps]
