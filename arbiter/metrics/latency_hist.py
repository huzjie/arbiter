# -*- coding: utf-8 -*-
"""延迟直方图（对数桶）。"""
import math


class LatencyHistogram:
    def __init__(self):
        self.buckets = {}
        self.count = 0
        self.total = 0.0

    def observe(self, ms: float):
        if ms <= 0:
            bucket = "0"
        else:
            bucket = str(int(math.log10(ms)))
        self.buckets[bucket] = self.buckets.get(bucket, 0) + 1
        self.count += 1
        self.total += ms

    @property
    def avg(self):
        return self.total / self.count if self.count else 0.0
