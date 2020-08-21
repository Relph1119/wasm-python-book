#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: instr_control.py
@time: 2020/8/20 17:31
@project: wasm-python-book
@desc:
"""


# hack!
from ch05.interpreter import uint32


def call(vm, args):
    idx = uint32(args)
    name = vm.module.import_sec[idx].name
    if name == 'assert_true':
        __assert_equal(vm.pop_bool(), True)
    elif name == 'assert_false':
        __assert_equal(vm.pop_bool(), False)
    elif name == 'assert_eq_i32':
        __assert_equal(vm.pop_u32(), vm.pop_u32())
    elif name == 'assert_eq_i64':
        __assert_equal(vm.pop_u64(), vm.pop_u64())
    elif name == 'assert_eq_f32':
        __assert_equal(vm.pop_f32(), vm.pop_f32())
    elif name == 'assert_eq_f64':
        __assert_equal(vm.pop_f64(), vm.pop_f64())
    else:
        raise Exception("TODO")


def __assert_equal(a, b):
    if a != b:
        raise Exception("{} != {}".format(a, b))
