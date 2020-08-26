#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: sig_parser_test.py
@time: 2020/8/25 15:21
@project: wasm-python-book
@desc:
"""

import unittest

from instance.sig_parser import parse_name_and_sig


class TestSigParserFunc(unittest.TestCase):
    def test_sig_parser(self):
        self.sig_parser("(i32,f64)->(f32,i64)")
        self.sig_parser("(i32)->(f32,i64)")
        self.sig_parser("()->(f32)")
        self.sig_parser("(i32)->()")

    def sig_parser(self, name_and_sig):
        name, sig = parse_name_and_sig(name_and_sig)
        self.assertEqual(name_and_sig, name + sig.get_signature())
