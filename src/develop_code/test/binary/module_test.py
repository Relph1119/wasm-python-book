#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: module_test.py
@time: 2020/8/19 8:45
@project: wasm-python-book
@desc:
"""

import unittest
import binary
from binary.module import MagicNumber, Version


class TestDecode(unittest.TestCase):
    def test_decode(self):
        module, err = binary.decode_file("../testdata/hw_rust.wasm")
        self.assertIsNone(err)
        self.assertEqual(MagicNumber, module.magic)
        self.assertEqual(Version, module.version)
        self.assertEqual(2, len(module.custom_secs))
        self.assertEqual(15, len(module.type_sec))
        self.assertEqual(0, len(module.import_sec))
        self.assertEqual(171, len(module.func_sec))
        self.assertEqual(1, len(module.table_sec))
        self.assertEqual(1, len(module.mem_sec))
        self.assertEqual(4, len(module.global_sec))
        self.assertEqual(5, len(module.export_sec))
        self.assertIsNone(module.start_sec)
        self.assertEqual(1, len(module.elem_sec))
        self.assertEqual(171, len(module.code_sec))
        self.assertEqual(4, len(module.data_sec))
