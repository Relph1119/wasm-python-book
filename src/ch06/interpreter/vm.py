#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: vm.py
@time: 2020/8/19 21:28
@project: wasm-python-book
@desc:
"""
from ch06.binary.module import Module
from ch06.interpreter.instructions import instr_table
from ch06.interpreter.vm_memory import Memory
from ch06.interpreter.vm_stack_operand import OperandStack


class VM(OperandStack):
    def __init__(self, module=None, memory=None):
        super().__init__()
        if module is None:
            module = Module()
        self.module = module
        self.memory = memory

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
                self.exe_instr(instr)

            # 指令执行完毕后，留在操作数栈顶的就是内存起始地址
            self.memory.write(self.pop_u64(), data.init)

    def exec_code(self, idx):
        """一条一条执行函数指令"""
        code = self.module.code_sec[idx]
        for _, instr in enumerate(code.expr):
            self.exe_instr(instr)

    def exe_instr(self, instr):
        """指令分派逻辑：采用查表法"""
        instr_table[instr.opcode](self, instr.args)


def exec_main_func(module):
    idx = int(module.start_sec) - len(module.import_sec)
    vm = VM(module)
    vm.init_mem()
    vm.exec_code(idx)
