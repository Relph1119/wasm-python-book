#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: vm.py
@time: 2020/8/19 21:28
@project: wasm-python-book
@desc:
"""
from binary.module import Module
from interpreter.instructions import instr_table
from interpreter.vm_stack_operand import OperandStack


class VM(OperandStack):
    def __init__(self, module=None):
        super().__init__()
        if module is None:
            module = Module()
        self.module = module

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
    vm.exec_code(idx)
