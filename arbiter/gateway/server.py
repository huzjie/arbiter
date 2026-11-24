# -*- coding: utf-8 -*-
"""HTTP 服务启动。"""
from http.server import ThreadingHTTPServer

from .app import ArbiterHandler
from .middleware import Middleware


def run(arbiter, host="127.0.0.1", port=8000, api_key=None):
    ArbiterHandler.arbiter = arbiter
    ArbiterHandler.middleware = Middleware(api_key=api_key)
    server = ThreadingHTTPServer((host, port), ArbiterHandler)
    print(f"arbiter 网关已启动: http://{host}:{port}")
    print("  GET  /health")
    print('  POST /v1/decide  {"query": "...", "options": [...]}')
    print('  POST /v1/route   {"query": "...", "options": [...]}')
    print("  POST /v1/chat/completions  (OpenAI 兼容)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
