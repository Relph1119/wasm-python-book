#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: types_test.py
@time: 2020/8/19 8:23
@project: wasm-python-book
@desc:
"""
import unittest

from ch02.binary.types import FuncType, ValTypeI32, ValTypeI64, ValTypeF32, ValTypeF64


class TestTypesFunc(unittest.TestCase):
    def test_signature_param_types(self):
        ft = FuncType(param_types=[ValTypeI32, ValTypeI64, ValTypeF32, ValTypeF64],
                      result_types=None)
        self.assertEqual("(i32,i64,f32,f64)->()", ft.get_signature())

    def test_signature_result_types(self):
        ft = FuncType(param_types=None,
                      result_types=[ValTypeI64])
        self.assertEqual("()->(i64)", ft.get_signature())
