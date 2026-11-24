# -*- coding: utf-8 -*-
"""TF-IDF + 线性分类器：把文本转稀疏向量，每个选项一套权重打分。"""
import math
from collections import Counter, defaultdict
from typing import List

from ..utils.text import tokenize
from ..utils.hashing import feature_hash
from .base import Decider


class TfidfLinearDecider(Decider):
    name = "tfidf"

    def __init__(self, dim: int = 65536):
        self.dim = dim
        self.df = defaultdict(int)
        self.n_docs = 0
        self.weights = defaultdict(lambda: defaultdict(float))  # label -> {idx: w}

    def fit(self, samples):
        docs = []
        for text, label in samples:
            toks = tokenize(text)
            docs.append((toks, label))
            for tok in set(toks):
                self.df[tok] += 1
        self.n_docs = len(docs)
        # 每类收集加权词频，累加成线性权重
        for toks, label in docs:
            tf = Counter(toks)
            for tok, cnt in tf.items():
                idf = math.log((1 + self.n_docs) / (1 + self.df[tok])) + 1.0
                self.weights[label][feature_hash(tok, self.dim)] += cnt * idf
        return self

    def _score(self, query: str, options: List[str]) -> List[float]:
        tf = Counter(tokenize(query))
        vec = defaultdict(float)
        for tok, cnt in tf.items():
            idf = math.log((1 + self.n_docs) / (1 + self.df.get(tok, 0))) + 1.0
            vec[feature_hash(tok, self.dim)] += cnt * idf
        scores = []
        for opt in options:
            w = self.weights.get(opt, {})
            s = sum(vec.get(i, 0.0) * wv for i, wv in w.items())
            scores.append(s)
        return scores
