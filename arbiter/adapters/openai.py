# -*- coding: utf-8 -*-
"""OpenAI 兼容 provider：用 urllib 调任意 OpenAI 兼容端点（可指向本地 vLLM 等）。"""
import json
import os
import urllib.request

from ..utils.errors import ProviderError
from .base import Provider


class OpenAIProvider(Provider):
    name = "openai"

    def __init__(self, base_url=None, api_key=None, model="gpt-4o-mini", timeout=30):
        self.base_url = (base_url or os.environ.get("OPENAI_BASE_URL")
                         or "https://api.openai.com/v1").rstrip("/")
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        self.model = model
        self.timeout = timeout

    def complete(self, prompt: str, **kw) -> str:
        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": kw.get("model", self.model),
            "messages": [{"role": "user", "content": prompt}],
            "temperature": kw.get("temperature", 0.0),
        }
        req = urllib.request.Request(
            url, data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json",
                     "Authorization": f"Bearer {self.api_key}"},
            method="POST")
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]
        except Exception as e:  # noqa: BLE001
            raise ProviderError(f"OpenAI 调用失败: {e}") from e
