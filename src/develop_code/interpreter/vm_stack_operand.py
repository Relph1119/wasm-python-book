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

from interpreter import uint64, int64, uint32, int32, float32, float64


class OperandStack:
    def __init__(self, slots=None):
        if slots is None:
            slots = []
        self.slots = slots

    def push_u64(self, val):
        self.slots.append(val)

    def pop_u64(self) -> uint64:
        return self.slots.pop()

    def push_s64(self, val):
        self.push_u64(uint64(val))

    def pop_s64(self) -> int64:
        return int64(self.pop_u64())

    def push_u32(self, val):
        self.push_u64(uint64(val))

    def pop_u32(self) -> uint32:
        return uint32(self.pop_u64())

    def push_s32(self, val):
        self.push_u64(uint32(val))

    def pop_s32(self):
        return int32(self.pop_u64())

    def push_f32(self, val):
        val = struct.unpack('>l', struct.pack('>f', val))[0]
        self.push_u64(val)

    def pop_f32(self):
        val = self.pop_u64()
        val = struct.unpack('>f', struct.pack('>l', val))[0]
        return float32(val)

    def push_f64(self, val):
        val = struct.unpack('>q', struct.pack('>d', val))[0]
        self.push_u64(val)

    def pop_f64(self):
        val = self.pop_u64()
        val = struct.unpack('>d', struct.pack('>q', val))[0]
        return float64(val)

    def push_bool(self, val):
        if val:
            self.push_u64(1)
        else:
            self.push_u64(0)

    def pop_bool(self):
        return self.pop_u64() != 0
