#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: vm.py
@time: 2020/8/19 21:28
@project: wasm-python-book
@desc:
"""
from ch07.binary.module import Module
from ch07.binary.opcodes import Call
from ch07.interpreter.instr_control import call
from ch07.interpreter.instructions import instr_table
from ch07.interpreter.vm_memory import Memory
from ch07.interpreter.vm_stack_control import ControlStack, ControlFrame
from ch07.interpreter.vm_stack_operand import OperandStack
from ch07.interpreter.vm_global import GlobalVar


class VM(OperandStack, ControlStack):
    def __init__(self, module=None, memory=None):
        super(VM, self).__init__()
        if module is None:
            module = Module()
        self.module = module
        self.memory = memory
        # 用于存放模块实例的全局变量
        self.globals = []
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

    def exec_code(self, idx):
        """一条一条执行函数指令"""
        code = self.module.code_sec[idx]
        for _, instr in enumerate(code.expr):
            self.exec_instr(instr)

    def exec_instr(self, instr):
        """指令分派逻辑：采用查表法"""
        instr_table[instr.opcode](self, instr.args)

    def loop(self):
        depth = self.control_depth
        while self.control_depth >= depth:
            cf = self.top_control_frame
            if cf.pc == len(cf.instrs):
                self.exit_block()
            else:
                instr = cf.instrs[cf.pc]
                cf.pc += 1
                self.exec_instr(instr)


def exec_main_func(module):
    vm = VM(module)
    vm.init_mem()
    vm.init_globals()
    call(vm, module.start_sec)
    vm.loop()
