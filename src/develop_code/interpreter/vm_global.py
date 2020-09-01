#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: vm_global.py
@time: 2020/8/23 10:59
@project: wasm-python-book
@desc:
"""
from binary.types import GlobalType
from instance import module
from interpreter.errors import ErrImmutableGlobal
from interpreter.val import wrap_u64, unwrap_u64


class GlobalVar(module.Global):
    def __init__(self, gt, val):
        self.type = gt
        self.val = val

    def get_as_u64(self):
        return self.val

    def set_as_u64(self, val):
        if self.type.mut != 1:
            return ErrImmutableGlobal
        self.val = val

    def get(self):
        return wrap_u64(self.type.val_type, self.val)

    def set(self, val):
        self.val = unwrap_u64(self.type.val_type, val)


def new_global(vt, mut, val):
    gt = GlobalType(val_type=vt)
    if mut:
        gt.mut = 1
    return GlobalVar(gt=gt, val=val)
