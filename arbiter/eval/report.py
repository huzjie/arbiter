# -*- coding: utf-8 -*-
"""报告渲染：把评估结果转成 Markdown / JSON。"""
import json


def render_report(rows, fmt="markdown"):
    if fmt == "json":
        return json.dumps(rows, ensure_ascii=False, indent=2)
    header = ("| skill | 路由准确率 | 决策准确率 | 升级率 | 成本节省 | 提速 |\n"
              "|---|---|---|---|---|---|")
    lines = [header]
    for r in rows:
        lines.append(
            f"| {r['skill']} | {r['routing_accuracy']:.3f} | "
            f"{r['decision_accuracy']:.3f} | {r['escalation_rate']:.3f} | "
            f"{r['avg_cost_saved']:.3f} | {r['avg_speedup']:.2f}x |")
    return "\n".join(lines)
