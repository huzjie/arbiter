# -*- coding: utf-8 -*-
class ArbiterError(Exception):
    """arbiter 顶层异常。"""


class ConfigError(ArbiterError):
    """配置错误。"""


class RoutingError(ArbiterError):
    """路由错误。"""


class ProviderError(ArbiterError):
    """模型 provider 调用错误。"""
