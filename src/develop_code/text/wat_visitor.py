#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: wat_visitor.py
@time: 2020/8/31 18:25
@project: wasm-python-book
@desc:
"""
from text.error_reporter import ErrorReporter
from text.parser.WASTParser import WASTParser
from text.parser.WASTVisitor import WASTVisitor
from text.visitor_utils import get_text


class WatVisitor(WASTVisitor, ErrorReporter):
    def __init__(self):
        super().__init__()
        self.module_builder = None
        self.code_builder = None

    def visitModule(self, ctx: WASTParser.ModuleContext):
        return ctx.watModule().accept(self).module

    def visitWatModule(self, ctx: WASTParser.WatModuleContext):
        name = get_text(ctx.NAME())
        self.module_builder = new_module_builder()



    def visitModuleField(self, ctx: WASTParser.ModuleFieldContext):
        return super().visitModuleField(ctx)

    def visitTypeDef(self, ctx: WASTParser.TypeDefContext):
        return super().visitTypeDef(ctx)

    def visitImport_(self, ctx: WASTParser.Import_Context):
        return super().visitImport_(ctx)

    def visitImportDesc(self, ctx: WASTParser.ImportDescContext):
        return super().visitImportDesc(ctx)

    def visitFunc_(self, ctx: WASTParser.Func_Context):
        return super().visitFunc_(ctx)

    def visitFuncLocal(self, ctx: WASTParser.FuncLocalContext):
        return super().visitFuncLocal(ctx)

    def visitTable(self, ctx: WASTParser.TableContext):
        return super().visitTable(ctx)

    def visitMemory(self, ctx: WASTParser.MemoryContext):
        return super().visitMemory(ctx)

    def visitGlobal(self, ctx: WASTParser.GlobalContext):
        return super().visitGlobal(ctx)

    def visitExport(self, ctx: WASTParser.ExportContext):
        return super().visitExport(ctx)

    def visitExportDesc(self, ctx: WASTParser.ExportDescContext):
        return super().visitExportDesc(ctx)

    def visitStart(self, ctx: WASTParser.StartContext):
        return super().visitStart(ctx)

    def visitElem(self, ctx: WASTParser.ElemContext):
        return super().visitElem(ctx)

    def visitData(self, ctx: WASTParser.DataContext):
        return super().visitData(ctx)

    def visitEmbeddedIm(self, ctx: WASTParser.EmbeddedImContext):
        return super().visitEmbeddedIm(ctx)

    def visitEmbeddedEx(self, ctx: WASTParser.EmbeddedExContext):
        return super().visitEmbeddedEx(ctx)

    def visitTypeUse(self, ctx: WASTParser.TypeUseContext):
        return super().visitTypeUse(ctx)

    def visitFuncVars(self, ctx: WASTParser.FuncVarsContext):
        return super().visitFuncVars(ctx)

    def visitValType(self, ctx: WASTParser.ValTypeContext):
        return super().visitValType(ctx)

    def visitBlockType(self, ctx: WASTParser.BlockTypeContext):
        return super().visitBlockType(ctx)

    def visitGlobalType(self, ctx: WASTParser.GlobalTypeContext):
        return super().visitGlobalType(ctx)

    def visitMemoryType(self, ctx: WASTParser.MemoryTypeContext):
        return super().visitMemoryType(ctx)

    def visitTableType(self, ctx: WASTParser.TableTypeContext):
        return super().visitTableType(ctx)

    def visitElemType(self, ctx: WASTParser.ElemTypeContext):
        return super().visitElemType(ctx)

    def visitLimits(self, ctx: WASTParser.LimitsContext):
        return super().visitLimits(ctx)

    def visitFuncType(self, ctx: WASTParser.FuncTypeContext):
        return super().visitFuncType(ctx)

    def visitParam(self, ctx: WASTParser.ParamContext):
        return super().visitParam(ctx)

    def visitResult(self, ctx: WASTParser.ResultContext):
        return super().visitResult(ctx)

    def visitExpr(self, ctx: WASTParser.ExprContext):
        return super().visitExpr(ctx)

    def visitInstr(self, ctx: WASTParser.InstrContext):
        return super().visitInstr(ctx)

    def visitFoldedInstr(self, ctx: WASTParser.FoldedInstrContext):
        return super().visitFoldedInstr(ctx)

    def visitBlockInstr(self, ctx: WASTParser.BlockInstrContext):
        return super().visitBlockInstr(ctx)

    def visitPlainInstr(self, ctx: WASTParser.PlainInstrContext):
        return super().visitPlainInstr(ctx)

    def visitConstInstr(self, ctx: WASTParser.ConstInstrContext):
        return super().visitConstInstr(ctx)

    def visitMemArg(self, ctx: WASTParser.MemArgContext):
        return super().visitMemArg(ctx)

    def visitNat(self, ctx: WASTParser.NatContext):
        return super().visitNat(ctx)

    def visitValue(self, ctx: WASTParser.ValueContext):
        return super().visitValue(ctx)

    def visitVariable(self, ctx: WASTParser.VariableContext):
        return super().visitVariable(ctx)

    def visit(self, tree):
        return super().visit(tree)

    def visitChildren(self, node):
        return super().visitChildren(node)

    def visitTerminal(self, node):
        super().visitTerminal(node)

    def visitErrorNode(self, node):
        super().visitErrorNode(node)

    def defaultResult(self):
        super().defaultResult()

    def aggregateResult(self, aggregate, nextResult):
        return super().aggregateResult(aggregate, nextResult)

    def shouldVisitNextChild(self, node, currentResult):
        return super().shouldVisitNextChild(node, currentResult)


def new_wat_visitor():
    wat_visitor = WatVisitor()
    wat_visitor.reports_validation_error = True

