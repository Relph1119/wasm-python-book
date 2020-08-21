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

from interpreter import float32, int64, uint64, int32, uint32
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
