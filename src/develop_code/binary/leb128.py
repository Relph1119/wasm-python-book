#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: leb128.py
@time: 2020/8/18 22:02
@project: wasm-python-book
@desc: LEB128
Wasm二进制格式使用LEB1128来编码列表长度和索引等整数值
"""
from binary.errors import ErrIntTooLong, ErrIntTooLarge, ErrUnexpectedEnd


def encode_var_uint(val, size):
    buf = []
    while True:
        b = val & 0x7f
        val >>= 7
        if val != 0:
            b |= 0x80
        buf.append(b)
        if val == 0:
            break
    return buf


def decode_var_uint(data, size: int):
    """
    LEB128无符号整数解码
    :param data: 解码后的整数
    :param size: 实际消耗的字节数
    :return:
    """
    result = 0
    for i, b in enumerate(data):
        if i == int(size / 7):
            if b & 0x80 != 0:
                raise ErrIntTooLong
            if b >> (size - i * 7) > 0:
                raise ErrIntTooLarge
        result |= (b & 0x7f) << (i * 7)
        if b & 0x80 == 0:
            return result, i + 1
    raise ErrUnexpectedEnd


def encode_var_int(val, size):
    buf = []
    more = True
    while more:
        b = val & 0x7f
        val >>= 7
        if (val == 0 and 0x40 & b == 0) or \
                (val == -1 and (0x40 & b != 0)):
            more = False
        else:
            b |= 0x80
        buf.append(b)
    return buf


def decode_var_int(data, size):
    """
    LEB128有符号整数解码
    :param data: 解码后的整数
    :param size: 实际消耗的字节数
    :return:
    """
    result = 0
    for i, b in enumerate(data):
        if i == int(size / 7):
            if b & 0x80 != 0:
                raise ErrIntTooLong
            if b & 0x40 == 0 and b >> (size - i * 7 - 1) != 0 or \
                    b & 0x40 != 0 and int(b | 0x80) >> (size - i * 7 - 1) != -1:
                raise ErrIntTooLarge
        result |= (b & 0x7f) << (i * 7)
        if b & 0x80 == 0:
            if (i * 7 < size) and (b & 0x40 != 0):
                result |= -1 << ((i + 1) * 7)
            return result, i + 1
    raise ErrUnexpectedEnd
