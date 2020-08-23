#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: val.py
@time: 2020/8/23 17:06
@project: wasm-python-book
@desc: 参数和返回值的包装/解包
"""
from binary.types import ValTypeI32, ValTypeI64, ValTypeF32, ValTypeF64
from interpreter import int32, int64, float32, float64, uint64


def warp_u64(vt, val):
    if vt == ValTypeI32:
        return int32(val)
    elif vt == ValTypeI64:
        return int64(val)
    elif vt == ValTypeF32:
        return float32(val)
    elif vt == ValTypeF64:
        return float64(val)
    else:
        raise Exception("unreachable")


def unwrap_u64(vt, val):
    if vt == ValTypeI32:
        return uint64(val)
    elif vt == ValTypeI64:
        return uint64(val)
    elif vt == ValTypeF32:
        return uint64(val)
    elif vt == ValTypeF64:
        return uint64(val)
    else:
        raise Exception("unreachable")
