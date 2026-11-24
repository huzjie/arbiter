# -*- coding: utf-8 -*-
"""多项式朴素贝叶斯决策模型：可训练、零依赖、可解释。"""
import math
from collections import defaultdict
from typing import List

from ..utils.text import tokenize
from .base import Decider


class NaiveBayesDecider(Decider):
    name = "naive_bayes"

    def __init__(self, alpha: float = 1.0):
        self.alpha = alpha
        self.class_counts = defaultdict(int)
        self.term_counts = defaultdict(lambda: defaultdict(int))
        self.vocab = set()
        self.total = 0

    def fit(self, samples):
        """samples: [(text, label), ...]"""
        for text, label in samples:
            self.class_counts[label] += 1
            self.total += 1
            for tok in tokenize(text):
                self.term_counts[label][tok] += 1
                self.vocab.add(tok)
        return self

    def _logp(self, label: str, toks) -> float:
        n_class = self.class_counts.get(label, 0)
        if n_class == 0:
            return float("-inf")
        denom = sum(self.term_counts[label].values()) + self.alpha * len(self.vocab)
        logp = math.log(n_class / self.total) if self.total else 0.0
        for tok in toks:
            num = self.term_counts[label].get(tok, 0) + self.alpha
            logp += math.log(num / denom)
        return logp

    def _score(self, query: str, options: List[str]) -> List[float]:
        toks = tokenize(query)
        return [self._logp(opt, toks) for opt in options]
