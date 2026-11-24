# 配置

策略用一个 YAML / JSON 文件描述。核心是 `tiers` 数组（从便宜到贵）。

```yaml
policy:
  name: default
  tiers:
    - name: decider
      type: mock        # mock/rule/naive_bayes/tfidf/llm
      skill: 0.95       # mock 后端专用：决策准确率 0~1
      cost: 1           # 单次调用成本（归一化单位）
      latency_ms: 5
      threshold: 0.85   # 置信度门控
      temperature: 1.0
    - name: reasoner
      type: mock
      skill: 1.0
      cost: 100
      latency_ms: 200
  budget:
    enabled: false
    max_cost: 5000
    max_latency_ms: 10000
  cache:
    enabled: true
    backend: lru
    capacity: 1000
    ttl_seconds: 300
    semantic_threshold: 0.92
  intents: [refund, consult, complaint, order, shipping, invoice, account, cancel]
```

加载：`python -m arbiter --config config.yaml route "..."` 或
`Arbiter(load_config("config.yaml"))`。
