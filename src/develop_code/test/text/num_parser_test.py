#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: num_parser_test.py
@time: 2020/9/1 19:19
@project: wasm-python-book
@desc:
"""
import math
import unittest

from interpreter import uint32, uint64, float32, float64
from text.num_parser import parse_f32


class TestNumParserFunc(unittest.TestCase):
    def test_nan(self):
        self.assertEqual(uint32(0x7fc00000), float32(str(math.nan)))
        self.assertEqual(uint32(0xffc00000), float32('-nan'))
        self.assertEqual(uint32(0x7f800000), float32(str(math.inf)))
        self.assertEqual(uint32(0xff800000), float32('-inf'))
        self.assertEqual(uint64(0x7ff8000000000001), float64(str(math.nan)))
        self.assertEqual(uint64(0xfff8000000000001), float64('-nan'))
        self.assertEqual(uint64(0x7ff0000000000000), float64(str(math.inf)))
        self.assertEqual(uint64(0xfff0000000000000), float64('-inf'))

    def test_parse_float(self):
        f1 = parse_f32("+0x1.00000100000000001p-50")
        f2 = parse_f32("+0x1.000002p-50")
        self.assertEqual(f1, f2)
