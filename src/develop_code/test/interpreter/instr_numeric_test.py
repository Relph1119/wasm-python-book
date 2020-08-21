#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: instr_numeric_test.py
@time: 2020/8/20 15:50
@project: wasm-python-book
@desc: 数值指令单元测试
"""
import unittest

from binary.opcodes import *
from interpreter.instr_numeric import i32_const, i64_const, f32_const, f64_const
from interpreter.instructions import instr_table, int32, int64, float32, float64
from interpreter.vm import VM


class TestInstrNumericFunc(unittest.TestCase):
    def test_const_ops(self):
        vm = VM()
        i32_const(vm, int32(100))
        i64_const(vm, int64(200))
        f32_const(vm, float32(1.5))
        f64_const(vm, 2.5)
        self.assertEqual(2.5, vm.pop_f64())
        self.assertEqual(float32(1.5), vm.pop_f32())
        self.assertEqual(int64(200), vm.pop_s64())
        self.assertEqual(int32(100), vm.pop_s32())

    def test_i32_cmp(self):
        self.i32_un_op(I32Eqz, 1, 0)
        self.i32_un_op(I32Eqz, 0, 1)
        self.i32_bin_op(I32Eq, 1, 1, 1)
        self.i32_bin_op(I32Eq, 1, -1, 0)
        self.i32_bin_op(I32Ne, 1, 1, 0)
        self.i32_bin_op(I32Ne, 1, -1, 1)
        self.i32_bin_op(I32LtS, -1, 1, 1)
        self.i32_bin_op(I32LtS, 1, -1, 0)
        self.i32_bin_op(I32LtU, -1, 1, 0)
        self.i32_bin_op(I32LtU, 1, -1, 1)
        self.i32_bin_op(I32GtS, -1, 1, 0)
        self.i32_bin_op(I32GtS, 1, -1, 1)
        self.i32_bin_op(I32GtU, -1, 1, 1)
        self.i32_bin_op(I32GtU, 1, -1, 0)
        self.i32_bin_op(I32LeS, -1, 1, 1)
        self.i32_bin_op(I32LeS, 1, -1, 0)
        self.i32_bin_op(I32LeU, -1, 1, 0)
        self.i32_bin_op(I32LeU, 1, -1, 1)
        self.i32_bin_op(I32GeS, -1, 1, 0)
        self.i32_bin_op(I32GeS, 1, -1, 1)
        self.i32_bin_op(I32GeU, -1, 1, 1)
        self.i32_bin_op(I32GeU, 1, -1, 0)

    def test_i64_cmp(self):
        self.i64_un_op(I64Eqz, 1, 0)
        self.i64_un_op(I64Eqz, 0, 1)
        self.i64_bin_op(I64Eq, 1, 1, 1)
        self.i64_bin_op(I64Eq, 1, -1, 0)
        self.i64_bin_op(I64Ne, 1, 1, 0)
        self.i64_bin_op(I64Ne, 1, -1, 1)
        self.i64_bin_op(I64LtS, -1, 1, 1)
        self.i64_bin_op(I64LtS, 1, -1, 0)
        self.i64_bin_op(I64LtU, -1, 1, 0)
        self.i64_bin_op(I64LtU, 1, -1, 1)
        self.i64_bin_op(I64GtS, -1, 1, 0)
        self.i64_bin_op(I64GtS, 1, -1, 1)
        self.i64_bin_op(I64GtU, -1, 1, 1)
        self.i64_bin_op(I64GtU, 1, -1, 0)
        self.i64_bin_op(I64LeS, -1, 1, 1)
        self.i64_bin_op(I64LeS, 1, -1, 0)
        self.i64_bin_op(I64LeU, -1, 1, 0)
        self.i64_bin_op(I64LeU, 1, -1, 1)
        self.i64_bin_op(I64GeS, -1, 1, 0)
        self.i64_bin_op(I64GeS, 1, -1, 1)
        self.i64_bin_op(I64GeU, -1, 1, 1)
        self.i64_bin_op(I64GeU, 1, -1, 0)

    def test_f32_cmp(self):
        self.f32_bin_cmp(F32Eq, 1.0, 1.0, 1)
        self.f32_bin_cmp(F32Eq, 1.0, 2.0, 0)
        self.f32_bin_cmp(F32Ne, 1.0, 1.0, 0)
        self.f32_bin_cmp(F32Ne, 1.0, 2.0, 1)
        self.f32_bin_cmp(F32Lt, 1.0, 2.0, 1)
        self.f32_bin_cmp(F32Lt, 2.0, 1.0, 0)
        self.f32_bin_cmp(F32Gt, 1.0, 2.0, 0)
        self.f32_bin_cmp(F32Gt, 2.0, 1.0, 1)
        self.f32_bin_cmp(F32Le, 1.0, 2.0, 1)
        self.f32_bin_cmp(F32Le, 2.0, 1.0, 0)
        self.f32_bin_cmp(F32Ge, 1.0, 2.0, 0)
        self.f32_bin_cmp(F32Ge, 2.0, 1.0, 1)

    def test_f64_cmp(self):
        self.f64_bin_cmp(F64Eq, 1.0, 1.0, 1)
        self.f64_bin_cmp(F64Eq, 1.0, 2.0, 0)
        self.f64_bin_cmp(F64Ne, 1.0, 1.0, 0)
        self.f64_bin_cmp(F64Ne, 1.0, 2.0, 1)
        self.f64_bin_cmp(F64Lt, 1.0, 2.0, 1)
        self.f64_bin_cmp(F64Lt, 2.0, 1.0, 0)
        self.f64_bin_cmp(F64Gt, 1.0, 2.0, 0)
        self.f64_bin_cmp(F64Gt, 2.0, 1.0, 1)
        self.f64_bin_cmp(F64Le, 1.0, 2.0, 1)
        self.f64_bin_cmp(F64Le, 2.0, 1.0, 0)
        self.f64_bin_cmp(F64Ge, 1.0, 2.0, 0)
        self.f64_bin_cmp(F64Ge, 2.0, 1.0, 1)

    def test_i32_arithmetic(self):
        self.i32_un_op(I32Clz, 0xF0, 24)
        self.i32_un_op(I32Ctz, 0xF0, 4)
        self.i32_un_op(I32PopCnt, 0xF0F0, 8)
        self.i32_bin_op(I32Add, 3, 2, 5)
        self.i32_bin_op(I32Sub, 3, 2, 1)
        self.i32_bin_op(I32Mul, 3, 2, 6)
        self.i32_bin_op(I32DivS, -8, 2, -4)
        self.i32_bin_op(I32DivU, -8, 2, 0x7FFF_FFFC)
        self.i32_bin_op(I32RemS, -5, 2, -1)
        self.i32_bin_op(I32RemU, -5, 2, 1)
        self.i32_bin_op(I32And, 0x0F0F, 0xF00F, 0x000F)
        self.i32_bin_op(I32Or, 0x0F0F, 0xF00F, 0xFF0F)
        self.i32_bin_op(I32Xor, 0x0F0F, 0xF00F, 0xFF00)
        self.i32_bin_op(I32Shl, -1, 8, -256)
        self.i32_bin_op(I32Shl, -1, 200, -256)
        self.i32_bin_op(I32ShrS, -1, 8, -1)
        self.i32_bin_op(I32ShrS, -1, 200, -1)
        self.i32_bin_op(I32ShrU, -1, 8, 0xFF_FFFF)
        self.i32_bin_op(I32ShrU, -1, 200, 0xFF_FFFF)
        self.i32_bin_op(I32Rotl, 0x1234_5678, 8, 0x3456_7812)
        self.i32_bin_op(I32Rotl, 0x1234_5678, 200, 0x3456_7812)
        self.i32_bin_op(I32Rotr, 0x1234_5678, 8, 0x7812_3456)
        self.i32_bin_op(I32Rotr, 0x1234_5678, 200, 0x7812_3456)

    def test_i64_arithmetic(self):
        self.i64_un_op(I64Clz, 0xF0, 56)
        self.i64_un_op(I64Ctz, 0xF0, 4)
        self.i64_un_op(I64PopCnt, 0xF0F0, 8)
        self.i64_bin_op(I64Add, 3, 2, 5)
        self.i64_bin_op(I64Sub, 3, 2, 1)
        self.i64_bin_op(I64Mul, 3, 2, 6)
        self.i64_bin_op(I64DivS, -8, 2, -4)
        self.i64_bin_op(I64DivU, -8, 2, 0x7FFF_FFFF_FFFF_FFFC)
        self.i64_bin_op(I64RemS, -5, 2, -1)
        self.i64_bin_op(I64RemU, -5, 2, 1)
        self.i64_bin_op(I64And, 0x0F0F, 0xF00F, 0x000F)
        self.i64_bin_op(I64Or, 0x0F0F, 0xF00F, 0xFF0F)
        self.i64_bin_op(I64Xor, 0x0F0F, 0xF00F, 0xFF00)
        self.i64_bin_op(I64Shl, -1, 8, -256)
        self.i64_bin_op(I64Shl, -1, 200, -256)
        self.i64_bin_op(I64ShrS, -1, 8, -1)
        self.i64_bin_op(I64ShrS, -1, 200, -1)
        self.i64_bin_op(I64ShrU, -1, 8, 0xFF_FFFF_FFFF_FFFF)
        self.i64_bin_op(I64ShrU, -1, 200, 0xFF_FFFF_FFFF_FFFF)
        self.i64_bin_op(I64Rotl, 0x1234_5678_1234_5678, 8, 0x3456_7812_3456_7812)
        self.i64_bin_op(I64Rotl, 0x1234_5678_1234_5678, 200, 0x3456_7812_3456_7812)
        self.i64_bin_op(I64Rotr, 0x1234_5678_1234_5678, 8, 0x7812_3456_7812_3456)
        self.i64_bin_op(I64Rotr, 0x1234_5678_1234_5678, 200, 0x7812_3456_7812_3456)

    def test_f32_arithmetic(self):
        self.f32_un_op(F32Abs, -1.5, 1.5)
        self.f32_un_op(F32Neg, 1.5, -1.5)
        self.f32_un_op(F32Ceil, 1.5, 2.0)
        self.f32_un_op(F32Floor, 1.5, 1.0)
        self.f32_un_op(F32Trunc, 1.5, 1.0)
        self.f32_un_op(F32Nearest, 0.5, 0.0)
        self.f32_un_op(F32Nearest, -0.5, 0.0)
        self.f32_un_op(F32Nearest, 1.1, 1.0)
        self.f32_un_op(F32Nearest, 1.5, 2.0)
        self.f32_un_op(F32Nearest, 1.9, 2.0)
        self.f32_un_op(F32Sqrt, 4.0, 2.0)
        self.f32_bin_op(F32Add, 3.0, 2.0, 5.0)
        self.f32_bin_op(F32Sub, 3.0, 2.0, 1.0)
        self.f32_bin_op(F32Mul, 3.0, 2.0, 6.0)
        self.f32_bin_op(F32Div, 3.0, 2.0, 1.5)
        self.f32_bin_op(F32Min, 3.0, 2.0, 2.0)
        self.f32_bin_op(F32Max, 3.0, 2.0, 3.0)
        self.f32_bin_op(F32CopySign, 3.0, 2.0, 3.0)
        self.f32_bin_op(F32CopySign, 3.0, -2.0, -3.0)

    def test_f64_arithmetic(self):
        self.f64_un_op(F64Abs, -1.5, 1.5)
        self.f64_un_op(F64Neg, 1.5, -1.5)
        self.f64_un_op(F64Ceil, 1.5, 2.0)
        self.f64_un_op(F64Floor, 1.5, 1.0)
        self.f64_un_op(F64Trunc, 1.5, 1.0)
        self.f64_un_op(F64Nearest, 0.5, 0.0)
        self.f64_un_op(F64Nearest, -0.5, 0.0)
        self.f64_un_op(F64Nearest, 1.1, 1.0)
        self.f64_un_op(F64Nearest, 1.5, 2.0)
        self.f64_un_op(F64Nearest, 1.9, 2.0)
        self.f64_un_op(F64Sqrt, 4.0, 2.0)
        self.f64_bin_op(F64Add, 3.0, 2.0, 5.0)
        self.f64_bin_op(F64Sub, 3.0, 2.0, 1.0)
        self.f64_bin_op(F64Mul, 3.0, 2.0, 6.0)
        self.f64_bin_op(F64Div, 3.0, 2.0, 1.5)
        self.f64_bin_op(F64Min, 3.0, 2.0, 2.0)
        self.f64_bin_op(F64Max, 3.0, 2.0, 3.0)
        self.f64_bin_op(F64CopySign, 3.0, 2.0, 3.0)
        self.f64_bin_op(F64CopySign, 3.0, -2.0, -3.0)

    def test_conversions(self):
        self.un_op(I32WrapI64, int64(0x7F7F_7F7F_7F7F_7F7F), int32(0x7F7F_7F7F))
        self.un_op(I32TruncF32S, float32(-1.5), int32(-1))
        self.un_op(I32TruncF32U, float32(1.5), int32(1))  # TODO
        self.un_op(I32TruncF64S, -1.5, int32(-1))
        self.un_op(I32TruncF64U, 1.5, int32(1))  # TODO
        self.un_op(I64ExtendI32S, int32(-1), int64(-1))
        self.un_op(I64ExtendI32U, int32(-1), int64(0xFFFF_FFFF))
        self.un_op(I64TruncF32S, float32(-1.5), int64(-1))
        self.un_op(I64TruncF32U, float32(1.5), int64(1))  # TODO
        self.un_op(I64TruncF64S, -1.5, int64(-1))
        self.un_op(I64TruncF64U, 1.5, int64(1))  # TODO
        self.un_op(F32ConvertI32S, int32(-1), float32(-1.0))
        self.un_op(F32ConvertI32U, int32(-1), float32(4.2949673e+09))
        self.un_op(F32ConvertI64S, int64(-1), float32(-1.0))
        self.un_op(F32ConvertI64U, int64(-1), float32(1.8446744e+19))
        self.un_op(F32DemoteF64, 1.5, float32(1.5))
        self.un_op(F64ConvertI32S, int32(-1), -1.0)
        self.un_op(F64ConvertI32U, int32(-1), 4.294967295e+09)
        self.un_op(F64ConvertI64S, int64(-1), -1.0)
        self.un_op(F64ConvertI64U, int64(-1), 1.8446744073709552e+19)
        self.un_op(F64PromoteF32, float32(1.5), 1.5)
        self.un_op(I32ReinterpretF32, float32(1.5), int32(0x3FC0_0000))
        self.un_op(I64ReinterpretF64, 1.5, int64(0x3FF8_0000_0000_0000))
        self.un_op(F32ReinterpretI32, int32(0x3FC0_0000), float32(1.5))
        self.un_op(F64ReinterpretI64, int64(0x3FF8_0000_0000_0000), 1.5)

    def i32_un_op(self, opcode, b, c):
        self.i32_bin_op(opcode, 0, int32(b), int32(c))

    def i64_un_op(self, opcode, b, c):
        self.i64_bin_op(opcode, 0, int64(b), int64(c))

    def f32_un_op(self, opcode, b, c):
        self.f32_bin_op(opcode, 0, float32(b), float32(c))

    def f64_un_op(self, opcode, b, c):
        self.f64_bin_op(opcode, 0, float64(b), float64(c))

    def i32_bin_op(self, opcode, a, b, c):
        self.bin_op(opcode, int32(a), int32(b), int32(c))

    def i64_bin_op(self, opcode, a, b, c):
        self.bin_op(opcode, int64(a), int64(b), int64(c))

    def f32_bin_cmp(self, opcode, a, b, c):
        self.bin_op(opcode, float32(a), float32(b), int32(c))

    def f64_bin_cmp(self, opcode, a, b, c):
        self.bin_op(opcode, float64(a), float64(b), int32(c))

    def f32_bin_op(self, opcode, a, b, c):
        self.bin_op(opcode, float32(a), float32(b), float32(c))

    def f64_bin_op(self, opcode, a, b, c):
        self.bin_op(opcode, float64(a), float64(b), float64(c))

    def un_op(self, opcode, b, c):
        self.bin_op(opcode, int32(0), b, c)

    def bin_op(self, opcode, a, b, c):
        vm = VM()
        push_val(vm, a)
        push_val(vm, b)
        instr_table[opcode](vm, None)
        self.assertEqual(c, pop_val(vm, c))


def push_val(vm, val):
    x = type(val)
    if x == int32:
        vm.push_s32(val)
    elif x in [int64, int]:
        vm.push_s64(val)
    elif x == float32:
        vm.push_f32(val)
    elif x in [float64, float]:
        vm.push_f64(val)
    else:
        raise Exception("wrong type: {}".format(val))


def pop_val(vm, value):
    type_info = type(value)
    if type_info == int32:
        return vm.pop_s32()
    elif type_info in [int64, int]:
        return vm.pop_s64()
    elif type_info == float32:
        return vm.pop_f32()
    elif type_info in [float64, float]:
        return vm.pop_f64()
    else:
        raise Exception("wrong type: {}".format(value))
