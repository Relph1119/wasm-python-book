#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: builder_symbols.py
@time: 2020/8/31 19:22
@project: wasm-python-book
@desc:
"""
from text.errors import new_semantic_error, new_verification_error
from text.num_parser import parse_u32


class SymbolTable:
    def __init__(self):
        self.kind = ""
        self.idx_by_name = dict()
        self.imported = 0
        self.defined = 0

    def get_idx(self, _var):
        idx = -1
        if _var[0] == '$':
            if _var in self.idx_by_name.keys():
                idx = self.idx_by_name.get(_var)
            else:
                return -1, new_semantic_error('undefined %s variable "%s"',
                                              (self.kind, _var))
        else:
            idx = parse_u32(_var)
        if self.kind != "label":
            max_value = self.imported + self.defined
            if idx >= max_value:
                return idx, new_verification_error("%s variable out of range: %d (max %d)",
                                                   (self.kind, idx, max_value - 1))

        return idx, None

    def import_name(self, name):
        idx = self.imported
        err = self.add_name(name, idx)
        if err is not None:
            return err
        self.imported += 1
        return None

    def define_name(self, name):
        idx = self.imported + self.defined
        err = self.add_name(name, idx)
        if err is not None:
            return err
        self.defined += 1
        return None

    def add_name(self, name, idx):
        if name != "":
            if name in self.idx_by_name.keys():
                return new_semantic_error('redefinition of %s "%s"',
                                          (self.kind, name))
            else:
                self.idx_by_name[name] = idx
        return None

    def define_label(self, name, idx):
        self.idx_by_name[name] = idx


def new_symbol_table(kind):
    symbol_table = SymbolTable()
    symbol_table.kind = kind
    return symbol_table
