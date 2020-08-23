#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: instr_variable.py
@time: 2020/8/23 11:35
@project: wasm-python-book
@desc: 局部变量指令
"""
from ch08.interpreter import uint32


def local_get(vm, args):
    """获取局部变量"""
    idx = uint32(args)
    val = vm.get_operand(vm.local_0_idx + idx)
    vm.push_u64(val)


def local_set(vm, args):
    """设置局部变量的值"""
    idx = uint32(args)
    val = vm.pop_u64()
    vm.set_operand(vm.local_0_idx + idx, val)


def local_tee(vm, args):
    """用重定向操作符>把某个命令的输出重定向到文件里"""
    idx = uint32(args)
    val = vm.pop_u64()
    vm.push_u64(val)
    vm.set_operand(vm.local_0_idx + idx, val)


def global_get(vm, args):
    idx = uint32(args)
    val = vm.globals[idx].get_as_u64()
    vm.push_u64(val)


def global_set(vm, args):
    idx = uint32(args)
    val = vm.pop_u64()
    vm.globals[idx].set_as_u64(val)
