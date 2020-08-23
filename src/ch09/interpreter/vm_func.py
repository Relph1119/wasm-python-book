#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: vm_func.py
@time: 2020/8/23 16:47
@project: wasm-python-book
@desc: 函数方法
"""


class VMFunc:
    def __init__(self, ft=None, code=None, pf=None):
        self.type = ft
        self.code = code
        self.py_func = pf


def new_external_func(ft, pf):
    return VMFunc(ft=ft, pf=pf)


def new_internal_func(ft, code):
    return VMFunc(ft=ft, code=code)
