#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: visitor_wat_names.py
@time: 2020/9/3 14:18
@project: wasm-python-book
@desc:
"""
from antlr4 import TerminalNode
from antlr4.tree import Tree

from text.error_reporter import ErrorReporter
from text.parser.WASTParser import WASTParser
from text.parser.WASTVisitor import WASTVisitor
from text.visitor_utils import get_text


class WatNamesVisitor(WASTVisitor, ErrorReporter):
    def __init__(self):
        super().__init__()
        self.module_builder = None

    def visitModuleField(self, ctx: WASTParser.ModuleFieldContext):
        def accept(val):
            if val is not None:
                return val.accept(self)

        imp = ctx.import_()
        accept(imp)
        f = ctx.func_()
        accept(f)
        m = ctx.memory()
        accept(m)
        g = ctx.global_()
        accept(g)
        return None

    def visitImport_(self, ctx: WASTParser.Import_Context):
        err = self.module_builder.ensure_no_non_imports()
        if err is not None:
            self.report_err(err, ctx.getChild(1))
        return ctx.importDesc().accept(self)

    def visitImportDesc(self, ctx: WASTParser.ImportDescContext):
        kind = ctx.kind.text
        name = get_text(ctx.NAME())
        err = self.module_builder.check_count(kind)
        if err is not None:
            self.report_err(err, ctx.parentCtx.getChild(1))
        err = self.module_builder.import_name(kind, name)
        if err is not None:
            self.report_err(err, ctx.NAME())
        return None

    def visitFunc_(self, ctx: WASTParser.Func_Context):
        return self.visit_module_field(ctx, "func", ctx.NAME(), ctx.embeddedIm())

    def visitTable(self, ctx: WASTParser.TableContext):
        return self.visit_module_field(ctx, "table", ctx.NAME(), ctx.embeddedIm())

    def visitMemory(self, ctx: WASTParser.MemoryContext):
        return self.visit_module_field(ctx, "memory", ctx.NAME(), ctx.embeddedIm())

    def visitGlobal(self, ctx: WASTParser.GlobalContext):
        return self.visit_module_field(ctx, "global", ctx.NAME(), ctx.embeddedIm())

    def visit_module_field(self, ctx: Tree, kind: str, name: TerminalNode, embeddedIm: WASTParser.EmbeddedImContext):
        err = self.module_builder.check_count(kind)
        if err is not None:
            self.report_err(err, ctx.getChild(1))

        if embeddedIm is not None:
            err = self.module_builder.ensure_no_non_imports()
            if err is not None:
                self.report_err(err, embeddedIm.getChild(1))
            err = self.module_builder.import_name(kind, get_text(name))
            if err is not None:
                self.report_err(err, name)
        else:
            err = self.module_builder.defind_name(kind, get_text(name))
            if err is not None:
                self.report_err(err, name)
        return None
