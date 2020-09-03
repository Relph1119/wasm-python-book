#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: builder_script.py
@time: 2020/9/3 9:51
@project: wasm-python-book
@desc:
"""
from text.wast_script import Script


class ScriptBuilder:
    def __init__(self, script=None):
        self.script = script

    def add_cmd(self, cmd):
        self.script.cmds.append(cmd)


def new_script_builder():
    return ScriptBuilder(script=Script())
