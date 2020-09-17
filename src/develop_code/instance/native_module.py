#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: native_module.py
@time: 2020/8/23 19:57
@project: wasm-python-book
@desc: 本地模型实例
"""
from instance import module
from instance.native_function import NativeFunction
from instance.sig_parser import parse_name_and_sig


class NativeModule(module.Module):
    def __init__(self):
        self.exported = dict()

    def register_func(self, name_and_sig, f):
        name, sig = parse_name_and_sig(name_and_sig)
        self.exported[name] = NativeFunction(t=sig, f=f)

    def register(self, name, x):
        self.exported[name] = x

    def get_member(self, name):
        return self.exported.get(name, None)

    def invoke_func(self, name, args):
        # TODO
        return self.exported[name].call(args)

    def get_global_val(self, name):
        # TODO
        return self.exported[name].get(), None

    def set_global_var(self, name, val):
        # TODO
        self.exported[name].set(val)
        return None
