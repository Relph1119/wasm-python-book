#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: vm_func.py
@time: 2020/8/23 16:47
@project: wasm-python-book
@desc: 函数方法
"""

from ch10.instance.module import Function
from ch10.interpreter.instr_control import call_func
from ch10.interpreter.val import unwrap_u64, wrap_u64


class VMFunc(Function):

    def __init__(self, vm=None, ft=None, code=None, f: Function = None):
        self.type = ft
        self.code = code
        self.func = f
        # 为了实现Call()方法
        self.vm = vm

    def call(self, args):
        if self.func is not None:
            return self.func.call(args)
        return self.safe_call(args)

    def safe_call(self, args):
        results, error = [], None
        try:
            results = self._call(args)
        except Exception as e:
            error = e

        return results, error

    def _call(self, args):
        push_args(self.vm, self.type, args)
        call_func(self.vm, self)
        if self.func is None:
            self.vm.loop()
        return pop_results(self.vm, self.type)


def push_args(vm, ft, args):
    if len(ft.param_types) != len(args):
        raise Exception("param count: %d, arg count: %d" %
                        (len(ft.param_types), len(args)))
    for i, vt in enumerate(ft.param_types):
        vm.push_u64(unwrap_u64(vt, args[i]))


def pop_results(vm, ft):
    results = [None] * len(ft.result_types)
    for n in range(len(ft.result_types) - 1, -1, -1):
        results[n] = wrap_u64(ft.result_types[n], vm.pop_u64())

    return results


def new_external_func(ft, f):
    return VMFunc(ft=ft, f=f)


def new_internal_func(vm, ft, code):
    return VMFunc(vm=vm, ft=ft, code=code)
