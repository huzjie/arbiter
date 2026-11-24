# -*- coding: utf-8 -*-
"""线程安全计数器。"""
import threading


class Counter:
    def __init__(self):
        self._n = 0
        self._lock = threading.Lock()

    def inc(self, d=1):
        with self._lock:
            self._n += d
            return self._n

    @property
    def value(self):
        with self._lock:
            return self._n
