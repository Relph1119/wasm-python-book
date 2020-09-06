#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: wasm_impl.py
@time: 2020/9/6 10:14
@project: wasm-python-book
@desc:
"""
from binary import reader
from interpreter import vm
from validator import module_validator


class WasmImpl:

    @staticmethod
    def validate(module):
        return module_validator.validate(module)

    @staticmethod
    def instantiate(module, instances):
        return vm.new(module, instances)

    @staticmethod
    def instantiate_bin(data, instances):
        m, err = reader.decode(data)
        if err is not None:
            return None, err
        return vm.new(m, instances)
