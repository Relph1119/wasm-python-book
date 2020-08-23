#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: native.py
@time: 2020/8/23 17:33
@project: wasm-python-book
@desc: 本地方法
"""
from ch09.interpreter import *


def print_char(args):
    print("%c" % int(args[0]), end='')
    return None


def assert_true(args):
    __assert_equal(int32(args[0]), int32(1))
    return None


def assert_false(args):
    __assert_equal(int32(args[0]), int32(0))
    return None


def assert_eq_i32(args):
    __assert_equal(int32(args[0]), int32(args[1]))
    return None


def assert_eq_i64(args):
    __assert_equal(int64(args[0]), int64(args[1]))
    return None


def assert_eq_f32(args):
    __assert_equal(float32(args[0]), float32(args[1]))
    return None


def assert_eq_f64(args):
    __assert_equal(float64(args[0]), float64(args[1]))
    return None


def __assert_equal(a, b):
    if a != b:
        raise Exception("{} != {}".format(a, b))
