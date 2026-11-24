# -*- coding: utf-8 -*-
"""OpenAI 兼容层：把路由结果包成 chat.completion 响应。"""
from .schemas import chat_completion_response


def chat_completion(query: str, res) -> dict:
    return chat_completion_response(query, res)
