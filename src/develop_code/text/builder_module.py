#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: builder_module.py
@time: 2020/8/31 19:13
@project: wasm-python-book
@desc:
"""
from binary.module import Module


class ModuleBuilder:
    def __init__(self):
        self.pass_ = 0
        self.module = None
        self.fty_by_sig = dict()
        self.fty_names = None
        self.fun_names = None
        self.tab_names = None
        self.mem_names = None
        self.glb_names = None

    def get_func_type_idx(self, _var):
        return self.fty_names.get_idx(_var)

    def get_func_idx(self, _var):
        return self.fun_names.get_idx(_var)

    def get_table_idx(self, _var):
        return self.tab_names.get_idx(_var)

    def get_mem_idx(self, _var):
        return self.mem_names.get_idx(_var)

    def get_global_idx(self, _var):
        return self.glb_names.get_idx(_var)


def new_module_builder():
    module_builder = ModuleBuilder()
    module_builder.module = Module()
    module_builder.fty_by_sig = dict()
    module_builder.fty_names = new_symbol_table("function type")
    module_builder.fun_names = new_symbol_table("function")
    module_builder.tab_names = new_symbol_table("table")
    module_builder.mem_names = new_symbol_table("memory")
    module_builder.glb_names = new_symbol_table("global")
    return module_builder
