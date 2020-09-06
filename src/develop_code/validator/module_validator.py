#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: module_validator.py
@time: 2020/8/24 8:43
@project: wasm-python-book
@desc: 模块验证
"""
from binary.module import ImportTagFunc, ImportTagTable, ImportTagMem, ImportTagGlobal, ExportTagFunc, ExportTagTable, \
    ExportTagMem, ExportTagGlobal
from binary.opcodes import I32Const, I64Const, F32Const, F64Const, GlobalGet
from binary.types import FuncType, ValTypeI32, ValTypeI64, ValTypeF32, ValTypeF64
from validator.code_validator import validate_code


class ModuleValidator:
    def __init__(self, module=None):
        self.module = module
        self.imported_funcs = []
        self.imported_tables = []
        self.imported_memories = []
        self.imported_globals = []
        self.global_types = []

    def validate(self):
        self.validate_import_sec()
        self.validate_func_sec()
        self.validate_table_sec()
        self.validate_mem_sec()
        self.validate_global_sec()
        self.validate_export_sec()
        self.validate_start_sec()
        self.validate_elem_sec()
        self.validate_code_sec()
        self.validate_data_sec()

    def validate_import_sec(self):
        """
        1.如果导入的是函数，类型索引有效
        2.最多只能导入一张表，且类型有效
        3.最多只能导入一块内存，且类型有效
        :return:
        """
        for i, imp in enumerate(self.module.import_sec):
            tag = imp.desc.tag
            if tag == ImportTagFunc:
                self.imported_funcs.append(imp)
                if int(imp.desc.func_type) >= self.get_type_count():
                    raise Exception("import[%d]: unknown type: %d" %
                                    (i, imp.desc.func_type))
            elif tag == ImportTagTable:
                if len(self.imported_tables) > 0:
                    raise Exception("multiple tables")
                self.imported_tables.append(imp)
                err = validate_table_type(imp)
                if err != "":
                    raise Exception("import[%d]: %s" % (i, err))
            elif tag == ImportTagMem:
                if len(self.imported_memories) > 0:
                    raise Exception("multiple memories")
                self.imported_memories.append(imp)
                err = validate_memory_type(imp.desc.mem)
                if err != "":
                    raise Exception("import[%d]: %s" % (i, err))
            elif tag == ImportTagGlobal:
                self.imported_globals.append(imp)
                self.global_types.append(imp.desc.global_type)

    def validate_func_sec(self):
        """
        函数类型有效
        :return:
        """
        for i, ft_idx in enumerate(self.module.func_sec):
            if int(ft_idx) >= self.get_type_count():
                raise Exception("func[%d]: unknown type: %d" % (i, ft_idx))

    def validate_table_sec(self):
        """
        1.如果已经导入表，则不允许有表段
        2.否则，只能定义一张表，且类型有效
        :return:
        """
        for i, table in enumerate(self.module.table_sec):
            # TODO >
            if i + self.get_imported_table_count() > 0:
                raise Exception("multiple tables")
            err = validate_table_type(table.limits)
            if err != "":
                raise Exception("table[%d]: %s" % (i, err))

    def validate_mem_sec(self):
        """
        1.如果已经导入内存，则不允许有内存段
        2.否则，只能定义一块内存，且类型有效
        :return:
        """
        for i, mem in enumerate(self.module.mem_sec):
            if i + self.get_imported_mem_count() > 0:
                raise Exception("multiple memories")
            err = validate_memory_type(mem)
            if err != "":
                raise Exception("mem[%d]: %s" % (i, err))

    def validate_global_sec(self):
        """
        全局项的初始值表达式有效
        :return:
        """
        for i, g in enumerate(self.module.global_sec):
            err = self.validate_const_expr(g.init, g.type.val_type)
            if err != "":
                raise Exception("global[%d]: %s" % (i + self.get_imported_global_count(), err))
            self.global_types.append(g.type)

    def validate_export_sec(self):
        """
        导出项的导出名唯一，且索引有效
        :return:
        """
        exported_names = dict()
        for i, exp in enumerate(self.module.export_sec):
            if exported_names.get(exp.name, False):
                raise Exception("duplicate export name: %s" % exp.name)
            else:
                exported_names[exp.name] = True

            tag = exp.desc.tag
            if tag == ExportTagFunc:
                if int(exp.desc.idx) >= self.get_func_count():
                    raise Exception("export[%d]: unknown function: %d" % (i, exp.desc.idx))
            elif tag == ExportTagTable:
                if int(exp.desc.idx) >= self.get_table_count():
                    raise Exception("export[%d]: unknown table: %d" % (i, exp.desc.idx))
            elif tag == ExportTagMem:
                if int(exp.desc.idx) >= self.get_mem_count():
                    raise Exception("export[%d]: unknown memory: %d" % (i, exp.desc.idx))
            elif tag == ExportTagGlobal:
                if int(exp.desc.idx) >= self.get_global_count():
                    raise Exception("export[%d]: unknown global: %d" % (i, exp.desc.idx))

    def validate_start_sec(self):
        """
        函数索引有效，且函数类型有效（不能有参数或返回值）
        :return:
        """
        if self.module.start_sec is not None:
            idx = int(self.module.start_sec)
            ft, ok = self.get_func_type(idx)
            if not ok:
                raise Exception("start function: unknown function: %d" % idx)
            if len(ft.param_types) > 0 or len(ft.result_types) > 0:
                raise Exception("start function: invalid type: %d" % idx)

    def validate_elem_sec(self):
        """
        1.元素项的表索引必须为0，偏移量表达式有效
        2.列出的函数索引有效
        :return:
        """
        for i, elem in enumerate(self.module.elem_sec):
            if int(elem.table) >= self.get_table_count():
                raise Exception("elem[%d]: unknown table: %d" % (i, elem.table))
            err = self.validate_const_expr(elem.offset, ValTypeI32)
            if err != "":
                raise Exception("elem[%d]: %s", (i, err))
            for j, func_idx in enumerate(elem.init):
                if int(func_idx) >= self.get_func_count():
                    raise Exception("elem[%d][%d]: unknown function: %d" % (i, j, func_idx))

    def validate_code_sec(self):
        """
        代码数量和函数数量一致，且字节码有效
        :return:
        """
        if len(self.module.code_sec) != len(self.module.func_sec):
            raise Exception("invalid code count")
        for i, code in enumerate(self.module.code_sec):
            ft_idx = self.module.func_sec[i]
            ft = self.module.type_sec[ft_idx]
            validate_code(self, i, code, ft)

    def validate_data_sec(self):
        """
        内存索引必须为0，偏移量表达式有效
        :return:
        """
        for i, data in enumerate(self.module.data_sec):
            if int(data.mem) >= self.get_mem_count():
                raise Exception("data[%d]: unknown memory: %d" % (i, data.mem))
            err = self.validate_const_expr(data.offset, ValTypeI32)
            if err != "":
                raise Exception("data[%d]: %s" % (i, err))

    def validate_const_expr(self, expr, expected_type):
        if len(expr) > 1:
            for instr in expr:
                if instr.opcode in [I32Const, I64Const, F32Const, F64Const, GlobalGet]:
                    pass
                else:
                    return "constant expression required"

            return "type mismatch"

        actual_type = 0
        if len(expr) > 0:
            opcode = expr[0].opcode
            if opcode == I32Const:
                actual_type = ValTypeI32
            elif opcode == I64Const:
                actual_type = ValTypeI64
            elif opcode == F32Const:
                actual_type = ValTypeF32
            elif opcode == F64Const:
                actual_type = ValTypeF64
            elif opcode == GlobalGet:
                g_idx = expr[0].args
                if int(g_idx) >= len(self.global_types):
                    return "unknown global: %d" % g_idx
                actual_type = self.global_types[g_idx].val_type
            else:
                return "constant expression required"

        if actual_type != expected_type:
            return "type mismatch"

        return ""

    def get_import_func_count(self):
        return len(self.imported_funcs)

    def get_imported_table_count(self):
        return len(self.imported_tables)

    def get_imported_mem_count(self):
        return len(self.imported_memories)

    def get_imported_global_count(self):
        return len(self.imported_globals)

    def get_internal_func_count(self):
        return len(self.module.func_sec)

    def get_internal_table_count(self):
        return len(self.module.table_sec)

    def get_internal_mem_count(self):
        return len(self.module.mem_sec)

    def get_internal_global_count(self):
        return len(self.module.global_sec)

    def get_type_count(self):
        return len(self.module.type_sec)

    def get_func_count(self):
        return self.get_import_func_count() + self.get_internal_func_count()

    def get_table_count(self):
        return self.get_imported_table_count() + self.get_internal_table_count()

    def get_mem_count(self):
        return self.get_imported_mem_count() + self.get_internal_mem_count()

    def get_global_count(self):
        return self.get_imported_global_count() + self.get_internal_global_count()

    def get_func_type(self, f_idx):
        if f_idx < self.get_import_func_count():
            ft_idx = self.imported_funcs[f_idx].desc.func_type
            return self.module.type_sec[ft_idx], True

        if f_idx < self.get_func_count():
            ft_idx = self.module.func_sec[f_idx - self.get_import_func_count()]
            return self.module.type_sec[ft_idx], True

        return FuncType(), False


def validate(module):
    err = None
    try:
        v = ModuleValidator(module)
        v.validate()
    except Exception as e:
        err = e
    return err


def validate_table_type(limits):
    return validate_limits(limits, (1 << 32) - 1, "table")


def validate_memory_type(limits):
    return validate_limits(limits, 1 << 16, "mem")


def validate_limits(limits, k, kind):
    if limits.min > k:
        if kind == "mem":
            return "memory size must be at most 65536 pages (4GiB)"
        else:
            # TODO
            pass
    if limits.tag == 1:
        if limits.max > k:
            if kind == "mem":
                return "memory size must be at most 65536 pages (4GiB)"
            else:
                # TODO
                pass
        if limits.max < limits.min:
            return "size minimum must not be greater than maximum"

    return ""
