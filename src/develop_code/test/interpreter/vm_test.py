#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: vm_test.py
@time: 2020/8/21 9:23
@project: wasm-python-book
@desc: VM虚拟机栈单元测试
"""
import unittest

from binary.types import MemType, GlobalType, ValTypeI32
from interpreter import float32, int64, uint64, int32, uint32
from interpreter.vm_global import GlobalVar
from interpreter.vm_memory import Memory
from interpreter.vm_stack_operand import OperandStack


class TestVMFunc(unittest.TestCase):
    def test_operand_stack(self):
        stack = OperandStack()
        stack.push_bool(True)
        stack.push_bool(False)
        stack.push_u32(1)
        stack.push_s32(-2)
        stack.push_u64(3)
        stack.push_s64(-4)
        stack.push_f32(5.5)
        stack.push_f64(6.5)

        self.assertEqual(6.5, stack.pop_f64())
        self.assertEqual(float32(5.5), stack.pop_f32())
        self.assertEqual(int64(-4), stack.pop_s64())
        self.assertEqual(uint64(3), stack.pop_u64())
        self.assertEqual(int32(-2), stack.pop_s32())
        self.assertEqual(uint32(1), stack.pop_u32())
        self.assertEqual(False, stack.pop_bool())
        self.assertEqual(True, stack.pop_bool())
        self.assertEqual(0, len(stack.slots))

    def test_local_var(self):
        stack = OperandStack()
        stack.push_u32(1)
        stack.push_u32(3)
        stack.push_u32(5)

        self.assertEqual(uint64(3), stack.get_operand(1))
        stack.set_operand(1, 7)
        self.assertEqual(uint64(7), stack.get_operand(1))

    def test_mem(self):
        mem = Memory(mem_type=MemType(min=1))

        buf = [0x01, 0x02, 0x03]
        mem.write(10, buf)
        buf = mem.read(11, buf)
        self.assertEqual([0x02, 0x03, 0x00], buf)

        self.assertEqual(1, mem.size)
        self.assertEqual(1, mem.grow(3))
        self.assertEqual(4, mem.size)

    def test_global_var(self):
        g = GlobalVar(gt=GlobalType(ValTypeI32, 1), val=0)

        g.set_as_u64(100)
        self.assertEqual(uint64(100), g.get_as_u64())
