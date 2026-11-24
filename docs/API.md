# API

## Python API

```python
from arbiter.api import Arbiter

a = Arbiter()                     # 默认策略（mock decider + mock reasoner）
r = a.route("我要退款")            # 分层路由
print(r.final_option, r.tier, r.cost_saved, r.speedup)
a.decide("我要退款")               # 只看首层决策打分
```

## HTTP API

```bash
python -m arbiter serve           # 默认 127.0.0.1:8000

curl -s localhost:8000/health
curl -s -X POST localhost:8000/v1/route \
  -H 'Content-Type: application/json' \
  -d '{"query":"我要退款"}'
```

## OpenAI 兼容

```bash
curl -s -X POST localhost:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"arbiter","messages":[{"role":"user","content":"我要退款"}]}'
```

## CLI

```bash
python -m arbiter doctor
python -m arbiter decide "我要退款"
python -m arbiter route "我要退款"
python -m arbiter bench --steps 6
python -m arbiter eval
python -m arbiter serve --port 8000
```
