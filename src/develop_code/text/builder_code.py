#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: builder_code.py
@time: 2020/8/31 19:22
@project: wasm-python-book
@desc:
"""
from binary.module import Locals


class CodeBuilder:
    def __init__(self):
        self.locals = []
        self.local_names = None
        self.label_names = None
        self.block_depth = 0

    def get_local_idx(self, var):
        self.local_names.kind = "local"
        return self.local_names.get_idx(var)

    def add_param(self, name):
        return self.local_names.define_name(name)

    def add_local(self, name, val_type):
        self.local_names.kind = "local"
        err = self.local_names.define_name(name)
        if err is not None:
            return err

        n = len(self.locals)
        if n == 0 or isinstance(self.locals[n - 1], val_type):
            self.locals.append(Locals(1, val_type))
        else:
            self.locals[n - 1].n += 1

        return None

    def enter_block(self):
        self.block_depth += 1

    def exit_block(self):
        self.block_depth -= 1

    def define_label(self, name):
        self.label_names.define_name


def new_code_builder():
    code_builder = CodeBuilder()
    code_builder.local_names = new_symbol_table("parameter")
    code_builder.label_names = new_symbol_table("label")
