#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: native.py
@time: 2020/8/23 17:33
@project: wasm-python-book
@desc: 本地方法
"""
from ch11.instance.native_module import NativeModule
from ch11.interpreter import *


def new_env():
    env = NativeModule()
    env.register_func("print_char(i32)->()", print_char)
    env.register_func("assert_true(i32)->()", assert_true)
    env.register_func("assert_false(i32)->()", assert_false)
    env.register_func("assert_eq_i32(i32,i32)->()", assert_eq_i32)
    env.register_func("assert_eq_i64(i64,i64)->()", assert_eq_i64)
    env.register_func("assert_eq_f32(f32,f32)->()", assert_eq_f32)
    env.register_func("assert_eq_f64(f64,f64)->()", assert_eq_f64)
    return env


def print_char(args):
    print("%c" % int(args[0]), end='')
    return None, None


def assert_true(args):
    __assert_equal(int32(args[0]), int32(1))
    return None, None


def assert_false(args):
    __assert_equal(int32(args[0]), int32(0))
    return None, None


def assert_eq_i32(args):
    __assert_equal(int32(args[0]), int32(args[1]))
    return None, None


def assert_eq_i64(args):
    __assert_equal(int64(args[0]), int64(args[1]))
    return None, None


def assert_eq_f32(args):
    __assert_equal(float32(args[0]), float32(args[1]))
    return None, None


def assert_eq_f64(args):
    __assert_equal(float64(args[0]), float64(args[1]))
    return None, None


def __assert_equal(a, b):
    if a != b:
        raise Exception("{} != {}".format(a, b))
