# 安全

- 默认**零网络调用**（mock/local 后端），不泄露任何数据。
- 接真实模型时，密钥走环境变量（`OPENAI_API_KEY` / `ANTHROPIC_API_KEY`），
  **不要**写进配置文件或提交到仓库。
- HTTP 服务可加 `--api-key`，请求需带 `Authorization: Bearer <key>`。
- 决策模型只做分类打分、不执行任意代码，天然比生成式 Agent 更可控。
