# -*- coding: utf-8 -*-
"""确定性 mock 决策模型：模拟一个「准确率=skill、置信度随 skill 校准」的分类器。

这是「不接真实模型也能验证整条链路」的关键设计：
- 正确性：以概率 skill 选对真实标签（否则选一个确定性错误项），
  故 decision_accuracy 随 skill 严格单调上升；
- 置信度：conf = 1/N + (1-1/N)*skill，随 skill 单调上升（越强越敢拍板）；
- 二者分开建模——真实模型里「准」与「自信」本就相关但非同一件事，
  置信度门控路由正是靠「不自信就升级」来兜住低 skill 时的错误。
"""
import math
from typing import List

from ..utils.rng import deterministic_rand
from ..intents import oracle_index
from .base import Decider


class MockDecider(Decider):
    name = "mock"

    def __init__(self, skill: float = 0.9, seed: str = "arbiter"):
        self.skill = max(0.0, min(1.0, float(skill)))
        self.seed = seed

    def _score(self, query: str, options: List[str]) -> List[float]:
        n = len(options)
        true = oracle_index(query, options)
        # 正确性硬币：以概率 skill 选对
        coin = deterministic_rand(self.seed, query, "coin")
        if coin < self.skill:
            chosen = true
        else:
            wrongs = [i for i in range(n) if i != true]
            chosen = wrongs[int(deterministic_rand(self.seed, query, "wrong") * len(wrongs)) % len(wrongs)]
        # 置信度目标（随 skill 单调升，加少量确定性抖动让升级率平滑）
        conf = 1.0 / n + (1.0 - 1.0 / n) * self.skill
        conf += (deterministic_rand(self.seed, query, "conf") - 0.5) * 0.08
        conf = min(0.99, max(1.0 / n, conf))
        # 把置信度反解成 logit 边际，使 softmax 后 top1 概率 ≈ conf
        margin = math.log((conf / (1.0 - conf)) * (n - 1) + 1e-9)
        scores = [deterministic_rand(self.seed, query, i, "noise") * 0.05 for i in range(n)]
        scores[chosen] = margin
        return scores
