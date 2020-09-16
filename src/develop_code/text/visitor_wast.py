#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: visitor_wast.py
@time: 2020/8/31 15:30
@project: wasm-python-book
@desc:
"""

from binary.opcodes import *
from interpreter import float32, float64
from text.builder_instr import new_instruction
from text.builder_script import new_script_builder
from text.parser.WASTParser import WASTParser
from text.parser.WASTVisitor import WASTVisitor
from text.str_escaper import escape
from text.visitor_utils import get_str, get_text, get_all_str
from text.visitor_wat import WatVisitor
from text.wast_script import Register, BinaryModule, QuotedModule, Action, ActionInvoke, ActionGet, Assertion, \
    AssertReturn, AssertTrap, AssertExhaustion, AssertMalformed, AssertInvalid, AssertUnlinkable


class WastVisitor(WatVisitor, WASTVisitor):
    def __init__(self):
        super().__init__()
        self.script_builder = None

    def visitScript(self, ctx: WASTParser.ScriptContext):
        self.script_builder = new_script_builder()
        for cmd in ctx.cmd():
            self.script_builder.add_cmd(cmd.accept(self))
        return self.script_builder.script

    def visitCmd(self, ctx: WASTParser.CmdContext):
        if ctx.wastModule() is not None:
            return ctx.wastModule().accept(self)
        elif ctx.action_() is not None:
            return ctx.action_().accept(self)
        elif ctx.assertion() is not None:
            return ctx.assertion().accept(self)
        elif ctx.meta() is not None:
            return ctx.meta().accept(self)
        else:
            register = Register()
            register.module_name = get_str(ctx.STRING())
            register.name = get_text(ctx.NAME())
            return register

    def visitWastModule(self, ctx: WASTParser.WastModuleContext):
        if ctx.watModule() is not None:
            return ctx.watModule().accept(self)

        name = get_text(ctx.NAME())
        kind_text = ctx.kind.text
        if kind_text == "binary":
            module = BinaryModule()
            module.name = name
            module.data = escape(get_all_str(ctx.STRING()))
            return module
        elif kind_text == "quote":
            module = QuotedModule()
            module.name = name
            module.text = get_all_str(ctx.STRING())
        else:
            raise Exception("unreachable")

    def visitAction_(self, ctx: WASTParser.Action_Context):
        a = Action()
        kind_text = ctx.kind.text
        if kind_text == "invoke":
            a.kind = ActionInvoke
        elif kind_text == "get":
            a.kind = ActionGet
        else:
            raise Exception("unreachable")

        a.module_name = get_text(ctx.NAME())
        a.item_name = get_str(ctx.STRING())
        if a.kind == ActionInvoke:
            if ctx.expr() is not None:
                a.expr = ctx.expr().accept(self)
            else:
                a.expr = []

        return a

    def visitAssertion(self, ctx: WASTParser.AssertionContext):
        a = Assertion()
        a.line = ctx.kind.line
        kind_text = ctx.kind.text
        if kind_text == "assert_return":
            a.kind = AssertReturn
        elif kind_text == "assert_trap":
            a.kind = AssertTrap
        elif kind_text == "assert_exhaustion":
            a.kind = AssertExhaustion
        elif kind_text == "assert_malformed":
            a.kind = AssertMalformed
        elif kind_text == "assert_invalid":
            a.kind = AssertInvalid
        elif kind_text == "assert_unlinkable":
            a.kind = AssertUnlinkable
        else:
            raise Exception("unreachable")

        if ctx.action_() is not None:
            a.action = ctx.action_().accept(self)

        for result in ctx.expected():
            a.result.append(result.accept(self))

        if ctx.wastModule() is not None:
            a.module = ctx.wastModule().accept(self)

        if ctx.STRING() is not None:
            a.failure = get_str(ctx.STRING())

        return a

    def visitExpected(self, ctx: WASTParser.ExpectedContext):
        if ctx.nan is not None:
            instr = new_instruction(ctx.op.text)
            opcode = instr.opcode
            if opcode == F32Const:
                instr.args = float32('nan')
            elif opcode == F64Const:
                instr.args = float64('nan')
            else:
                raise Exception("TODO:NAN")
            return instr
        return ctx.constInstr().accept(self)


def new_wast_visitor():
    return WastVisitor()
