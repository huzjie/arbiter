# -*- coding: utf-8 -*-
"""合成数据集：确定性生成带真值的查询集，真值由闭式 oracle 提供。"""
from ..intents import INTENTS, INTENT_IDS, oracle_label
from ..utils.rng import seed_from, deterministic_shuffle

_TEMPLATES = [
    "{kw}",
    "我想{kw}",
    "请问{kw}怎么办",
    "{kw}怎么操作",
    "帮我{kw}",
    "关于{kw}的问题",
    "{kw}，谢谢",
    "请问一下{kw}",
]


def make_dataset(seed="arbiter", per_intent=4, noise=8):
    """返回 [(query, true_label), ...]。每个意图 per_intent 条 + noise 条噪声。"""
    queries = []
    for iid in INTENT_IDS:
        kws = INTENTS[iid]["keywords"]
        for i in range(per_intent):
            kw = kws[i % len(kws)]
            tmpl = _TEMPLATES[(seed_from(seed, iid, i) % len(_TEMPLATES))]
            queries.append(tmpl.format(kw=kw))
    # 噪声：无关键词的随意文本，oracle 哈希兜底
    noise_words = ["今天", "天气", "心情", "随便", "聊天", "你好", "再见",
                   "在吗", "嗯嗯", "好的", "明白了", "收到"]
    for i in range(noise):
        w = noise_words[(seed_from(seed, "noise", i) % len(noise_words))]
        queries.append(f"随便说说{w}")
    deterministic_shuffle(seed, queries)
    return [(q, oracle_label(q)) for q in queries]
