# 快速开始

## 30 秒跑通

```bash
git clone https://github.com/huzjie/arbiter.git
cd arbiter
pip install -r requirements.txt    # 仅 PyYAML（可选）
python -m arbiter doctor           # 自检
python -m arbiter route "我要退款"   # 分层路由
python -m arbiter bench            # 技能扫掠基准
python -m arbiter eval             # 评估
python -m arbiter serve            # 启动 HTTP 服务
```

## 填配置接真实模型

把 `config.example.yaml` 复制为 `config.yaml`，把 decider 的 `type` 从
`mock` 改成 `rule` / `naive_bayes` / `tfidf` / `llm`，reasoner 换成真实
provider（`openai` / `anthropic`），填上你的 key 与模型名即可。

```yaml
policy:
  tiers:
    - name: decider
      type: llm                # 用小模型在选项上打分
      cost: 1
      latency_ms: 40
      threshold: 0.85
    - name: reasoner
      type: llm                # 大模型兜底
      cost: 100
      latency_ms: 300
```

## 一句话原理

便宜的小决策模型在封闭选项集上打分，置信度够就采纳（便宜路径）；
不够就升级到贵的大模型兜底。于是成本降下来、准确率仍被兜底保住。
