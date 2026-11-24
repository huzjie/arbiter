# -*- coding: utf-8 -*-
"""指标导出。"""
import json


def export_json(snapshot: dict) -> str:
    return json.dumps(snapshot, ensure_ascii=False, indent=2)
