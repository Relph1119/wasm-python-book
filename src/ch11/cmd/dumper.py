#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: dumper.py
@time: 2020/8/19 10:54
@project: wasm-python-book
@desc: wasm-objdump工具
"""
from ch11.binary.module import ImportTagFunc, ImportTagTable, ImportTagMem, ImportTagGlobal, ExportTagFunc, \
    ExportTagTable, ExportTagMem, ExportTagGlobal
from ch11.binary.opcodes import *
from ch11.binary.types import val_type_to_str


class Dumper:
    def __init__(self, module):
        self.module = module
        self.imported_func_count = 0
        self.imported_table_count = 0
        self.imported_mem_count = 0
        self.imported_global_count = 0

    def dump_type_sec(self):
        print("Type[%d]:" % len(self.module.type_sec))
        for i, ft in enumerate(self.module.type_sec):
            print("  type[%d]: %s" % (i, ft))

    def dump_import_sec(self):
        print("Import[%d]:" % len(self.module.import_sec))
        for _, imp in enumerate(self.module.import_sec):
            tag = imp.desc.tag
            if tag == ImportTagFunc:
                print("  func[%d]: %s.%s, sig=%d" %
                      (self.imported_func_count, imp.module, imp.name, imp.desc.func_type))
                self.imported_func_count += 1
            elif tag == ImportTagTable:
                print("  table[%d]: %s.%s, %s" %
                      (self.imported_table_count, imp.module, imp.name, imp.desc.table.limits))
                self.imported_table_count += 1
            elif tag == ImportTagMem:
                print("  memory[%d]: %s.%s, %s" %
                      (self.imported_mem_count, imp.module, imp.name, imp.desc.mem))
                self.imported_mem_count += 1
            elif tag == ImportTagGlobal:
                print("  global[%d]: %s.%s, %s" %
                      (self.imported_global_count, imp.module, imp.name, imp.desc.global_type))
                self.imported_global_count += 1

    def dump_func_sec(self):
        print("Function[%d]:" % len(self.module.func_sec))
        for i, sig in enumerate(self.module.func_sec):
            print("  func[%d]: sig=%d" %
                  (self.imported_func_count + i, sig))

    def dump_table_sec(self):
        print("Table[%d]:" % len(self.module.table_sec))
        for i, t in enumerate(self.module.table_sec):
            print("  table[%d]: %s" %
                  (self.imported_table_count + i, t.limits))

    def dump_mem_sec(self):
        print("Memory[%d]:" % len(self.module.mem_sec))
        for i, limits in enumerate(self.module.mem_sec):
            print("  memory[%d]: %s" %
                  (self.imported_mem_count + i, limits))

    def dump_global_sec(self):
        print("Global[%d]:" % len(self.module.global_sec))
        for i, g in enumerate(self.module.global_sec):
            print("  global[%d]: %s" %
                  (self.imported_global_count + i, g.type))

    def dump_export_sec(self):
        print("Export[%d]:" % len(self.module.export_sec))
        for _, exp in enumerate(self.module.export_sec):
            tag = exp.desc.tag
            if tag == ExportTagFunc:
                print("  func[%d]: name=%s" % (int(exp.desc.idx), exp.name))
            elif tag == ExportTagTable:
                print("  table[%d]: name=%s" % (int(exp.desc.idx), exp.name))
            elif tag == ExportTagMem:
                print("  memory[%d]: name=%s" % (int(exp.desc.idx), exp.name))
            elif tag == ExportTagGlobal:
                print("  global[%d]: name=%s" % (int(exp.desc.idx), exp.name))

    def dump_start_sec(self):
        print("Start:")
        if self.module.start_sec is not None:
            print("  func=%d" % self.module.start_sec)

    def dump_elem_sec(self):
        print("Element[%d]:" % len(self.module.elem_sec))
        for i, elem in enumerate(self.module.elem_sec):
            print("  elem[%d]: table=%d" % (i, elem.table))

    def dump_code_sec(self):
        print("Code[%d]:" % len(self.module.code_sec))
        for i, code in enumerate(self.module.code_sec):
            print("  func[%d]: locals=[" % (self.imported_func_count + i), end='')
            print(",".join(["%s x %d" % (val_type_to_str(locals.type), locals.n)
                            for locals in code.locals]), end='')
            print("]")
            self.dump_expr("    ", code.expr)

    def dump_data_sec(self):
        print("Data[%d]:" % len(self.module.data_sec))
        for i, data in enumerate(self.module.data_sec):
            print("  data[%d]: mem=%d" % (i, data.mem))

    def dump_custom_sec(self):
        print("Custom[%d]:" % len(self.module.custom_secs))
        for i, cs in enumerate(self.module.custom_secs):
            print("  custom[%d]: name=%s" % (i, cs.name))

    def dump_expr(self, indentation, expr):
        for _, instr in enumerate(expr):
            if instr.opcode in [Block, Loop]:
                args = instr.args
                bt = self.module.get_block_type(args.bt)
                print("%s%s %s" % (indentation, instr.get_opname(), bt))
                self.dump_expr(indentation + "  ", args.instrs)
                print("%s%s" % (indentation, "end"))
            elif instr.opcode == If:
                args = instr.args
                bt = self.module.get_block_type(args.bt)
                print("%s%s %s" % (indentation, "if", bt))
                self.dump_expr(indentation + "  ", args.instrs1)
                print("%s%s" % (indentation, "else"))
                self.dump_expr(indentation + "  ", args.instrs2)
                print("%s%s" % (indentation, "end"))
            else:
                if instr.args is not None:
                    print("{}{} {}".format(indentation, instr.get_opname(), instr.args))


def dump(module):
    d = Dumper(module)
    print("Version: 0x%02x" % d.module.version)
    d.dump_type_sec()
    d.dump_import_sec()
    d.dump_func_sec()
    d.dump_table_sec()
    d.dump_mem_sec()
    d.dump_global_sec()
    d.dump_export_sec()
    d.dump_start_sec()
    d.dump_elem_sec()
    d.dump_code_sec()
    d.dump_data_sec()
    d.dump_custom_sec()
