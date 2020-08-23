#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: vm_stack_control.py
@time: 2020/8/23 10:41
@project: wasm-python-book
@desc: 控制帧
"""
from ch08.binary.opcodes import Call


class ControlFrame:
    """控制帧"""

    def __init__(self, opcode, bt, instrs, bp):
        self.opcode = opcode
        self.bt = bt
        self.instrs = instrs
        self.bp = bp
        # 程序计数器，用于记录指令执行的位置
        self.pc = 0


class ControlStack:
    def __init__(self):
        self.frames = []

    @property
    def control_depth(self):
        return len(self.frames)

    @property
    def top_control_frame(self):
        return self.frames[-1]

    def top_call_frame(self):
        n = len(self.frames) - 1
        while n >= 0:
            cf = self.frames[n]
            if cf.opcode == Call:
                return cf, len(self.frames) - 1 - n
            n -= 1
        return None, -1

    def push_control_frame(self, cf):
        self.frames.append(cf)

    def pop_control_frame(self):
        return self.frames.pop()
