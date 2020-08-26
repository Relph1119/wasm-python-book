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

from binary.types import MemType, GlobalType, ValTypeI32, TableType, Limits, FuncType, ValTypeI64, ValTypeF32, \
    ValTypeF64
from interpreter import float32, int64, uint64, int32, uint32
from interpreter.vm_func import VMFunc
from interpreter.vm_global import GlobalVar
from interpreter.vm_memory import Memory
from interpreter.vm_stack_operand import OperandStack
from interpreter.vm_table import Table


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

    def test_table(self):
        limits = Limits(min=10, max=20)
        table = Table(table_type=TableType(limits=limits))
        fs = [VMFunc(ft=FuncType(param_types=[ValTypeI32])),
              VMFunc(ft=FuncType(param_types=[ValTypeI64])),
              VMFunc(ft=FuncType(param_types=[ValTypeF32])),
              VMFunc(ft=FuncType(param_types=[ValTypeF64]))]

        table.set_elem(6, fs[0])
        table.set_elem(7, fs[1])
        table.set_elem(8, fs[2])
        table.set_elem(9, fs[3])
        self.assertEqual(fs[0], table.get_elem(6))
        self.assertEqual(fs[1], table.get_elem(7))
        self.assertEqual(fs[2], table.get_elem(8))
        self.assertEqual(fs[3], table.get_elem(9))

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
        g = GlobalVar(gt=GlobalType(ValTypeI32, 1),
                      val=0)

        g.set_as_u64(100)
        self.assertEqual(uint64(100), g.get_as_u64())
