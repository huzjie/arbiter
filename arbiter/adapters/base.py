# -*- coding: utf-8 -*-
"""模型 provider 抽象。"""
from abc import ABC, abstractmethod


class Provider(ABC):
    name = "base"

    @abstractmethod
    def complete(self, prompt: str, **kw) -> str:
        """给定提示词，返回模型文本。"""
        raise NotImplementedError
