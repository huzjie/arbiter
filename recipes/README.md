# 策略配方

现成策略配置，`python -m arbiter --config recipes/<name>.yaml route "..."` 直接用。

| 文件 | 场景 |
|---|---|
| confidence_gate.yaml | 默认：置信度门控级联 |
| cost_first.yaml | 成本优先（低阈值，尽量就地解决） |
| accuracy_first.yaml | 准确率优先（高阈值，宁升级） |
| multi_tier.yaml | 多级级联（规则→小模型→大模型） |
