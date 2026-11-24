# 贡献指南

1. Fork 仓库，新建分支。
2. 改动后跑 `python -m unittest discover -s tests`。
3. 提交前 `python -m arbiter doctor` 自检。
4. 发 PR，说明改动与动机。

代码风格：零第三方依赖（除可选 PyYAML），标准库优先。
