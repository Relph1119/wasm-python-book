#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: errors.py
@time: 2020/8/18 16:42
@project: wasm-python-book
@desc: 自定义异常
"""


class ErrUnexpectedEnd(Exception):
    """方法或段结束异常"""

    def __init__(self):
        super().__init__("unexpected end of section or function")


class ErrIntTooLong(Exception):
    """Int类型超长"""

    def __init__(self):
        super().__init__("integer representation too long")


class ErrIntTooLarge(Exception):
    """Int类型值太大"""

    def __init__(self):
        super().__init__("integer too large")
