# -*- coding: utf-8 -*-
"""内置意图集（封闭选项集）：决策模型在这里打分选路。

每个意图：id + 中文标签 + 关键词。这是「决策模型在预设选项中打分选路」的
最小完整示例——真实场景把 keywords 换成你自己的分类体系即可。
"""

INTENTS = {
    "refund": {"label": "退款", "keywords": ["退款", "退货", "退钱", "返款", "退款流程", "退款进度", "七天无理由"]},
    "consult": {"label": "咨询", "keywords": ["怎么", "如何", "使用", "说明", "教程", "怎么用", "怎么操作", "帮助", "介绍"]},
    "complaint": {"label": "投诉", "keywords": ["投诉", "差评", "不满", "生气", "态度差", "举报", "维权", "糟心"]},
    "order": {"label": "下单", "keywords": ["下单", "购买", "买", "订购", "加入购物车", "付款", "结算", "拍下"]},
    "shipping": {"label": "物流", "keywords": ["物流", "发货", "快递", "到哪", "运输", "配送", "单号", "签收"]},
    "invoice": {"label": "发票", "keywords": ["发票", "开票", "报销", "抬头", "税号", "电子发票", "专票"]},
    "account": {"label": "账户", "keywords": ["账户", "登录", "密码", "注册", "账号", "验证码", "绑定", "改密"]},
    "cancel": {"label": "取消", "keywords": ["取消", "撤销", "取消订单", "退订", "关闭", "不想要"]},
}

INTENT_IDS = list(INTENTS.keys())
INTENT_LABELS = {k: v["label"] for k, v in INTENTS.items()}


def oracle_label(query: str) -> str:
    """闭式 oracle：按关键词命中数确定真实意图，未命中则哈希兜底。"""
    best, best_hit = None, 0
    for iid, meta in INTENTS.items():
        hit = sum(1 for kw in meta["keywords"] if kw in query)
        if hit > best_hit:
            best, best_hit = iid, hit
    if best is not None:
        return best
    from .utils.rng import seed_from
    return INTENT_IDS[seed_from("oracle", query) % len(INTENT_IDS)]


def oracle_index(query: str, options) -> int:
    """返回 query 在 options 中的真实选项下标。"""
    label = oracle_label(query)
    for i, opt in enumerate(options):
        s = str(opt)
        if s == label or s == INTENT_LABELS.get(label):
            return i
    from .utils.rng import seed_from
    return seed_from("oracle_idx", query) % len(options)
