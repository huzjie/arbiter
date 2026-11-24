# -*- coding: utf-8 -*-
"""Anthropic provider（Messages API）。"""
import json
import os
import urllib.request

from ..utils.errors import ProviderError
from .base import Provider


class AnthropicProvider(Provider):
    name = "anthropic"

    def __init__(self, api_key=None, model="claude-sonnet-4-5", timeout=30):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY", "")
        self.model = model
        self.timeout = timeout

    def complete(self, prompt: str, **kw) -> str:
        url = "https://api.anthropic.com/v1/messages"
        payload = {
            "model": kw.get("model", self.model),
            "max_tokens": kw.get("max_tokens", 512),
            "messages": [{"role": "user", "content": prompt}],
        }
        req = urllib.request.Request(
            url, data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json",
                     "x-api-key": self.api_key,
                     "anthropic-version": "2023-06-01"},
            method="POST")
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            return "".join(b.get("text", "") for b in data.get("content", []))
        except Exception as e:  # noqa: BLE001
            raise ProviderError(f"Anthropic 调用失败: {e}") from e
