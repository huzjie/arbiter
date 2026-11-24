# -*- coding: utf-8 -*-
import json


def dumps(obj, **kw):
    return json.dumps(obj, ensure_ascii=False, **kw)


def loads(s):
    return json.loads(s)
