#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: leb128_test.py
@time: 2020/8/18 22:28
@project: wasm-python-book
@desc: 测试LEB128解码
"""
import random
import unittest

from binary.leb128 import decode_var_uint, decode_var_int, encode_var_uint, encode_var_int


class TestLEB128Func(unittest.TestCase):

    def test_var_uint(self):
        for i in range(100):
            val = random.randint(0, 1 << 64 - 1)
            data = encode_var_uint(val, 64)
            val2, n = decode_var_uint(data, 64)
            self.assertEqual(val, val2)
            self.assertEqual(len(data), n)

        for i in range(100):
            val = random.randint(0, 1 << 32 - 1)
            data = encode_var_uint(val, 32)
            val2, n = decode_var_uint(data, 32)
            self.assertEqual(val, val2)
            self.assertEqual(len(data), n)

    def test_var_int(self):
        for i in range(100):
            val = random.randint(- 1 << 63, 1 << 63 - 1)
            data = encode_var_int(val, 64)
            val2, n = decode_var_int(data, 64)
            self.assertEqual(val, val2)
            self.assertEqual(len(data), n)

        for i in range(100):
            val = random.randint(- 1 << 31, 1 << 31 - 1)
            data = encode_var_int(val, 32)
            val2, n = decode_var_int(data, 32)
            self.assertEqual(val, val2)
            self.assertEqual(len(data), n)

    def test_decode_var_uint(self):
        data = [
            0b1_0111111,
            0b1_0011111,
            0b1_0001111,
            0b1_0000111,
            0b1_0000011,
            0b0_0000001]
        self.decode_var_uint32(data[5:], 0b0000001, 1)
        self.decode_var_uint32(data[4:], 0b1_0000011, 2)
        self.decode_var_uint32(data[3:], 0b1_0000011_0000111, 3)
        self.decode_var_uint32(data[2:], 0b1_0000011_0000111_0001111, 4)
        self.decode_var_uint32(data[1:], 0b1_0000011_0000111_0001111_0011111, 5)

    def test_decode_var_int(self):
        self.decode_var_int32([0xC0, 0xBB, 0x78], -123456, 3)
        self.decode_var_int32([0x7F], -1, 1)
        self.decode_var_int32([0x7E], -2, 1)
        self.decode_var_int32([0x7D], -3, 1)
        self.decode_var_int32([0x7C], -4, 1)
        self.decode_var_int32([0x40], -64, 1)

    def decode_var_uint32(self, data, n, w):
        _n, _w = decode_var_uint(data, 32)
        self.assertEqual(n, _n)
        self.assertEqual(w, _w)

    def decode_var_int32(self, data, n, w):
        _n, _w = decode_var_int(data, 32)
        self.assertEqual(n, _n)
        self.assertEqual(w, _w)
