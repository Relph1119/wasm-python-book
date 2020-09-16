#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: vm_table.py
@time: 2020/8/23 17:16
@project: wasm-python-book
@desc:
"""
from binary.types import TableType, FuncRef, Limits
from instance import module
from interpreter.errors import ErrUndefinedElem, ErrUninitializedElem


class Table(module.Table):
    def __init__(self, table_type=None):
        self.type = table_type
        self.elems = [None] * table_type.limits.min

    @property
    def size(self):
        return len(self.elems)

    def grow(self, n):
        self.elems.extend([None] * n)

    def get_elem(self, idx):
        self.check_idx(idx)
        elem = self.elems[idx]
        if elem is None:
            raise ErrUninitializedElem
        return elem

    def set_elem(self, idx, elem):
        self.check_idx(idx)
        self.elems[idx] = elem

    def check_idx(self, idx):
        if idx >= len(self.elems):
            raise ErrUndefinedElem


def new_table(min_value, max_value):
    tt = TableType(elem_type=FuncRef,
                   limits=Limits(min=min_value, max=max_value))
    return Table(tt)
