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
    n = len(s)
    data = []

    i = 0
    while i < n:
        if s[i] != '\\':
            data.append(ord(s[i]))
        else:
            if s[i+1] == 't':
                data.append('\t')
            elif s[i+1] == 'n':
                data.append('\n')
            elif s[i+1] == 'r':
                data.append('\r')
            elif s[i+1] == '""':
                data.append('""')
            elif s[i+1] == '\\':
                data.append('\\')
            elif s[i+1] == 'u':
                raise Exception("TODO")
            else:
                k = int(s[i+1:i+3], 16)
                data.append(k)
                i += 2
        i += 1
    return bytearray(data)
