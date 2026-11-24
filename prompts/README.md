# 可复用提示词模板

这些模板可直接喂给任意真实模型，用于把 `arbiter` 接到生产环境。

| 文件 | 用途 |
|---|---|
| intent_classification.system.md | 意图分类（封闭选项打分） |
| scoring.system.md | 选项打分 + 置信度输出 |
| escalation_policy.system.md | 升级策略说明 |
| calibration.system.md | 置信度校准 |
| decision_briefing.system.md | 决策简报（给人看） |
