# arbiter —— 分层决策路由网关

> **把「大模型负责推理、小决策模型负责高频判断」的分层架构，落成一个零依赖、填配置就能跑的成本优化层。**
> 对应热点：AWS Strands Decider v2 决策模型家族——在预设选项中打分选路，成本降 98%、速度提 78%。

[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![License MIT](https://img.shields.io/badge/license-MIT-green)](./LICENSE)

---

## 👀 它解决什么问题？

现在调用大模型的默认姿势是「什么事都交给最贵的模型」。但大量高频判断——
意图分类、打分、选路、是/否——根本不需要生成，本质是在一个**封闭选项集里挑一个**。

**arbiter 把这层判断从「生成」里抽出来，交给便宜的决策模型：**

| 层 | 类比 | 做什么 | 成本 |
|---|---|---|---|
| **decider**（决策模型） | 前台小模型 | 在封闭选项集上打分选路 | 便宜（1 单位） |
| **reasoner**（推理模型） | 后台大模型 | 兜底难判断 | 贵（100 单位） |

decider 打分后，**top1 置信度 ≥ 阈值就采纳**（便宜路径）；不够才升级到 reasoner（贵路径）。
于是：海量简单判断就地解决、少数难判断才上贵模型——**成本降下来、准确率被兜底保住**。

---

## ⚡ 30 秒上手

```bash
git clone https://github.com/huzjie/arbiter.git
cd arbiter
pip install -r requirements.txt   # 仅 PyYAML，可选
python -m arbiter doctor          # 自检
python -m arbiter route "我要退款"  # 分层路由
python -m arbiter bench           # 技能扫掠基准
python -m arbiter eval            # 评估
python -m arbiter serve           # 启动 HTTP 服务（含 OpenAI 兼容端点）
```

**填配置接真实模型**：把 `config.example.yaml` 复制为 `config.yaml`，把 decider 的 `type`
从 `mock` 改成 `llm`，reasoner 换成 `openai`/`anthropic` provider，填 key 即可。

---

## 🧠 技术拆解：三个核心机制（可直接照抄）

### 1. 决策模型 = 不生成文本，只在选项上打分

大模型默认是「生成器」——逐 token 吐答案。但「分类/打分/选路」这些高频判断，
本质是把「语言头」换成「指针头」：一次前向对每个候选打分，直接输出概率分布。

好处：输出空间小、可控（不会幻觉出选项之外的东西）、能接概率校准与门控、小模型也能做好。

```python
from arbiter.api import Arbiter

a = Arbiter()
r = a.route("我要退款")          # 在 8 个意图里选一个
print(r.final_option, r.tier, r.cost_saved)   # refund  decider  0.99
```

### 2. 级联路由 + 置信度门控

```
decider 打分 → top1 置信度 >= 阈值 ? 采纳（便宜路径）
                             : 升级到 reasoner（贵路径兜底）
```

阈值是**关键旋钮**：调低省得多但可能放过「自信但错误」的判断，调高更稳但省得少。
`python -m arbiter bench` 会把 skill 从 0 扫到 1，让你看到完整的单调曲线。

### 3. 成本模型（诚实暴露边界）

```
实际成本 = c0 + e × c1         # e = 升级率
成本节省 = 1 - (c0 + e·c1) / c1
```

默认 c0=1、c1=100：决策模型足够强（e→0）省 99%、提速 40x；但若 e→1（决策模型太弱，
几乎全升级），你反而**多付了一层 decider**。所以分层路由不是「白加一层」，
而是「把足够强的决策模型下沉」，这一层必须真的比贵模型便宜一个数量级才划算。

---

## 📊 基准（实测，确定性可复现）

```
| skill | 路由准确率 | 决策准确率 | 升级率 | 成本节省 | 提速 |
|-------|-----------|-----------|--------|---------|------|
| 0.00  | 1.000     | 0.075     | 1.000  | 0.000   | 0.98x|
| 0.50  | 1.000     | 0.400     | 1.000  | 0.000   | 0.98x|
| 0.83  | 0.875     | 0.675     | 0.575  | 0.415   | 1.67x|
| 1.00  | 1.000     | 1.000     | 0.000  | 0.990   | 40.00x|
```

解读：**决策准确率**随 skill 单调升（证明 mock 后端正确）、**升级率**单调降、
**成本节省**单调升；**路由准确率**始终≈1.0（低 skill 时靠 reasoner 兜底纠正）。
skill≈0.83 处的小回落，直观展示了「自信但错误越过阈值」的代价——这就是调阈值的意义。

---

## 🗂 项目结构

```
arbiter/
├── deciders/     决策模型（mock/rule/naive_bayes/tfidf/llm/threshold/ensemble）
├── router/       级联路由 + 预算路由
├── budget/       成本/延迟预算
├── cache/        LRU/TTL/语义缓存/路由缓存
├── adapters/     模型 provider（mock/openai/anthropic/local）
├── gateway/      零依赖 HTTP 网关 + OpenAI 兼容端点
├── eval/         合成数据集 + 指标 + 技能扫掠基准
├── policy/ config/ metrics/ utils/
├── api.py        门面（route/decide）
├── cli.py        doctor/decide/route/bench/eval/serve
tests/           55 个单元测试（unittest，零依赖）
docs/            18 篇文档 + 逐模块说明
examples/        12 个可运行示例
prompts/         6 套可复用提示词模板
recipes/         4 套策略配方
helm/ k8s/ .github/  Docker/K8s/Helm/CI
```

---

## 🧩 可直接复用的干货块

**A. 确定性 mock 决策模型的「正确性 / 置信度」分离建模**（`arbiter/deciders/mock.py`）：

```python
# 正确性硬币：以概率 skill 选对（决策准确率随 skill 单调）
chosen = true if deterministic_rand(seed, query, "coin") < skill else wrong
# 置信度目标：conf = 1/N + (1 - 1/N)*skill，随 skill 单调（越强越敢拍板）
conf = 1/n + (1 - 1/n)*skill
# 把置信度反解成 logit 边际，使 softmax 后 top1 ≈ conf
margin = log((conf/(1-conf)) * (n-1))
```

关键：**「准不准」和「敢不敢拍板」是两件事，要分开建模**——真实分类器就是这样，
置信度门控路由正是靠「不自信就升级」兜住低 skill 时的错误。

**B. 置信度门控的阈值调参口诀**：先保住目标准确率，再往低调阈值抠成本；
decider 与 reasoner 成本比越大（如 1:100），阈值可越激进；误判代价高（医疗/金融）就调高。

**C. 语义缓存命中即省**：TF-IDF 余弦相似度 ≥ 阈值直接复用上次结果，连 decider 都不跑。
中文分词记得先加停用词表，否则「一张发票」「一张流程图」会因「一张」撞车。

**D. 兜底 reasoner 一定要设成「恒信任」**（末层 `is_final=True`），否则级联可能不终止。

---

## 📄 许可

MIT License
