#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: compiler_test.py
@time: 2020/9/4 9:44
@project: wasm-python-book
@desc:
"""
import glob
import os
import unittest

from text.compiler import compile_module_file, compile_module_str


class TestCompilerFunc(unittest.TestCase):
    def test_compile_errors(self):
        files = glob.glob(os.path.join("../testdata", "err_*.wat"))
        for file in files:
            self.compile_err(file)

    def compile_err(self, file_name):
        with open(file_name, mode="rb") as f:
            test_wat = str(f.read(), encoding='utf8')
            sep = ";;------------------------------;;"
            if test_wat.find(sep) < 0:
                expected_err = get_expected_err(file_name, test_wat)
                _, err = compile_module_file(file_name)
                self.assertEqual(expected_err, err.error)
            else:
                for wat in test_wat.split(sep):
                    wat = wat.strip()
                    expected_err = get_expected_err("Obtained from string", wat)
                    _, err = compile_module_str(wat)
                    self.assertEqual(expected_err, err.error)


def get_expected_err(file_name, wat):
    start = wat.index("(;;") + 3
    end = wat.index(";;)")
    err = wat[start:end].strip()
    return err.replace("err.wat", file_name)
