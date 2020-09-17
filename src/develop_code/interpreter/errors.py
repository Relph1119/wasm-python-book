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
    def __init__(self):
        super().__init__("unreachable")


class ErrCallStackOverflow(Exception):
    def __init__(self):
        super().__init__("call stack exhausted")


class ErrTypeMismatch(Exception):
    def __init__(self):
        super().__init__("indirect call type mismatch")


class ErrUndefinedElem(Exception):
    def __init__(self):
        super().__init__("undefined element")


class ErrUninitializedElem(Exception):
    def __init__(self):
        super().__init__("uninitialized element")


class ErrMemOutOfBounds(Exception):
    def __init__(self):
        super().__init__("out of bounds memory access")


class ErrImmutableGlobal(Exception):
    def __init__(self):
        super().__init__("immutable global")


class ErrIntOverflow(Exception):
    def __init__(self):
        super().__init__("integer overflow")


class ErrConvertToInt(Exception):
    def __init__(self):
        super().__init__("invalid conversion to integer")


class ErrIntDivideByZero(Exception):
    def __init__(self):
        super().__init__("integer divide by zero")
