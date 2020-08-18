#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: leb128_test.py
@time: 2020/8/18 22:28
@project: wasm-python-book
@desc: 测试LEB128解码
"""
import unittest

from binary.leb128 import decode_var_uint, decode_var_int


class TestLEB128Func(unittest.TestCase):

    def setUp(self):
        self.uint_data = [
            0b1_0111111,
            0b1_0011111,
            0b1_0001111,
            0b1_0000111,
            0b1_0000011,
            0b0_0000001]
        self.int_data = [0xC0, 0xBB, 0x78]

    def test_decode_var_uint(self):
        self.decode_var_uint32(self.uint_data[5:], 0b0000001, 1)
        self.decode_var_uint32(self.uint_data[4:], 0b1_0000011, 2)
        self.decode_var_uint32(self.uint_data[3:], 0b1_0000011_0000111, 3)
        self.decode_var_uint32(self.uint_data[2:], 0b1_0000011_0000111_0001111, 4)
        self.decode_var_uint32(self.uint_data[1:], 0b1_0000011_0000111_0001111_0011111, 5)

    def test_decode_var_int(self):
        self.decode_var_int32(self.int_data, -123456, 3)

    def decode_var_uint32(self, data, n, w):
        _n, _w = decode_var_uint(data, 32)
        self.assertEqual(n, _n)
        self.assertEqual(w, _w)

    def decode_var_int32(self, data, n, w):
        _n, _w = decode_var_int(data, 32)
        self.assertEqual(n, _n)
        self.assertEqual(w, _w)
