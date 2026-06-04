# -*- coding: utf-8 -*-
"""
kaiwu-community: 基础版 SDK
"""

import pkgutil
import importlib

# 1. 这一行必须保留：支持跨目录合并社区版和企业版的代码路径
__path__ = pkgutil.extend_path(__path__, __name__)

__version__ = "1.0.4"

# 2. 正常、显式导入社区版的核心子模块（层级清晰，不带 * 污染）
from . import core, common

# 3. 声明企业版的子包白名单（不在这里 import，仅作名字记录）
_EXT_MODULES = {
    "cim",
    "classical",
    "hobo",
    "hybrid",
    "license",
    "preprocess",
    "sampler",
}


def __getattr__(name: str):
    """
    Python 3.7+ 特性：当用户尝试访问 kw.classical，且顶层没有这个属性时，会触发此函数。
    """
    if name in _EXT_MODULES:
        try:
            # 只有在用户调用的时候，才临时去系统里导入它
            return importlib.import_module(f"kaiwu.{name}")
        except ModuleNotFoundError as e:
            # 如果是 classical 这个子包自身找不到，说明用户只装了社区版，没有安装企业版
            if e.name == f"kaiwu.{name}":
                raise AttributeError(
                    f"Module 'kaiwu' has no attribute '{name}'. "
                    f"This feature requires 'kaiwu-enterprise' to be installed."
                ) from None
            # 如果是企业版装了，但它内部代码报错或者缺少 numpy 等依赖，原样抛出，方便 Debug
            raise e

    raise AttributeError(f"module 'kaiwu' has no attribute '{name}'")


# 4. 显式声明，让 IDE 和打包工具能够清晰感知
__all__ = ["core", "common"] + list(_EXT_MODULES)
