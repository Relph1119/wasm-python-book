#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: val.py
@time: 2020/8/23 17:06
@project: wasm-python-book
@desc: 参数和返回值的包装/解包
"""
import math
import struct

from binary.types import ValTypeI32, ValTypeI64, ValTypeF32, ValTypeF64
from interpreter import int32, int64, float32, float64, uint64, uint32


def wrap_u64(vt, val):
    if vt == ValTypeI32:
        return int32(val)
    elif vt == ValTypeI64:
        return int64(val)
    elif vt == ValTypeF32:
        cov_val = struct.unpack('>f', struct.pack('>l', int64(val)))[0]
        if math.isnan(cov_val):
            return float32(val)
        else:
            return float32(cov_val)
    elif vt == ValTypeF64:
        cov_val = struct.unpack('>d', struct.pack('>q', int64(val)))[0]
        if math.isnan(cov_val):
            return float64(val)
        else:
            return float64(cov_val)
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
