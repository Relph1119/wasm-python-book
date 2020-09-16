#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: wast_script.py
@time: 2020/8/31 14:31
@project: wasm-python-book
@desc:
"""

ActionInvoke = 1
ActionGet = 2

AssertReturn = 1
AssertTrap = 2
AssertExhaustion = 3
AssertMalformed = 4
AssertInvalid = 5
AssertUnlinkable = 6


class Script:
    def __init__(self):
        self.cmds = []


class WatModule:
    def __init__(self):
        self.line = None
        self.name = ""
        self.module = None


class BinaryModule:
    def __init__(self):
        self.line = None
        self.name = ""
        self.data = []


class QuotedModule:
    def __init__(self):
        self.line = None
        self.name = ""
        self.text = ""


class Register:
    def __init__(self):
        self.module_name = ""
        self.name = ""


class Action:
    def __init__(self):
        self.kind = None
        self.module_name = ""
        self.item_name = ""
        self.expr = []


class Assertion:
    def __init__(self):
        self.line = None
        self.kind = None
        self.action = None
        self.result = []
        self.module = None
        self.failure = ""


class Meta:
    def __init__(self):
        pass
