#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: instr_parametric.py
@time: 2020/8/19 21:48
@project: wasm-python-book
@desc: 参数指令
"""


def drop(vm, _):
    """drop指令（操作码0x1A）从栈顶弹出一个操作数并把它扔掉"""
    vm.pop_u64()


def _select(vm, _):
    """
    select指令（操作码0x1B）从栈顶弹出3个操作数，
    然后根据最先弹出的操作数从其他两个操作数中“选择”一个压栈
    """
    v3 = vm.pop_bool()
    v2 = vm.pop_u64()
    v1 = vm.pop_u64()

    if v3:
        vm.push_u64(v1)
    else:
        vm.push_u64(v2)
