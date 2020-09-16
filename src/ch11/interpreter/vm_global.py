#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: vm_global.py
@time: 2020/8/23 10:59
@project: wasm-python-book
@desc:
"""
from ch11.instance import module
from ch11.interpreter.errors import ErrImmutableGlobal
from ch11.interpreter.val import wrap_u64, unwrap_u64


class GlobalVar(module.Global):
    def __init__(self, gt, val):
        self.type = gt
        self.val = val

    def get_as_u64(self):
        return self.val

    def set_as_u64(self, val):
        if self.type.mut != 1:
            raise ErrImmutableGlobal
        self.val = val

    def get(self):
        return wrap_u64(self.type.val_type, self.val)

    def set(self, val):
        self.val = unwrap_u64(self.type.val_type, val)
