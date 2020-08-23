#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: instr_variable_test.py
@time: 2020/8/23 12:43
@project: wasm-python-book
@desc: 局部/全局变量指令单元测试
"""

import unittest

from binary.opcodes import *
from binary.types import GlobalType
from interpreter.instructions import instr_table
from interpreter import *
from interpreter.vm import VM
from interpreter.vm_global import GlobalVar


class TestVariableFunc(unittest.TestCase):
    def test_local(self):
        vm = VM()
        vm.slots = [123, 456, 789]
        vm.local_0_idx = 1

        instr_table[LocalGet](vm, uint32(1))
        self.assertEqual(vm.slots[2], vm.pop_u64())

        vm.push_u64(246)
        instr_table[LocalTee](vm, uint32(1))
        self.assertEqual(vm.slots[3], vm.slots[2])
        instr_table[LocalSet](vm, uint32(0))
        self.assertEqual(vm.slots[2], vm.slots[1])

    def test_global(self):
        vm = VM()
        vm.globals = [GlobalVar(GlobalType(mut=1), 100),
                      GlobalVar(GlobalType(mut=1), 200),
                      GlobalVar(GlobalType(mut=1), 300)]

        instr_table[GlobalGet](vm, uint32(0))
        instr_table[GlobalGet](vm, uint32(1))
        instr_table[GlobalGet](vm, uint32(2))
        instr_table[GlobalSet](vm, uint32(1))
        instr_table[GlobalSet](vm, uint32(0))
        instr_table[GlobalSet](vm, uint32(2))

        self.assertEqual(uint64(200), vm.globals[0].get_as_u64())
        self.assertEqual(uint64(300), vm.globals[1].get_as_u64())
        self.assertEqual(uint64(100), vm.globals[2].get_as_u64())
