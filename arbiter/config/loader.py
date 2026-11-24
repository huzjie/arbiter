# -*- coding: utf-8 -*-
"""配置 / 策略加载。零依赖：无 PyYAML 时用极简解析。"""
import json
from pathlib import Path

from .defaults import DEFAULT_POLICY
from ..utils.errors import ConfigError

try:
    import yaml as _yaml
except ImportError:
    _yaml = None


def _parse_yaml(text: str) -> dict:
    if _yaml is not None:
        return _yaml.safe_load(text) or {}
    # 极简 YAML 兜底（支持本项目的嵌套结构）
    import re
    root = {}
    stack = [(root, -1)]
    for line in text.splitlines():
        stripped = line.rstrip()
        if not stripped.strip() or stripped.lstrip().startswith("#"):
            continue
        indent = len(stripped) - len(stripped.lstrip(" "))
        content = stripped.strip()
        # 退栈
        while len(stack) > 1 and indent <= stack[-1][1]:
            stack.pop()
        cur = stack[-1][0]
        if content.startswith("- "):
            item = content[2:].strip()
            if ":" in item:
                k, v = item.split(":", 1)
                cur.setdefault("_list", []).append({k.strip(): _scalar(v.strip())})
            else:
                cur.setdefault("_list", []).append(_scalar(item))
            continue
        if content.endswith(":") and not content.startswith("-"):
            key = content[:-1].strip()
            child = {}
            cur[key] = child
            stack.append((child, indent))
            continue
        if ":" in content:
            k, v = content.split(":", 1)
            cur[k.strip()] = _scalar(v.strip())
    return root


def _scalar(v: str):
    v = v.strip().strip('"').strip("'")
    if v.lower() in ("true", "false"):
        return v.lower() == "true"
    if v in ("null", "none", "~"):
        return None
    try:
        return int(v)
    except ValueError:
        pass
    try:
        return float(v)
    except ValueError:
        return v


def load_config(path: str) -> dict:
    p = Path(path)
    if not p.exists():
        raise ConfigError(f"配置文件不存在: {path}")
    text = p.read_text(encoding="utf-8")
    if p.suffix.lower() == ".json":
        return json.loads(text)
    return _parse_yaml(text)


def load_policy(path: str) -> dict:
    cfg = load_config(path)
    return cfg.get("policy", cfg)


def merge_defaults(user: dict) -> dict:
    """把用户策略合并到默认策略上。"""
    import copy
    base = copy.deepcopy(DEFAULT_POLICY)
    if not user:
        return base
    for k, v in user.items():
        if k in base and isinstance(base[k], dict) and isinstance(v, dict):
            base[k].update(v)
        else:
            base[k] = v
    return base
