#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: vm.py
@time: 2020/8/19 21:28
@project: wasm-python-book
@desc:
"""
from ch11.binary.module import Module, ImportTagFunc, ImportTagTable, ImportTagMem, ImportTagGlobal, ExportTagFunc, \
    ExportTagTable, ExportTagMem, ExportTagGlobal
from ch11.binary.opcodes import Call
from ch11.instance import module
from ch11.interpreter.instructions import instr_table
from ch11.interpreter.vm_func import new_internal_func, new_external_func
from ch11.interpreter.vm_global import GlobalVar
from ch11.interpreter.vm_memory import Memory
from ch11.interpreter.vm_stack_control import ControlStack, ControlFrame
from ch11.interpreter.vm_stack_operand import OperandStack
from ch11.interpreter.vm_table import Table
from ch11.validator.module_validator import validate


class VM(OperandStack, ControlStack, module.Module):
    def __init__(self, module=None, memory=None):
        super(VM, self).__init__()
        if module is None:
            module = Module()
        self.module = module
        self.memory = memory
        # 用于存放模块实例的全局变量
        self.globals = []
        # 用于记录内/外部函数
        self.funcs = []
        self.table = None
        # 用来记录当前函数的第一个局部变量
        self.local_0_idx = None
        self.frames = []
        self.slots = []

    def link_imports(self, mm):
        for imp in self.module.import_sec:
            m = mm[imp.module]
            if m is None:
                raise Exception("module not found: " + imp.module)
            else:
                self.link_import(m, imp)

    def link_import(self, m, imp):
        exported = m.get_member(imp.name)
        if exported is None:
            raise Exception("unknown import: %s.%s" % (imp.module, imp.name))

        type_matched = False
        if isinstance(exported, module.Function):
            if imp.desc.tag == ImportTagFunc:
                exported_ft = self.module.type_sec[imp.desc.func_type]
                type_matched = is_func_type_match(exported_ft, exported.type)
                self.funcs.append(new_external_func(exported_ft, exported))
        elif isinstance(exported, module.Table):
            if imp.desc.tag == ImportTagTable:
                type_matched = is_limits_match(imp.desc.table.limits, exported.type.limits)
                self.table = exported
        elif isinstance(exported, module.Memory):
            if imp.desc.tag == ImportTagMem:
                type_matched = is_limits_match(imp.desc.mem, exported.type)
                self.memory = exported
        elif isinstance(exported, module.Global):
            if imp.desc.tag == ImportTagGlobal:
                type_matched = is_global_type_match(imp.desc.global_type, exported.type)
                self.globals.append(exported)

        if not type_matched:
            raise Exception("incompatible import type: %s.%s" % (imp.module, imp.name))

    def init_mem(self):
        """
        内存初始化
        Wasm模块可以导入或者定义一块内存，还有一个数据段专门用来存放内存初始化数据
        """
        # 如果模块定义了内存，就先创建内存实例并分配必要的内存页
        if len(self.module.mem_sec) > 0:
            self.memory = Memory(self.module.mem_sec[0])

        for data in self.module.data_sec:
            self.exec_const_expr(data.offset)

            # 指令执行完毕后，留在操作数栈顶的就是内存起始地址
            self.memory.write(self.pop_u64(), data.init)

    def init_globals(self):
        for global_var in self.module.global_sec:
            self.exec_const_expr(global_var.init)
            self.globals.append(GlobalVar(global_var.type, self.pop_u64()))

    def init_funcs(self):
        for i, ft_idx in enumerate(self.module.func_sec):
            ft = self.module.type_sec[ft_idx]
            code = self.module.code_sec[i]
            self.funcs.append(new_internal_func(self, ft, code))

    def init_table(self):
        if len(self.module.table_sec) > 0:
            self.table = Table(self.module.table_sec[0])
        for elem in self.module.elem_sec:
            for instr in elem.offset:
                self.exec_instr(instr)
            offset = self.pop_u32()
            for i, func_idx in enumerate(elem.init):
                self.table.set_elem(offset + i, self.funcs[func_idx])

    def exec_const_expr(self, expr):
        for instr in expr:
            self.exec_instr(instr)

    def exec_start_func(self):
        if self.module.start_sec is not None:
            idx = self.module.start_sec
            self.funcs[idx].call(None)

    def enter_block(self, opcode, bt, instrs):
        """
        进入函数（或控制块）时使用
        """
        bp = self.stack_size - len(bt.param_types)
        cf = ControlFrame(opcode, bt, instrs, bp)
        self.push_control_frame(cf)
        if opcode == Call:
            self.local_0_idx = int(bp)

    def exit_block(self):
        cf = self.pop_control_frame()
        self.clear_block(cf)

    def clear_block(self, cf):
        results = self.pop_u64s(len(cf.bt.result_types))
        self.pop_u64s(self.stack_size - cf.bp)
        self.push_u64s(results)
        if cf.opcode == Call and self.control_depth > 0:
            last_call_frame, _ = self.top_call_frame()
            self.local_0_idx = int(last_call_frame.bp)

    def reset_block(self, cf):
        results = self.pop_u64s(len(cf.bt.param_types))
        self.pop_u64s(self.stack_size - cf.bp)
        self.push_u64s(results)

    def loop(self, verbose_flag=False):
        depth = self.control_depth
        while self.control_depth >= depth:
            cf = self.top_control_frame
            if cf.pc == len(cf.instrs):
                self.exit_block()
            else:
                instr = cf.instrs[cf.pc]
                if verbose_flag:
                    print("PC={}, opcode={}, instrs={}, slots={}".format(cf.pc, instr.opcode,
                                                                         instr_table[instr.opcode].__name__,
                                                                         self.slots))
                cf.pc += 1
                self.exec_instr(instr)

    def exec_instr(self, instr):
        """指令分派逻辑：采用查表法"""
        instr_table[instr.opcode](self, instr.args)

    def get_member(self, name):
        for exp in self.module.export_sec:
            if exp.name == name:
                idx = exp.desc.idx
                tag = exp.desc.tag
                if tag == ExportTagFunc:
                    return self.funcs[idx]
                elif tag == ExportTagTable:
                    return self.table
                elif tag == ExportTagMem:
                    return self.memory
                elif tag == ExportTagGlobal:
                    return self.globals[idx]
        return None

    def invoke_func(self, name, args=None):
        if args is None:
            args = []
        m = self.get_member(name)
        if m is not None:
            return m.call(args)

    def get_global_val(self, name):
        m = self.get_member(name)
        if m is not None:
            return m.get(), None
        return None, "global not found: " + name

    def set_global_var(self, name, val):
        m = self.get_member(name)
        if m is not None:
            m.set(val)
            return None
        return "global not found: " + name


def new(m, mm):
    inst, err = None, None
    err = validate(m)
    if err is not None:
        return None, err
    try:
        inst = new_vm(m, mm)
    except Exception as e:
        err = e
    return inst, err


def new_vm(m, mm):
    vm = VM(m)
    vm.link_imports(mm)
    vm.init_funcs()
    vm.init_table()
    vm.init_mem()
    vm.init_globals()
    vm.exec_start_func()
    return vm


def is_func_type_match(expected, actual) -> bool:
    return str(expected) == str(actual)


def is_global_type_match(expected, actual) -> bool:
    return actual.val_type == expected.val_type and actual.mut == expected.mut


def is_limits_match(expected, actual) -> bool:
    return actual.min >= expected.min and \
           (expected.max == 0 or 0 < actual.max <= expected.max)
