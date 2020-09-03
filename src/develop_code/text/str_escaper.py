#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: str_escaper.py
@time: 2020/9/3 9:30
@project: wasm-python-book
@desc:
"""


def escape(s: str):
    s = s.encode('utf8')
    return bytearray(s)
