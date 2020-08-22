#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: instr_memory_test.py
@time: 2020/8/22 14:45
@project: wasm-python-book
@desc: 内存指令单元测试
"""

import unittest

from binary.instruction import MemArg
from binary.opcodes import *
from binary.types import MemType
from interpreter.instructions import *
from interpreter.vm import VM
from interpreter.vm_memory import Memory
from test.interpreter.instr_numeric_test import push_val, pop_val


class TestInstrMemoryFunc(unittest.TestCase):
    def test_mem_size_and_grow(self):
        mem = Memory(mem_type=MemType(min=2))
        vm = VM(memory=mem)

        instr_table[MemorySize](vm, None)
        self.assertEqual(uint64(2), vm.pop_u64())

        vm.push_u32(3)
        instr_table[MemoryGrow](vm, None)
        self.assertEqual(uint64(2), vm.pop_u64())

        instr_table[MemorySize](vm, None)
        self.assertEqual(uint64(5), vm.pop_u64())

    def test_mem_ops(self):
        mem = Memory(mem_type=MemType(min=1))
        vm = VM(memory=mem)
        self.mem_op(vm, I32Store, I32Load, 0x10, 0x01, int32(100))
        self.mem_op(vm, I64Store, I64Load, 0x20, 0x02, int64(123))
        self.mem_op(vm, F32Store, F32Load, 0x30, 0x03, float32(1.5))
        self.mem_op(vm, F64Store, F64Load, 0x40, 0x04, 1.5)
        self.mem_op(vm, I32Store8, I32Load8S, 0x50, 0x05, int32(-100))
        self.mem_op(vm, I32Store8, I32Load8U, 0x60, 0x06, int32(100))
        self.mem_op(vm, I32Store16, I32Load16S, 0x70, 0x07, int32(-10000))
        self.mem_op(vm, I32Store16, I32Load16U, 0x80, 0x08, int32(10000))
        self.mem_op(vm, I64Store8, I64Load8S, 0x90, 0x09, int32(-100))
        self.mem_op(vm, I64Store8, I64Load8U, 0xA0, 0x0A, int32(100))
        self.mem_op(vm, I64Store16, I64Load16S, 0xB0, 0x0B, int32(-10000))
        self.mem_op(vm, I64Store16, I64Load16U, 0xC0, 0x0C, int32(10000))
        self.mem_op(vm, I64Store32, I64Load32S, 0xD0, 0x0D, int32(-1000000))
        self.mem_op(vm, I64Store32, I64Load32U, 0xE0, 0x0E, int32(1000000))

    def mem_op(self, vm, store_op, load_op, offset, i, val):
        mem_arg = MemArg(offset=offset)

        # store
        vm.push_u32(i)
        push_val(vm, val)
        instr_table[store_op](vm, mem_arg)

        # load
        vm.push_u32(i)
        instr_table[load_op](vm, mem_arg)

        # check
        self.assertEqual(val, pop_val(vm, val))
