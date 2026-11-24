# -*- coding: utf-8 -*-
"""CLI：doctor / decide / route / bench / eval / serve。"""
import argparse
import json
import sys

from .api import Arbiter
from .config.loader import load_config, merge_defaults


def _load_policy(path):
    if path:
        return load_config(path)
    return None


def cmd_doctor(args):
    arb = Arbiter(_load_policy(args.config))
    ok = True
    print("== arbiter doctor ==")
    print(f"tiers: {[t.name for t in arb.tiers]}")
    print(f"intents: {arb.intents}")
    for q in ["我要退款", "这个怎么用", "帮我开个发票"]:
        r = arb.route(q)
        print(f"  route({q!r}) -> {r.final_option!r} "
              f"[tier={r.tier}, conf={r.confidence:.3f}, "
              f"cost_saved={r.cost_saved:.1%}]")
        ok = ok and bool(r.final_option)
    print("✅ doctor 通过" if ok else "❌ doctor 失败")
    return 0 if ok else 1


def cmd_decide(args):
    arb = Arbiter(_load_policy(args.config))
    r = arb.decide(args.query)
    print(json.dumps(r.as_dict(), ensure_ascii=False, indent=2))
    return 0


def cmd_route(args):
    arb = Arbiter(_load_policy(args.config))
    r = arb.route(args.query)
    print(json.dumps(r.as_dict(), ensure_ascii=False, indent=2))
    return 0


def cmd_bench(args):
    from .eval.bench import bench_skill_sweep
    from .eval.report import render_report
    rows = bench_skill_sweep(steps=args.steps, threshold=args.threshold)
    print(render_report(rows, args.format))
    return 0


def cmd_eval(args):
    from .eval.dataset import make_dataset
    from .eval.metrics import evaluate
    arb = Arbiter(_load_policy(args.config))
    queries = make_dataset()
    m = evaluate(arb.router, queries)
    print(json.dumps(m, ensure_ascii=False, indent=2))
    return 0


def cmd_serve(args):
    from .gateway.server import run
    arb = Arbiter(_load_policy(args.config))
    arb.metrics = __import__("arbiter.metrics.collector",
                             fromlist=["MetricsCollector"]).MetricsCollector()
    run(arb, host=args.host, port=args.port, api_key=args.api_key)
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(prog="arbiter",
                                 description="分层决策路由网关")
    ap.add_argument("--config", default=None, help="策略配置文件 (YAML/JSON)")
    sub = ap.add_subparsers(dest="cmd")

    sub.add_parser("doctor", help="自检")

    p = sub.add_parser("decide", help="决策打分")
    p.add_argument("query")

    p = sub.add_parser("route", help="分层路由")
    p.add_argument("query")

    p = sub.add_parser("bench", help="技能扫掠基准")
    p.add_argument("--steps", type=int, default=6)
    p.add_argument("--threshold", type=float, default=0.85)
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")

    sub.add_parser("eval", help="评估")

    p = sub.add_parser("serve", help="启动 HTTP 服务")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8000)
    p.add_argument("--api-key", default=None)

    args = ap.parse_args(argv)
    if args.cmd is None:
        ap.print_help()
        return 0
    return {
        "doctor": cmd_doctor, "decide": cmd_decide, "route": cmd_route,
        "bench": cmd_bench, "eval": cmd_eval, "serve": cmd_serve,
    }[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
