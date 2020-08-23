#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: instruction.py
@time: 2020/8/18 18:28
@project: wasm-python-book
@desc:
"""
from ch09.binary.opnames import opnames


class Expr(list):
    """
    表达式
    expr  : instr*|0x0b
    """

    def __init__(self):
        super().__init__()


class Instruction:
    """指令"""

    def __init__(self):
        # 操作码
        self.opcode = None
        # 操作数
        self.args = None

    def get_opname(self):
        return opnames[self.opcode]

    def __str__(self):
        return opnames[self.opcode]


class BlockArgs:
    """block和loop指令的参数"""

    def __init__(self):
        # block type:
        # -1表示i32类型结果，-2表示i64类型结果，
        # -3表示f32类型结果，-4表示f64类型结果，
        # -64表示没有结果
        self.bt = None
        # 内嵌的指令序列
        self.instrs = []


class IfArgs:
    """if指令的参数"""

    def __init__(self):
        # block type
        self.bt = None
        self.instrs1 = []
        self.instrs2 = []


class BrTableArgs:
    """br_table指令的参数"""

    def __init__(self, labels=None, default=None):
        # 跳转表
        if labels is None:
            labels = []
        self.labels = labels
        # 默认跳转标签
        self.default = default


class MemArg:
    """内存指令参数"""

    def __init__(self, align=0, offset=None):
        # 对齐提示
        self.align = align
        # 内存偏移量
        self.offset = offset
