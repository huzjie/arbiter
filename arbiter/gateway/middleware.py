# -*- coding: utf-8 -*-
"""中间件：简单 API Key 校验 + 访问日志。"""
import time


class Middleware:
    def __init__(self, api_key: str = None, logger=None):
        self.api_key = api_key
        self.logger = logger

    def authorize(self, headers) -> bool:
        if not self.api_key:
            return True
        auth = headers.get("Authorization", "")
        return auth == f"Bearer {self.api_key}"

    def log(self, method, path, status, ms):
        if self.logger:
            self.logger(f"{time.strftime('%H:%M:%S')} {method} {path} "
                        f"-> {status} ({ms}ms)")
