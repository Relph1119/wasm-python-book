#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: vm_stack_operand.py
@time: 2020/8/19 21:13
@project: wasm-python-book
@desc: 虚拟机框架单元测试
"""
import struct

from ch11.interpreter import uint64, int64, uint32, int32, float32, float64


class OperandStack:
    def __init__(self, slots=None):
        if slots is None:
            slots = []
        self.slots = slots

    @property
    def stack_size(self):
        # 获取操作数栈的长度
        return len(self.slots)

    def get_operand(self, idx):
        # 按索引读操作数
        return self.slots[idx]

    def set_operand(self, idx, val):
        # 按索引写操作数
        self.slots[idx] = val

    def push_u64s(self, vals):
        self.slots.extend(vals)

    def pop_u64s(self, n):
        vals = self.slots[len(self.slots) - n:]
        self.slots = self.slots[:len(self.slots) - n]
        return vals

    def push_u64(self, val):
        self.slots.append(uint64(val))

    def pop_u64(self) -> uint64:
        return uint64(self.slots.pop())

    def push_numeric(self, val):
        self.slots.append(val)

    def pop_numeric(self):
        return self.slots.pop()

    def push_s64(self, val):
        self.push_numeric(uint64(val))

    def pop_s64(self) -> int64:
        return int64(self.pop_numeric())

    def push_u32(self, val):
        self.push_numeric(uint64(val))

    def pop_u32(self) -> uint32:
        return uint32(self.pop_numeric())

    def push_s32(self, val):
        self.push_numeric(uint32(val))

    def pop_s32(self):
        return int32(self.pop_numeric())

    def push_f32(self, val):
        val = struct.unpack('>l', struct.pack('>f', val))[0]
        self.push_numeric(val)

    def pop_f32(self):
        val = self.pop_numeric()
        val = struct.unpack('>f', struct.pack('>l', val))[0]
        return float32(val)

    def push_f64(self, val):
        val = struct.unpack('>q', struct.pack('>d', val))[0]
        self.push_numeric(val)

    def pop_f64(self):
        val = self.pop_numeric()
        val = struct.unpack('>d', struct.pack('>q', val))[0]
        return float64(val)

    def push_bool(self, val):
        if val:
            self.push_numeric(1)
        else:
            self.push_numeric(0)

    def pop_bool(self):
        return self.pop_numeric() != 0
