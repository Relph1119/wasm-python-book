#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: vm_table.py
@time: 2020/8/23 17:16
@project: wasm-python-book
@desc:
"""
from interpreter.errors import ErrUndefinedElem


class Table:
    def __init__(self, tt=None):
        self.type = tt
        self.elems = [None] * tt.limits.min

    @property
    def size(self):
        return len(self.elems)

    def grow(self, n):
        self.elems.extend([None] * n)

    def get_elem(self, idx):
        self.check_idx(idx)
        elem = self.elems[idx]
        return elem

    def set_elem(self, idx, elem):
        self.check_idx(idx)
        self.elems[idx] = elem

    def check_idx(self, idx):
        if idx >= len(self.elems):
            raise ErrUndefinedElem
