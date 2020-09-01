#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: native.py
@time: 2020/8/23 17:33
@project: wasm-python-book
@desc: 本地方法
"""
from binary.types import ValTypeI32, ValTypeF32, ValTypeF64
from instance.native_module import NativeModule
from interpreter.vm_global import new_global
from interpreter.vm_memory import new_memory
from interpreter.vm_table import new_table

DEBUG = False


def new_spectest_instance():
    spec_test = NativeModule()
    spec_test.register_func("print()->()", _print)
    spec_test.register_func("print_i32(i32)->()", _print)
    spec_test.register_func("print_i64(i64)->()", _print)
    spec_test.register_func("print_f32(f32)->()", _print)
    spec_test.register_func("print_f64(f64)->()", _print)
    spec_test.register_func("print_i32_f32(i32,f32)->()", _print)
    spec_test.register_func("print_f64_f64(f64,f64)->()", _print)
    spec_test.register("global_i32", new_global(ValTypeI32, False, 666))
    spec_test.register("global_f32", new_global(ValTypeF32, False, 0))
    spec_test.register("global_f64", new_global(ValTypeF64, False, 0))
    spec_test.register("table", new_table(10, 20))
    spec_test.register("memory", new_memory(1, 2))
    return spec_test


def _print(args):
    if DEBUG:
        for arg in args:
            print("spectest> {}".format(arg))
    return None, None
