#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: sig_parser.py
@time: 2020/8/23 19:59
@project: wasm-python-book
@desc:
"""
from ch10.binary.types import FuncType, ValTypeI32, ValTypeI64, ValTypeF32, ValTypeF64


def parse_name_and_sig(name_and_sig: str):
    idx_of_lpar = name_and_sig.find('(')
    name = name_and_sig[:idx_of_lpar]
    sig = name_and_sig[idx_of_lpar:]
    return name, parse_sig(sig)


def parse_sig(sig):
    params_and_results = sig.split('->')
    return FuncType(param_types=parse_val_types(params_and_results[0]),
                    result_types=parse_val_types(params_and_results[1]))


def parse_val_types(val_types_str: str):
    val_types_str = val_types_str.strip()
    # remove ()
    val_types_str = val_types_str[1:-1]
    val_types = []
    for t in val_types_str.split(','):
        t = t.strip()
        if t == 'i32':
            val_types.append(ValTypeI32)
        elif t == 'i64':
            val_types.append(ValTypeI64)
        elif t == 'f32':
            val_types.append(ValTypeF32)
        elif t == 'f64':
            val_types.append(ValTypeF64)

    return val_types
