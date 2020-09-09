#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: num_parser.py
@time: 2020/9/1 18:42
@project: wasm-python-book
@desc:
"""
import math

from interpreter import uint32, int32, int64, float32, float64


def parse_u32(s: str):
    base = 10
    s = s.replace("_", "")
    if s.find("0x") >= 0:
        base = 16
        s = s.replace("0x", "", 1)

    i = int(s, base)
    return uint32(i)


def parse_i32(s: str):
    return int32(parse_int(s, 32))


def parse_i64(s: str):
    return parse_int(s, 64)


def parse_int(s, bit_size):
    base = 10
    s = s.replace("_", "")
    if s.startswith("+"):
        s = s[1:]
    if s.find("0x") >= 0:
        s = s.replace("0x", "", 1)
        base = 16
    if s.startswith("-"):
        i = int(s, base)
    else:
        u = int(s, base)
        i = int64(u)
    return i


def parse_f32(s: str):
    if s.find("nan") >= 0:
        return parse_nan32(s)
    return float32(parse_float(s))


def parse_f64(s: str):
    if s.find("nan") >= 0:
        return parse_nan64(s)
    return parse_float(s)


def parse_float(s: str):
    s = s.replace("_", "")
    if s.find("0x") >= 0 > s.find('P') and s.find('p') < 0:
        s += "p0"
        return float.fromhex(s)
    elif s.find('P') > 0 or s.find('p') > 0:
        return float.fromhex(s)
    else:
        return float(s)


def parse_nan32(s: str):
    s = s.replace("_", "")
    f = float32('nan')
    if s[0] == '-':
        f = -f
        s = s[1:]
    elif s[0] == '+':
        s = s[1:]

    if s.startswith("nan:0x"):
        payload = int(s[6:], 16)
        bits = f & 0xFFBFFFFF
        f = float32(bits | payload)
    return f


def parse_nan64(s: str):
    s = s.replace("_", "")
    f = float64('nan')
    if s[0] == '-':
        f = -f
        s = s[1:]
    elif s[0] == '+':
        s = s[1:]
    if s.startswith("nan:0x"):
        payload = int(s[6:], 16)
        bits = f & 0xFFF7FFFFFFFFFFFE
        f = float32(bits | payload)
    else:
        bits = f & 0xFFF7FFFFFFFFFFFE
        f = float32(bits)
    return f
