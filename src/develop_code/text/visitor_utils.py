#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: visitor_utils.py
@time: 2020/8/31 19:07
@project: wasm-python-book
@desc:
"""


def get_expr(node, visitor):
    if node is None:
        return []
    else:
        return node.accept(visitor)


def get_text(node):
    if node is None:
        return ""
    return node.getText()


def get_str(node):
    text = node.getText()
    return text[1: len(text) - 1]


def get_all_str(nodes):
    s = ""
    for node in nodes:
        s += get_str(node)
    return s
