#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: __init__.py.py
@time: 2020/8/19 21:07
@project: wasm-python-book
@desc:
"""

import ctypes


class int8(int):
    def __new__(cls, val):
        val = ctypes.c_int8(val).value
        return super().__new__(cls, val)


class int16(int):
    def __new__(cls, val):
        val = ctypes.c_int16(val).value
        return super().__new__(cls, val)


class int32(int):
    def __new__(cls, val):
        val = ctypes.c_int32(val).value
        return super().__new__(cls, val)


class int64(int):
    def __new__(cls, val):
        val = ctypes.c_int64(val).value
        return super().__new__(cls, val)


class uint16(int):
    def __new__(cls, val):
        val = ctypes.c_uint16(val).value
        return super().__new__(cls, val)


class uint32(int):
    def __new__(cls, val):
        val = ctypes.c_uint32(val).value
        return super().__new__(cls, val)


class uint64(int):
    def __new__(cls, val):
        val = ctypes.c_uint64(val).value
        return super().__new__(cls, val)


class float32(float):
    def __new__(cls, val):
        val = ctypes.c_float(val).value
        return super().__new__(cls, val)


class float64(float):
    def __new__(cls, val):
        val = ctypes.c_double(val).value
        return super().__new__(cls, val)
