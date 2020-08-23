#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: instr_control.py
@time: 2020/8/20 17:31
@project: wasm-python-book
@desc:
"""
from ch07.binary.opcodes import Call
from ch07.interpreter import uint32


def call(vm, args):
    idx = uint32(args)
    imported_func_count = len(vm.module.import_sec)
    if idx < imported_func_count:
        # hack!
        call_assert_func(vm, args)
    else:
        call_internal_func(vm, idx - imported_func_count)


"""
operand stack:

+~~~~~~~~~~~~~~~+
|               |
+---------------+
|     stack     |
+---------------+
|     locals    |
+---------------+
|     params    |
+---------------+
|  ............ |
"""


def call_internal_func(vm, idx):
    ft_idx = vm.module.func_sec[idx]
    ft = vm.module.type_sec[ft_idx]
    code = vm.module.code_sec[idx]
    vm.enter_block(Call, ft, code.expr)

    local_count = int(code.get_local_count())
    for _ in range(local_count):
        vm.push_u64(0)


def call_assert_func(vm, args):
    idx = int(args)
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


# hack!
def br_if(vm, arg):
    if vm.pop_bool():
        vm.exit_block()
