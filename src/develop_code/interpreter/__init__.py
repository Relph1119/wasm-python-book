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


class uint8(int):
    def __new__(cls, val):
        val = ctypes.c_uint8(val).value
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
        if isinstance(val, str):
            if val.find('nan') >= 0:
                if val.startswith("-"):
                    val = 0xffc00000
                else:
                    val = 0x7fc00000
            elif val.find('inf') >= 0:
                if val.startswith("-"):
                    val = 0xff800000
                else:
                    val = 0x7f800000
            return val
        else:
            val = ctypes.c_float(val).value
            return super().__new__(cls, val)


class float64(float):
    def __new__(cls, val):
        if isinstance(val, str):
            if val.find('nan') >= 0:
                if val.startswith("-"):
                    val = 0xfff8000000000001
                else:
                    val = 0x7ff8000000000001
            elif val.find('inf') >= 0:
                if val.startswith("-"):
                    val = 0xfff0000000000000
                else:
                    val = 0x7ff0000000000000
            return val
        else:
            val = ctypes.c_double(val).value
            return super().__new__(cls, val)
