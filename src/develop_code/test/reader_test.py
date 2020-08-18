#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: reader_test.py
@time: 2020/8/19 1:21
@project: wasm-python-book
@desc:
"""

import unittest

from binary.reader import WasmReader


class TestReaderFunc(unittest.TestCase):

    def setUp(self):
        data = [0x01,
                0x02, 0x03, 0x04, 0x05,
                0x00, 0x00, 0xc0, 0x3f,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xf8, 0x3f,
                0xE5, 0x8E, 0x26,  # https://en.wikipedia.org/wiki/LEB128#Unsigned_LEB128
                0xC0, 0xBB, 0x78,  # https://en.wikipedia.org/wiki/LEB128#Signed_LEB128
                0xC0, 0xBB, 0x78,
                0x03, 0x01, 0x02, 0x03,
                0x03, 0x66, 0x6f, 0x6f]
        reader = WasmReader(data)
        self.reader = reader

    def test_reads(self):
        self.assertEqual(0x01, self.reader.read_byte())
        self.assertEqual(int(0x05040302), self.reader.read_u32())
        self.assertEqual(float(1.5), self.reader.read_f32())
        self.assertEqual(1.5, self.reader.read_f64())
        self.assertEqual(624485, self.reader.read_var_u32())
        self.assertEqual(-123456, self.reader.read_var_s32())
        self.assertEqual(-123456, self.reader.read_var_s64())
        self.assertEqual(bytearray([0x01, 0x02, 0x03]), self.reader.read_bytes())
        self.assertEqual("foo", self.reader.read_name())
        self.assertEqual(0, self.reader.remaining())
