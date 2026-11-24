# FAQ

**Q：这跟普通「路由到大模型」有什么区别？**
A：普通路由是「选哪个模型」，这里是「便宜模型先打分、不够再升级」的**级联**，
还带置信度门控、预算、缓存，是一套完整的成本优化层。

**Q：mock 后端是什么？**
A：一个确定性的假决策模型，`skill` 参数控制准确率。用来离线验证链路，
不接真实模型也能跑通 doctor / bench / eval。

**Q：能接我的私有模型吗？**
A：能。`adapters.openai.OpenAIProvider` 支持任意 OpenAI 兼容端点（vLLM 等），
填 `base_url` + `model` 即可。

**Q：选项集怎么换成我自己的分类？**
A：改 `intents` 列表 + 对应关键词，或用 `NaiveBayesDecider` / `TfidfLinearDecider`
在你自己标注的数据上 `.fit()`。
