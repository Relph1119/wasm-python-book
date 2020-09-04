#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: builder_module.py
@time: 2020/8/31 19:13
@project: wasm-python-book
@desc:
"""
from binary.module import Module, Code, Elem, Global, Export, ExportDesc, Data
from binary.types import TableType, FuncRef, Limits
from interpreter import uint32
from text.builder_instr import new_i32_const0
from text.builder_symbols import new_symbol_table
from text.errors import new_verification_error, new_semantic_error
from text.str_escaper import escape


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

    def ensure_no_start(self):
        if self.module.start_sec is not None:
            return new_verification_error("multiple start sections")
        return None

    def ensure_no_non_imports(self):
        if self.fun_names.defined > 0 \
                or self.tab_names.defined > 0 \
                or self.mem_names.defined > 0 \
                or self.glb_names.defined > 0:
            return new_semantic_error("imports must occur before all non-import definitions")

        return None

    def check_count(self, kind):
        if kind == "table" and self.tab_names.imported > 0:
            return new_verification_error("only one table allowed")
        if kind == "memory" and self.mem_names.imported > 0:
            return new_verification_error("only one memory block allowed")
        return None

    def import_name(self, kind, name):
        err = self.ensure_no_non_imports()
        if err is not None:
            return err
        if kind == "func":
            return self.fun_names.import_name(name)
        elif kind == "table":
            return self.tab_names.import_name(name)
        elif kind == "memory":
            return self.mem_names.import_name(name)
        elif kind == "global":
            return self.glb_names.import_name(name)
        else:
            raise Exception("unreachable")

    def define_name(self, kind, name):
        if kind == "func":
            return self.fun_names.define_name(name)
        elif kind == "table":
            return self.tab_names.define_name(name)
        elif kind == "memory":
            return self.mem_names.define_name(name)
        elif kind == "global":
            return self.glb_names.define_name(name)
        else:
            raise Exception("unreachable")

    def add_type_def(self, name, func_type):
        err = self.fty_names.define_name(name)
        if err is not None:
            return err

        self.module.type_sec.append(func_type)
        sig = func_type.get_signature()

        if sig not in self.fty_by_sig.keys():
            self.fty_by_sig[sig] = len(self.module.type_sec) - 1
        return None

    def add_type_use(self, func_type):
        sig = func_type.get_signature()
        if sig in self.fty_by_sig.keys():
            return self.fty_by_sig.get(sig)

        self.module.type_sec.append(func_type)
        idx = len(self.module.type_sec) - 1
        self.fty_by_sig[sig] = idx
        self.fty_names.define_name("")
        return idx

    def add_import(self, imp):
        self.module.import_sec.append(imp)
        return self.calc_imported_count(imp.desc.tag) - 1

    def calc_imported_count(self, tag):
        n = 0
        for imp in self.module.import_sec:
            if imp.desc.tag == tag:
                n += 1

        return n

    def add_func(self, ft_idx, locals_vec, expr):
        self.module.func_sec.append(uint32(ft_idx))
        self.module.code_sec.append(Code(locals_vec=locals_vec, expr=expr))
        return self.fun_names.imported + len(self.module.func_sec) - 1

    def add_table(self, table_type):
        self.module.table_sec.append(table_type)
        if self.tab_names.imported + len(self.module.table_sec) > 1:
            return new_verification_error("only one table allowed")

        return None

    def add_table_with_elems(self, func_indices):
        err = self.add_table(TableType(elem_type=FuncRef,
                                       limits=Limits(min=len(func_indices))))
        self.module.elem_sec.append(Elem(table_idx=0,
                                         offset_expr=[new_i32_const0()],
                                         vec_init=func_indices))
        return err

    def add_memory(self, mem_type):
        self.module.mem_sec.append(mem_type)
        if self.mem_names.imported + len(self.module.mem_sec) > 1:
            return new_verification_error("only one memory block allowed")
        return None

    def add_global(self, global_type, expr):
        self.module.global_sec.append(Global(global_type=global_type, init=expr))
        return self.glb_names.imported + len(self.module.global_sec) - 1

    def add_export(self, name, kind, idx):
        self.module.export_sec.append(Export(name=name,
                                             export_desc=ExportDesc(tag=kind,
                                                                    idx=idx)))

    def add_start(self, _var):
        f_idx, err = self.get_func_idx(_var)
        self.module.start_sec = f_idx
        return err

    def add_elem(self, _var, offset, init_data):
        if _var != "":
            _, err = self.get_table_idx(_var)
            if err is not None:
                return err
        self.module.elem_sec.append(Elem(table_idx=0,
                                         offset_expr=offset,
                                         vec_init=init_data))
        return None

    def add_data(self, _var: str, offset: list, init_data: str):
        if _var != "":
            _, err = self.get_mem_idx(_var)
            if err is not None:
                return err
        self.module.data_sec.append(Data(mem_idx=0,
                                         offset_expr=offset,
                                         vec_init=escape(init_data)))


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
