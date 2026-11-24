# -*- coding: utf-8 -*-
"""零依赖 HTTP 网关：基于 http.server 的 OpenAI 兼容 + 决策/路由端点。"""
import json
import time
from http.server import BaseHTTPRequestHandler

from .schemas import (parse_request, route_response, chat_completion_response)
from .middleware import Middleware
from .errors import http_error


class ArbiterHandler(BaseHTTPRequestHandler):
    arbiter = None
    middleware = None

    def _json(self, obj, status=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        t0 = time.time()
        if self.path in ("/health", "/healthz"):
            self._json({"status": "ok", "version": "1.0.0"})
            self._log(200, t0)
            return
        if self.path == "/metrics":
            self._json(self.arbiter.metrics.snapshot()
                       if hasattr(self.arbiter, "metrics") else {})
            self._log(200, t0)
            return
        http_error(self, 404, "not found")
        self._log(404, t0)

    def do_POST(self):
        t0 = time.time()
        if self.middleware and not self.middleware.authorize(self.headers):
            http_error(self, 401, "unauthorized")
            self._log(401, t0)
            return
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8")
            req = parse_request(body)
            if self.path == "/v1/decide":
                self._json(self._decide(req))
            elif self.path == "/v1/route":
                self._json(self._route(req))
            elif self.path == "/v1/chat/completions":
                self._json(self._chat(req))
            else:
                http_error(self, 404, "not found")
            self._log(200, t0)
        except Exception as e:  # noqa: BLE001
            http_error(self, 500, str(e))
            self._log(500, t0)

    def _decide(self, req):
        query = req.get("query", "")
        options = req.get("options")
        r = self.arbiter.decide(query, options)
        return r.as_dict()

    def _route(self, req):
        query = req.get("query", "")
        options = req.get("options")
        res = self.arbiter.route(query, options)
        if hasattr(self.arbiter, "metrics"):
            self.arbiter.metrics.record(res)
        return route_response(res)

    def _chat(self, req):
        messages = req.get("messages", [])
        query = ""
        for m in reversed(messages):
            if m.get("role") == "user":
                query = m.get("content", "")
                break
        res = self.arbiter.route(query)
        return chat_completion_response(query, res)

    def _log(self, status, t0):
        ms = int((time.time() - t0) * 1000)
        if self.middleware:
            self.middleware.log(self.command, self.path, status, ms)

    def log_message(self, fmt, *args):
        pass  # 用自带的中间件日志，关闭默认 stderr 输出
