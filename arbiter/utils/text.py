# -*- coding: utf-8 -*-
"""零依赖分词：ASCII 词 + 中文单字/二元组，附停用词表。"""
import re

STOPWORDS = {
    "的", "了", "是", "我", "你", "他", "她", "它", "们", "在", "有", "和",
    "就", "不", "人", "都", "一", "个", "上", "也", "很", "到", "说", "要",
    "去", "会", "着", "看", "好", "自己", "这", "那", "什么", "怎么", "为",
    "与", "或", "及", "等", "还", "而", "被", "把", "让", "请", "这个",
    "那个", "一个", "我们", "你们", "他们", "可以", "没有", "不是", "就是",
    "还是", "但是", "因为", "所以", "如果", "已经", "现在", "然后", "一下",
    "一些", "这些", "那些", "时候", "这样", "那样", "知道", "觉得", "请问",
    "麻烦", "谢谢", "你好", "帮我", "我要", "我想", "请问一下",
}

_CJK = re.compile(r"[\u4e00-\u9fff]")
_ASCII = re.compile(r"[a-zA-Z0-9]+")


def tokenize(text: str):
    """返回 token 列表：英文单词 + 中文单字 + 中文二元组（去停用词）。"""
    if not text:
        return []
    text = text.lower()
    toks = _ASCII.findall(text)
    cjk = _CJK.findall(text)
    # 中文单字（去停用词）
    toks += [c for c in cjk if c not in STOPWORDS]
    # 中文二元组
    toks += [cjk[i] + cjk[i + 1] for i in range(len(cjk) - 1)]
    return [t for t in toks if t not in STOPWORDS]
