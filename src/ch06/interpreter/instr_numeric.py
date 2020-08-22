#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: instr_numeric.py
@time: 2020/8/19 21:54
@project: wasm-python-book
@desc: 数值指令
"""

# 常数指令
import math
from decimal import Decimal
from ch06.interpreter import int32, int64, float32, float64, uint32, uint64, int8, int16
from ch06.interpreter.errors import ErrIntOverflow, ErrConvertToInt

__MaxInt32 = 1 << 31 - 1
__MinInt32 = -1 << 31
__MaxInt64 = 1 << 63 - 1
__MinInt64 = -1 << 63
__MaxUint32 = 1 << 32 - 1
__MaxUint64 = 1 << 64 - 1


def i32_const(vm, args):
    vm.push_s32(int32(args))


def i64_const(vm, args):
    vm.push_s64(int64(args))


def f32_const(vm, args):
    vm.push_f32(float32(args))


def f64_const(vm, args):
    vm.push_f64(float64(args))


# i32 test & rel
def i32_eqz(vm, _):
    vm.push_bool(vm.pop_u32() == 0)


def i32_eq(vm, _):
    v2, v1 = vm.pop_u32(), vm.pop_u32()
    vm.push_bool(v1 == v2)


def i32_ne(vm, _):
    v2, v1 = vm.pop_u32(), vm.pop_u32()
    vm.push_bool(v1 != v2)


def i32_lt_s(vm, _):
    v2, v1 = vm.pop_s32(), vm.pop_s32()
    vm.push_bool(v1 < v2)


def i32_lt_u(vm, _):
    v2, v1 = vm.pop_u32(), vm.pop_u32()
    vm.push_bool(v1 < v2)


def i32_gt_s(vm, _):
    v2, v1 = vm.pop_s32(), vm.pop_s32()
    vm.push_bool(v1 > v2)


def i32_gt_u(vm, _):
    v2, v1 = vm.pop_u32(), vm.pop_u32()
    vm.push_bool(v1 > v2)


def i32_le_s(vm, _):
    v2, v1 = vm.pop_s32(), vm.pop_s32()
    vm.push_bool(v1 <= v2)


def i32_le_u(vm, _):
    v2, v1 = vm.pop_u32(), vm.pop_u32()
    vm.push_bool(v1 <= v2)


def i32_ge_s(vm, _):
    v2, v1 = vm.pop_s32(), vm.pop_s32()
    vm.push_bool(v1 >= v2)


def i32_ge_u(vm, _):
    v2, v1 = vm.pop_u32(), vm.pop_u32()
    vm.push_bool(v1 >= v2)


# i64 test & rel
def i64_eqz(vm, _):
    vm.push_bool(vm.pop_u64() == 0)


def i64_eq(vm, _):
    v2, v1 = vm.pop_u64(), vm.pop_u64()
    vm.push_bool(v1 == v2)


def i64_ne(vm, _):
    v2, v1 = vm.pop_u64(), vm.pop_u64()
    vm.push_bool(v1 != v2)


def i64_lt_s(vm, _):
    v2, v1 = vm.pop_s64(), vm.pop_s64()
    vm.push_bool(v1 < v2)


def i64_lt_u(vm, _):
    v2, v1 = vm.pop_u64(), vm.pop_u64()
    vm.push_bool(v1 < v2)


def i64_gt_s(vm, _):
    v2, v1 = vm.pop_s64(), vm.pop_s64()
    vm.push_bool(v1 > v2)


def i64_gt_u(vm, _):
    v2, v1 = vm.pop_u64(), vm.pop_u64()
    vm.push_bool(v1 > v2)


def i64_le_s(vm, _):
    v2, v1 = vm.pop_s64(), vm.pop_s64()
    vm.push_bool(v1 <= v2)


def i64_le_u(vm, _):
    v2, v1 = vm.pop_u64(), vm.pop_u64()
    vm.push_bool(v1 <= v2)


def i64_ge_s(vm, _):
    v2, v1 = vm.pop_s64(), vm.pop_s64()
    vm.push_bool(v1 >= v2)


def i64_ge_u(vm, _):
    v2, v1 = vm.pop_u64(), vm.pop_u64()
    vm.push_bool(v1 >= v2)


# f32 rel
def f32_eq(vm, _):
    v2, v1 = vm.pop_f32(), vm.pop_f32()
    vm.push_bool(v1 == v2)


def f32_ne(vm, _):
    v2, v1 = vm.pop_f32(), vm.pop_f32()
    vm.push_bool(v1 != v2)


def f32_lt(vm, _):
    v2, v1 = vm.pop_f32(), vm.pop_f32()
    vm.push_bool(v1 < v2)


def f32_gt(vm, _):
    v2, v1 = vm.pop_f32(), vm.pop_f32()
    vm.push_bool(v1 > v2)


def f32_le(vm, _):
    v2, v1 = vm.pop_f32(), vm.pop_f32()
    vm.push_bool(v1 <= v2)


def f32_ge(vm, _):
    v2, v1 = vm.pop_f32(), vm.pop_f32()
    vm.push_bool(v1 >= v2)


# f64 rel
def f64_eq(vm, _):
    v2, v1 = vm.pop_f64(), vm.pop_f64()
    vm.push_bool(v1 == v2)


def f64_ne(vm, _):
    v2, v1 = vm.pop_f64(), vm.pop_f64()
    vm.push_bool(v1 != v2)


def f64_lt(vm, _):
    v2, v1 = vm.pop_f64(), vm.pop_f64()
    vm.push_bool(v1 < v2)


def f64_gt(vm, _):
    v2, v1 = vm.pop_f64(), vm.pop_f64()
    vm.push_bool(v1 > v2)


def f64_le(vm, _):
    v2, v1 = vm.pop_f64(), vm.pop_f64()
    vm.push_bool(v1 <= v2)


def f64_ge(vm, _):
    v2, v1 = vm.pop_f64(), vm.pop_f64()
    vm.push_bool(v1 >= v2)


__len8tab = [
    0x00, 0x01, 0x02, 0x02, 0x03, 0x03, 0x03, 0x03, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04,
    0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05,
    0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06,
    0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06,
    0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07,
    0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07,
    0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07,
    0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07,
    0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08,
    0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08,
    0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08,
    0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08,
    0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08,
    0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08,
    0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08,
    0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08,
]

__pop8tab = [
    0x00, 0x01, 0x01, 0x02, 0x01, 0x02, 0x02, 0x03, 0x01, 0x02, 0x02, 0x03, 0x02, 0x03, 0x03, 0x04,
    0x01, 0x02, 0x02, 0x03, 0x02, 0x03, 0x03, 0x04, 0x02, 0x03, 0x03, 0x04, 0x03, 0x04, 0x04, 0x05,
    0x01, 0x02, 0x02, 0x03, 0x02, 0x03, 0x03, 0x04, 0x02, 0x03, 0x03, 0x04, 0x03, 0x04, 0x04, 0x05,
    0x02, 0x03, 0x03, 0x04, 0x03, 0x04, 0x04, 0x05, 0x03, 0x04, 0x04, 0x05, 0x04, 0x05, 0x05, 0x06,
    0x01, 0x02, 0x02, 0x03, 0x02, 0x03, 0x03, 0x04, 0x02, 0x03, 0x03, 0x04, 0x03, 0x04, 0x04, 0x05,
    0x02, 0x03, 0x03, 0x04, 0x03, 0x04, 0x04, 0x05, 0x03, 0x04, 0x04, 0x05, 0x04, 0x05, 0x05, 0x06,
    0x02, 0x03, 0x03, 0x04, 0x03, 0x04, 0x04, 0x05, 0x03, 0x04, 0x04, 0x05, 0x04, 0x05, 0x05, 0x06,
    0x03, 0x04, 0x04, 0x05, 0x04, 0x05, 0x05, 0x06, 0x04, 0x05, 0x05, 0x06, 0x05, 0x06, 0x06, 0x07,
    0x01, 0x02, 0x02, 0x03, 0x02, 0x03, 0x03, 0x04, 0x02, 0x03, 0x03, 0x04, 0x03, 0x04, 0x04, 0x05,
    0x02, 0x03, 0x03, 0x04, 0x03, 0x04, 0x04, 0x05, 0x03, 0x04, 0x04, 0x05, 0x04, 0x05, 0x05, 0x06,
    0x02, 0x03, 0x03, 0x04, 0x03, 0x04, 0x04, 0x05, 0x03, 0x04, 0x04, 0x05, 0x04, 0x05, 0x05, 0x06,
    0x03, 0x04, 0x04, 0x05, 0x04, 0x05, 0x05, 0x06, 0x04, 0x05, 0x05, 0x06, 0x05, 0x06, 0x06, 0x07,
    0x02, 0x03, 0x03, 0x04, 0x03, 0x04, 0x04, 0x05, 0x03, 0x04, 0x04, 0x05, 0x04, 0x05, 0x05, 0x06,
    0x03, 0x04, 0x04, 0x05, 0x04, 0x05, 0x05, 0x06, 0x04, 0x05, 0x05, 0x06, 0x05, 0x06, 0x06, 0x07,
    0x03, 0x04, 0x04, 0x05, 0x04, 0x05, 0x05, 0x06, 0x04, 0x05, 0x05, 0x06, 0x05, 0x06, 0x06, 0x07,
    0x04, 0x05, 0x05, 0x06, 0x05, 0x06, 0x06, 0x07, 0x05, 0x06, 0x06, 0x07, 0x06, 0x07, 0x07, 0x08,
]


def __leading_zeros32(x):
    def len32(k):
        n = 0
        if k >= 1 << 16:
            k >>= 16
            n = 16
        if k >= 1 << 8:
            k >>= 8
            n += 8
        return n + int(__len8tab[k])

    return 32 - len32(x)


def __trailing_zeros32(x):
    de_bruijn32 = 0x077CB531

    de_bruijn32tab = [
        0, 1, 28, 2, 29, 14, 24, 3, 30, 22, 20, 15, 25, 17, 4, 8,
        31, 27, 13, 23, 21, 19, 16, 7, 26, 12, 18, 6, 11, 5, 10, 9,
    ]

    if x == 0:
        return 32
    return int(de_bruijn32tab[(x & -x) * de_bruijn32 >> (32 - 5)])


def __ones_count32(x):
    return int(__pop8tab[x >> 24] + __pop8tab[x >> 16 & 0xff]
               + __pop8tab[x >> 8 & 0xff] + __pop8tab[x & 0xff])


def __rotate_left32(x, k):
    n = 32
    s = k & (n - 1)
    return x << s | x >> (n - s)


# i32 arithmetic & bitwise
def i32_clz(vm, _):
    """统计前置0比特数"""
    vm.push_u32(uint32(__leading_zeros32(vm.pop_u32())))


def i32_ctz(vm, _):
    """统计后置0比特数"""
    vm.push_u32(uint32(__trailing_zeros32(vm.pop_u32())))


def i32_pop_cnt(vm, _):
    """统计1比特数"""
    vm.push_u32(uint32(__ones_count32(vm.pop_u32())))


def i32_add(vm, _):
    v2, v1 = vm.pop_u32(), vm.pop_u32()
    vm.push_u32(v1 + v2)


def i32_sub(vm, _):
    v2, v1 = vm.pop_u32(), vm.pop_u32()
    vm.push_u32(v1 - v2)


def i32_mul(vm, _):
    v2, v1 = vm.pop_u32(), vm.pop_u32()
    vm.push_u32(v1 * v2)


def i32_div_s(vm, _):
    v2, v1 = vm.pop_s32(), vm.pop_s32()
    if v1 == __MinInt32 and v2 == -1:
        raise ErrIntOverflow
    vm.push_s32(int(v1 / v2))


def i32_div_u(vm, _):
    v2, v1 = vm.pop_u32(), vm.pop_u32()
    vm.push_u32(int(v1 / v2))


def i32_rem_s(vm, _):
    v2, v1 = vm.pop_s32(), vm.pop_s32()
    vm.push_s32(int(math.fmod(v1, v2)))


def i32_rem_u(vm, _):
    v2, v1 = vm.pop_u32(), vm.pop_u32()
    vm.push_u32(int(math.fmod(v1, v2)))


def i32_and(vm, _):
    v2, v1 = vm.pop_u32(), vm.pop_u32()
    vm.push_u32(v1 & v2)


def i32_or(vm, _):
    v2, v1 = vm.pop_u32(), vm.pop_u32()
    vm.push_u32(v1 | v2)


def i32_xor(vm, _):
    v2, v1 = vm.pop_u32(), vm.pop_u32()
    vm.push_u32(v1 ^ v2)


def i32_shl(vm, _):
    v2, v1 = vm.pop_u32(), vm.pop_u32()
    vm.push_u32(v1 << (v2 % 32))


def i32_shr_s(vm, _):
    v2, v1 = vm.pop_u32(), vm.pop_s32()
    vm.push_s32(v1 >> (v2 % 32))


def i32_shr_u(vm, _):
    v2, v1 = vm.pop_u32(), vm.pop_u32()
    vm.push_u32(v1 >> (v2 % 32))


def i32_rotl(vm, _):
    v2, v1 = vm.pop_u32(), vm.pop_u32()
    vm.push_u32(__rotate_left32(v1, int(v2)))


def i32_rotr(vm, _):
    v2, v1 = vm.pop_u32(), vm.pop_u32()
    vm.push_u32(__rotate_left32(v1, -int(v2)))


def __leading_zeros64(x):
    def len64(k):
        n = 0
        if k >= 1 << 32:
            k >>= 32
            n = 32
        if k >= 1 << 16:
            k >>= 16
            n += 16
        if k >= 1 << 8:
            k >>= 8
            n += 8
        return n + int(__len8tab[k])

    return 64 - len64(x)


def __trailing_zeros64(x):
    de_bruijn64 = 0x03f79d71b4ca8b09

    de_bruijn64tab = [
        0, 1, 56, 2, 57, 49, 28, 3, 61, 58, 42, 50, 38, 29, 17, 4,
        62, 47, 59, 36, 45, 43, 51, 22, 53, 39, 33, 30, 24, 18, 12, 5,
        63, 55, 48, 27, 60, 41, 37, 16, 46, 35, 44, 21, 52, 32, 23, 11,
        54, 26, 40, 15, 34, 20, 31, 10, 25, 14, 19, 9, 13, 8, 7, 6,
    ]

    if x == 0:
        return 64
    return int(de_bruijn64tab[(x & -x) * de_bruijn64 >> (64 - 6)])


def __ones_count64(x):
    bin_n = bin(x)
    num = str(bin_n).count('1')
    return num


def __rotate_left64(x, k):
    n = 64
    s = k & (n - 1)
    return x << s | x >> (n - s)


# i64 arithmetic & bitwise
def i64_clz(vm, _):
    vm.push_u64(uint64(__leading_zeros64(vm.pop_u64())))


def i64_ctz(vm, _):
    vm.push_u64(uint64(__trailing_zeros64(vm.pop_u64())))


def i64_pop_cnt(vm, _):
    vm.push_u64(uint64(__ones_count64(vm.pop_u64())))


def i64_add(vm, _):
    v2, v1 = vm.pop_u64(), vm.pop_u64()
    vm.push_u64(v1 + v2)


def i64_sub(vm, _):
    v2, v1 = vm.pop_u64(), vm.pop_u64()
    vm.push_u64(v1 - v2)


def i64_mul(vm, _):
    v2, v1 = vm.pop_u64(), vm.pop_u64()
    vm.push_u64(int(Decimal(v1) * v2))


def i64_div_s(vm, _):
    v2, v1 = vm.pop_s64(), vm.pop_s64()
    if v1 == __MinInt64 and v2 == -1:
        raise ErrIntOverflow
    vm.push_s64(int(Decimal(v1) / v2))


def i64_div_u(vm, _):
    v2, v1 = vm.pop_u64(), vm.pop_u64()
    vm.push_u64(int(Decimal(v1) / v2))


def i64_rem_s(vm, _):
    v2, v1 = vm.pop_s64(), vm.pop_s64()
    vm.push_s64(int(math.fmod(v1, v2)))


def i64_rem_u(vm, _):
    v2, v1 = vm.pop_u64(), vm.pop_u64()
    vm.push_u64(v1 % v2)


def i64_and(vm, _):
    v2, v1 = vm.pop_u64(), vm.pop_u64()
    vm.push_u64(v1 & v2)


def i64_or(vm, _):
    v2, v1 = vm.pop_u64(), vm.pop_u64()
    vm.push_u64(v1 | v2)


def i64_xor(vm, _):
    v2, v1 = vm.pop_u64(), vm.pop_u64()
    vm.push_u64(v1 ^ v2)


def i64_shl(vm, _):
    v2, v1 = vm.pop_u64(), vm.pop_u64()
    vm.push_u64(v1 << (v2 % 64))


def i64_shr_s(vm, _):
    v2, v1 = vm.pop_u64(), vm.pop_s64()
    vm.push_s64(v1 >> (v2 & 64))


def i64_shr_u(vm, _):
    v2, v1 = vm.pop_u64(), vm.pop_u64()
    vm.push_u64(v1 >> (v2 % 64))


def i64_rotl(vm, _):
    v2, v1 = vm.pop_u64(), vm.pop_u64()
    vm.push_u64(__rotate_left64(v1, int(v2)))


def i64_rotr(vm, _):
    v2, v1 = vm.pop_u64(), vm.pop_u64()
    vm.push_u64(__rotate_left64(v1, -int(v2)))


# f32 arithmetic
def f32_abs(vm, _):
    vm.push_f32(abs(vm.pop_f32()))


def f32_neg(vm, _):
    vm.push_f32(-vm.pop_f32())


def f32_ceil(vm, _):
    vm.push_f32(math.ceil(vm.pop_f32()))


def f32_floor(vm, _):
    vm.push_f32(math.floor(vm.pop_f32()))


def f32_trunc(vm, _):
    vm.push_f32(math.trunc(vm.pop_f32()))


def f32_nearest(vm, _):
    vm.push_f32(round(vm.pop_f32()))


def f32_sqrt(vm, _):
    vm.push_f32(math.sqrt(vm.pop_f32()))


def f32_add(vm, _):
    v2, v1 = vm.pop_f32(), vm.pop_f32()
    vm.push_f32(v1 + v2)


def f32_sub(vm, _):
    v2, v1 = vm.pop_f32(), vm.pop_f32()
    vm.push_f32(v1 - v2)


def f32_mul(vm, _):
    v2, v1 = vm.pop_f32(), vm.pop_f32()
    vm.push_f32(v1 * v2)


def f32_div(vm, _):
    v2, v1 = vm.pop_f32(), vm.pop_f32()
    vm.push_f32(v1 / v2)


def f32_min(vm, _):
    v2, v1 = vm.pop_f32(), vm.pop_f32()
    v1_nan = math.isnan(v1)
    v2_nan = math.isnan(v2)
    if v1_nan and not v2_nan:
        vm.push_f32(v1)
    elif v2_nan and not v1_nan:
        vm.push_f32(v2)
    else:
        vm.push_f32(min(v1, v2))


def f32_max(vm, _):
    v2, v1 = vm.pop_f32(), vm.pop_f32()
    v1_nan = math.isnan(v1)
    v2_nan = math.isnan(v2)
    if v1_nan and not v2_nan:
        vm.push_f32(v1)
    elif v2_nan and not v1_nan:
        vm.push_f32(v2)
    else:
        vm.push_f32(max(v1, v2))


def f32_copysign(vm, _):
    v2, v1 = vm.pop_f32(), vm.pop_f32()
    vm.push_f32(math.copysign(v1, v2))


# f64 arithmetic
def f64_abs(vm, _):
    vm.push_f64(abs(vm.pop_f64()))


def f64_neg(vm, _):
    vm.push_f64(-vm.pop_f64())


def f64_ceil(vm, _):
    vm.push_f64(math.ceil(vm.pop_f64()))


def f64_floor(vm, _):
    vm.push_f64(math.floor(vm.pop_f64()))


def f64_trunc(vm, _):
    vm.push_f64(math.trunc(vm.pop_f64()))


def f64_nearest(vm, _):
    vm.push_f64(round(vm.pop_f64()))


def f64_sqrt(vm, _):
    vm.push_f64(math.sqrt(vm.pop_f64()))


def f64_add(vm, _):
    v2, v1 = vm.pop_f64(), vm.pop_f64()
    vm.push_f64(v1 + v2)


def f64_sub(vm, _):
    v2, v1 = vm.pop_f64(), vm.pop_f64()
    vm.push_f64(v1 - v2)


def f64_mul(vm, _):
    v2, v1 = vm.pop_f64(), vm.pop_f64()
    vm.push_f64(v1 * v2)


def f64_div(vm, _):
    v2, v1 = vm.pop_f64(), vm.pop_f64()
    vm.push_f64(v1 / v2)


def f64_min(vm, _):
    v2, v1 = vm.pop_f64(), vm.pop_f64()
    v1_nan = math.isnan(v1)
    v2_nan = math.isnan(v2)
    if v1_nan and not v2_nan:
        vm.push_f64(v1)
    elif v2_nan and not v1_nan:
        vm.push_f64(v2)
    else:
        vm.push_f64(min(v1, v2))


def f64_max(vm, _):
    v2, v1 = vm.pop_f64(), vm.pop_f64()
    v1_nan = math.isnan(v1)
    v2_nan = math.isnan(v2)
    if v1_nan and not v2_nan:
        vm.push_f64(v1)
    elif v2_nan and not v1_nan:
        vm.push_f64(v2)
    else:
        vm.push_f64(max(v1, v2))


def f64_copysign(vm, _):
    v2, v1 = vm.pop_f64(), vm.pop_f64()
    vm.push_f64(math.copysign(v1, v2))


# conversions
def i32_wrap_i64(vm, _):
    vm.push_u32(uint32(vm.pop_u64()))


def i32_trunc_f32s(vm, _):
    f = math.trunc(vm.pop_f32())
    if f > __MaxInt32 or f < __MinInt32:
        raise ErrIntOverflow
    if math.isnan(f):
        raise ErrConvertToInt
    vm.push_u32(int32(f))


def i32_trunc_f32u(vm, _):
    f = math.trunc(vm.pop_f32())
    if f > __MaxUint32 or f < 0:
        raise ErrIntOverflow
    if math.isnan(f):
        raise ErrConvertToInt
    vm.push_u32(uint32(f))


def i32_trunc_f64s(vm, _):
    f = math.trunc(vm.pop_f64())
    if f > __MaxInt32 or f < __MinInt32:
        raise ErrIntOverflow
    if math.isnan(f):
        raise ErrConvertToInt
    vm.push_s32(int32(f))


def i32_trunc_f64u(vm, _):
    f = math.trunc(vm.pop_f64())
    if f > __MaxUint32 or f < 0:
        raise ErrIntOverflow
    if math.isnan(f):
        raise ErrConvertToInt
    vm.push_u32(uint32(f))


def i64_extend_i32s(vm, _):
    vm.push_s64(int64(vm.pop_s32()))


def i64_extend_i32u(vm, _):
    vm.push_u64(uint64(vm.pop_u32()))


def i64_trunc_f32s(vm, _):
    f = math.trunc(vm.pop_f32())
    if f >= __MaxInt64 or f < __MinInt64:
        raise ErrIntOverflow
    if math.isnan(f):
        raise ErrConvertToInt
    vm.push_s64(int64(f))


def i64_trunc_f32u(vm, _):
    f = math.trunc(vm.pop_f32())
    if f >= __MaxUint64 or f < 0:
        raise ErrIntOverflow
    if math.isnan(f):
        raise ErrConvertToInt
    vm.push_u64(uint64(f))


def i64_trunc_f64s(vm, _):
    f = math.trunc(vm.pop_f64())
    if f >= __MaxInt64 or f < __MinInt64:
        raise ErrIntOverflow
    if math.isnan(f):
        raise ErrConvertToInt
    vm.push_s64(int64(f))


def i64_trunc_f64u(vm, _):
    f = math.trunc(vm.pop_f64())
    if f >= __MaxUint64 or f < 0:
        raise ErrIntOverflow
    if math.isnan(f):
        raise ErrConvertToInt
    vm.push_u64(uint64(f))


def f32_convert_i32s(vm, _):
    vm.push_f32(float32(vm.pop_s32()))


def f32_convert_i32u(vm, _):
    vm.push_f32(float32(vm.pop_u32()))


def f32_convert_i64s(vm, _):
    vm.push_f32(float32(vm.pop_s64()))


def f32_convert_i64u(vm, _):
    vm.push_f32(float32(vm.pop_u64()))


def f32_demote_f64(vm, _):
    vm.push_f32(float32(vm.pop_f64()))


def f64_convert_i32s(vm, _):
    vm.push_f64(float64(vm.pop_s32()))


def f64_convert_i32u(vm, _):
    vm.push_f64(float64(vm.pop_u32()))


def f64_convert_i64s(vm, _):
    vm.push_f64(float64(vm.pop_s64()))


def f64_convert_i64u(vm, _):
    vm.push_f64(float64(vm.pop_u64()))


def f64_promote_f32(vm, _):
    vm.push_f64(float64(vm.pop_f32()))


def i32_reinterpret_f32(vm, _):
    pass


def i64_reinterpret_f64(vm, _):
    pass


def f32_reinterpret_i32(vm, _):
    pass


def f64_reinterpret_i64(vm, _):
    pass


def i32_extend_8s(vm, _):
    vm.push_s32(int32(int8(vm.pop_s32())))


def i32_extend_16s(vm, _):
    vm.push_s32(int32(int16(vm.pop_s32())))


def i64_extend_8s(vm, _):
    vm.push_s64(int64(int8(vm.pop_s64())))


def i64_extend_16s(vm, _):
    vm.push_s64(int64(int16(vm.pop_s64())))


def i64_extend_32s(vm, _):
    vm.push_s64(int64(int32(vm.pop_s64())))


def trunc_sat(vm, args):
    if args == 0:  # i32.trunc_sat_f32_s
        v = __trunc_sat_s(vm.pop_f32(), 32)
        vm.push_s32(int32(v))
    elif args == 1:  # i32.trunc_sat_f32_u
        v = __trunc_sat_u(vm.pop_f32(), 32)
        vm.push_u32(uint32(v))
    elif args == 2:  # i32.trunc_sat_f64_s
        v = __trunc_sat_s(vm.pop_f64(), 32)
        vm.push_s32(int32(v))
    elif args == 3:  # i32.trunc_sat_f64_u
        v = __trunc_sat_u(vm.pop_f64(), 32)
        vm.push_u32(uint32(v))
    elif args == 4:  # i64.trunc_sat_f32_s
        v = __trunc_sat_s(vm.pop_f32(), 64)
        vm.push_s64(v)
    elif args == 5:  # i64.trunc_sat_f32_u
        v = __trunc_sat_u(vm.pop_f32(), 64)
        vm.push_u64(v)
    elif args == 6:  # i64.trunc_sat_f64_s
        v = __trunc_sat_s(vm.pop_f64(), 64)
        vm.push_s64(v)
    elif args == 7:  # i64.trunc_sat_f64_u
        v = __trunc_sat_u(vm.pop_f64(), 64)
        vm.push_u64(v)
    else:
        raise Exception("unreachable")


def __trunc_sat_u(z, n):
    if math.isnan(z):
        return 0
    if z == -math.inf:
        return 0
    max_value = (uint64(1) << n) - 1
    if math.isinf(z):
        return max_value
    x = math.trunc(z)
    if x < 0:
        return 0
    elif x >= float64(max_value):
        return max_value
    else:
        return uint64(x)


def __trunc_sat_s(z, n):
    if math.isnan(z):
        return 0
    min_value = -(int64(1) << (n - 1))
    max_value = (int64(1) << (n - 1)) - 1
    if z == -math.inf:
        return min_value
    if math.isinf(z):
        return max_value
    x = math.trunc(z)
    if x < float64(min_value):
        return min_value
    elif x >= float64(max_value):
        return max_value
    else:
        return int64(x)
