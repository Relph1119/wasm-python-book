#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: visitor_wast.py
@time: 2020/8/31 15:30
@project: wasm-python-book
@desc:
"""

from text.parser.WASTVisitor import WASTVisitor

class WastVisitor(WatVisitor, WASTVisitor):


def new_wast_visitor():
    return WastVisitor()
