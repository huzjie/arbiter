# -*- coding: utf-8 -*-
"""请求/响应结构（轻量 dict 约定，零依赖）。"""


def parse_request(body: str):
    import json
    if not body:
        return {}
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        return {}


def route_response(res) -> dict:
    return res.as_dict()


def chat_completion_response(query: str, res) -> dict:
    content = (f"意图: {res.final_option} (置信度 {res.confidence:.3f}, "
               f"由 {res.tier} 判定, 成本节省 {res.cost_saved:.1%})")
    return {
        "id": f"arbiter-{res.tier}",
        "object": "chat.completion",
        "model": res.tier,
        "choices": [{
            "index": 0,
            "message": {"role": "assistant", "content": content},
            "finish_reason": "stop",
        }],
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
        "arbiter": res.as_dict(),
    }
