#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: errors.py
@time: 2020/8/19 21:07
@project: wasm-python-book
@desc: 解释器Error异常
"""


class ErrTrap(Exception):
    def __str__(self):
        print("unreachable")


class ErrCallStackOverflow(Exception):
    def __str__(self):
        print("call stack exhausted")


class ErrTypeMismatch(Exception):
    def __str__(self):
        print("indirect call type mismatch")


class ErrUndefinedElem(Exception):
    def __str__(self):
        print("undefined element")


class ErrUninitializedElem(Exception):
    def __str__(self):
        print("uninitialized element")


class ErrMemOutOfBounds(Exception):
    def __str__(self):
        print("out of bounds memory access")


class ErrImmutableGlobal(Exception):
    def __str__(self):
        print("immutable global")


class ErrIntOverflow(Exception):
    def __str__(self):
        print("integer overflow")


class ErrConvertToInt(Exception):
    def __str__(self):
        print("invalid conversion to integer")
