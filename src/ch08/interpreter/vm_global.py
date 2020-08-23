#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: vm_global.py
@time: 2020/8/23 10:59
@project: wasm-python-book
@desc:
"""
from ch08.interpreter.errors import ErrImmutableGlobal


class GlobalVar:
    def __init__(self, gt, val):
        self.type = gt
        self.val = val

    def get_as_u64(self):
        return self.val

    def set_as_u64(self, val):
        if self.type.mut != 1:
            return ErrImmutableGlobal
        self.val = val
