# -*- coding: utf-8 -*-
"""HTTP 客户端示例（先 python -m arbiter serve 启动服务）。"""
import json
import urllib.request


def post(url, data):
    req = urllib.request.Request(
        url, data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))


if __name__ == "__main__":
    print("health:", json.dumps(post("http://127.0.0.1:8000/health", {}), ensure_ascii=False))
    print("route:", json.dumps(post("http://127.0.0.1:8000/v1/route",
                                    {"query": "我要退款"}), ensure_ascii=False))
