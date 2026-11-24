# -*- coding: utf-8 -*-
"""零依赖 token 估算：中文按字数、英文按 ~4 字符/token。"""
import re

_CJK = re.compile(r"[\u4e00-\u9fff]")
_ASCII = re.compile(r"[a-zA-Z0-9]+")


def estimate_tokens(text: str) -> int:
    """粗略估算文本 token 数。中文 1 字 ≈ 1 token，英文 ~4 字符 ≈ 1 token。"""
    if not text:
        return 0
    cjk = len(_CJK.findall(text))
    ascii_chars = len(_ASCII.findall("".join(_ASCII.findall(text))))
    ascii_tokens = max(1, ascii_chars // 4) if ascii_chars else 0
    return cjk + ascii_tokens
