#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: vm.py
@time: 2020/8/19 21:28
@project: wasm-python-book
@desc:
"""
from binary.module import Module, ImportTagFunc
from binary.opcodes import Call
from interpreter.instr_control import call
from interpreter.instructions import instr_table
from interpreter.native import *
from interpreter.vm_func import new_internal_func, new_external_func
from interpreter.vm_global import GlobalVar
from interpreter.vm_memory import Memory
from interpreter.vm_stack_control import ControlStack, ControlFrame
from interpreter.vm_stack_operand import OperandStack
from interpreter.vm_table import Table


class VM(OperandStack, ControlStack):
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

    def init_mem(self):
        """
        内存初始化
        Wasm模块可以导入或者定义一块内存，还有一个数据段专门用来存放内存初始化数据
        """
        # 如果模块定义了内存，就先创建内存实例并分配必要的内存页
        if len(self.module.mem_sec) > 0:
            self.memory = Memory(self.module.mem_sec[0])

        for data in self.module.data_sec:
            for instr in data.offset:
                self.exec_instr(instr)

            # 指令执行完毕后，留在操作数栈顶的就是内存起始地址
            self.memory.write(self.pop_u64(), data.init)

    def init_globals(self):
        for global_var in self.module.global_sec:
            for instr in global_var.init:
                self.exec_instr(instr)
            self.globals.append(GlobalVar(global_var.type, self.pop_u64()))

    def init_funcs(self):
        self.link_native_funcs()
        for i, ft_idx in enumerate(self.module.func_sec):
            ft = self.module.type_sec[ft_idx]
            code = self.module.code_sec[i]
            self.funcs.append(new_internal_func(ft, code))

    def link_native_funcs(self):
        """外部函数的初始化"""
        for imp in self.module.import_sec:
            if imp.desc.tag == ImportTagFunc and imp.module == "env":
                ft = self.module.type_sec[imp.desc.func_type]
                name = imp.name
                if name == "print_char":
                    self.funcs.append(new_external_func(ft, print_char))
                elif name == "assert_true":
                    self.funcs.append(new_external_func(ft, assert_true))
                elif name == "assert_false":
                    self.funcs.append(new_external_func(ft, assert_false))
                elif name == "assert_eq_i32":
                    self.funcs.append(new_external_func(ft, assert_eq_i32))
                elif name == "assert_eq_i64":
                    self.funcs.append(new_external_func(ft, assert_eq_i64))
                elif name == "assert_eq_f32":
                    self.funcs.append(new_external_func(ft, assert_eq_f32))
                elif name == "assert_eq_f64":
                    self.funcs.append(new_external_func(ft, assert_eq_f64))
                else:
                    raise Exception("TODO")

    def init_table(self):
        if len(self.module.table_sec) > 0:
            self.table = Table(self.module.table_sec[0])
        for elem in self.module.elem_sec:
            for instr in elem.offset:
                self.exec_instr(instr)
            offset = self.pop_u32()
            for i, func_idx in enumerate(elem.init):
                self.table.set_elem(offset + i, self.funcs[func_idx])

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

    def exec_code(self, idx):
        """一条一条执行函数指令"""
        code = self.module.code_sec[idx]
        for _, instr in enumerate(code.expr):
            self.exec_instr(instr)

    def exec_instr(self, instr):
        """指令分派逻辑：采用查表法"""
        instr_table[instr.opcode](self, instr.args)

    def loop(self, verbose_flag):
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


def get_main_func_idx(module):
    for exp in module.export_sec:
        if exp.desc.tag == ImportTagFunc and exp.name == "main":
            return exp.desc.idx
    raise Exception("main func not found")


def exec_main_func(module, verbose_flag=False):
    vm = VM(module)
    vm.init_mem()
    vm.init_globals()
    vm.init_funcs()
    vm.init_table()
    if module.start_sec is not None:
        call(vm, module.start_sec)
    else:
        call(vm, get_main_func_idx(module))
    vm.loop(verbose_flag)
