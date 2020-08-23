#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: native_function.py
@time: 2020/8/23 19:54
@project: wasm-python-book
@desc:
"""
from binary.types import FuncType
from instance.module import Function


class NativeFunction(Function):
    def __init__(self, t: FuncType = None, f=None):
        self.type = t
        self.f = f

    def call(self, args):
        return self.f(args)
