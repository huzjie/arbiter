# -*- coding: utf-8 -*-
"""策略 JSON Schema 描述（文档用途 + 可选校验）。"""

POLICY_SCHEMA = {
    "type": "object",
    "required": ["tiers"],
    "properties": {
        "name": {"type": "string"},
        "tiers": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["name", "type"],
                "properties": {
                    "name": {"type": "string"},
                    "type": {"enum": ["mock", "rule", "naive_bayes", "tfidf", "llm"]},
                    "skill": {"type": "number", "minimum": 0, "maximum": 1},
                    "cost": {"type": "number", "minimum": 0},
                    "latency_ms": {"type": "number", "minimum": 0},
                    "threshold": {"type": "number", "minimum": 0, "maximum": 1},
                    "temperature": {"type": "number"},
                },
            },
        },
        "budget": {"type": "object"},
        "cache": {"type": "object"},
        "intents": {"type": "array", "items": {"type": "string"}},
    },
}
