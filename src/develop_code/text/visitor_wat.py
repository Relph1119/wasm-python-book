#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: wat_visitor.py
@time: 2020/8/31 18:25
@project: wasm-python-book
@desc:
"""
import math

from binary.module import Import, ImportDesc, ImportTagFunc, ImportTagTable, ImportTagMem, ImportTagGlobal, \
    ExportTagFunc, ExportTagTable, PageSize, ExportTagMem, ExportTagGlobal
from binary.types import Limits, ValTypeI32, ValTypeI64, ValTypeF32, ValTypeF64, BlockTypeI32, BlockTypeI64, \
    BlockTypeF32, BlockTypeF64, FuncType, BlockTypeEmpty
from text.builder_code import new_code_builder
from text.builder_instr import new_i32_const0
from text.builder_module import new_module_builder
from text.error_reporter import ErrorReporter
from text.errors import new_verification_error
from text.parser.WASTParser import WASTParser
from text.parser.WASTVisitor import WASTVisitor
from text.visitor_utils import get_text, get_str, get_expr, get_all_str
from text.visitor_wat_names import WatNamesVisitor
from text.wast_script import WatModule


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
        self.module_builder.pass_ = 1
        nv = WatNamesVisitor()
        nv.module_builder = self.module_builder
        for field in ctx.moduleField():
            field.accept(self)
            field.accept(nv)

        self.module_builder.pass_ = 2
        for field in ctx.moduleField():
            field.accept(self)

        wat_module = WatModule()
        wat_module.line = ctx.kw.line
        wat_module.name = name
        wat_module.module = self.module_builder.module
        return wat_module

    def visitModuleField(self, ctx: WASTParser.ModuleFieldContext):
        pass_ = self.module_builder.pass_
        if pass_ == 1:
            if ctx.typeDef() is not None:
                ctx.typeDef().accept()
        elif pass_ == 2:
            if ctx.typeDef() is None:
                ctx.getChild(0).accept(self)
        return None

    def visitTypeDef(self, ctx: WASTParser.TypeDefContext):
        name = ctx.NAME()
        ft = ctx.funcType().accept(self)
        err = self.module_builder.add_type_def(get_text(name), ft)
        self.report_err(err, name)
        return None

    def visitImport_(self, ctx: WASTParser.Import_Context):
        imp = Import(module=get_str(ctx.STRING(0)),
                     name=get_str(ctx.STRING(1)),
                     desc=ctx.importDesc().accept(self))
        self.module_builder.add_import(imp)
        return None

    def visitImportDesc(self, ctx: WASTParser.ImportDescContext):
        kind = ctx.kind.text
        if kind == "func":
            return ImportDesc(tag=ImportTagFunc,
                              func_type=ctx.typeUse().accept(self))
        elif kind == "table":
            return ImportDesc(tag=ImportTagTable,
                              table=ctx.tableType().accept(self))
        elif kind == "memory":
            return ImportDesc(tag=ImportTagMem,
                              mem=ctx.memoryType().accept(self))
        elif kind == "global":
            return ImportDesc(tag=ImportTagGlobal,
                              global_type=ctx.globalType().accept(self))
        else:
            raise Exception("unreachable")

    def visitFunc_(self, ctx: WASTParser.Func_Context):
        self.code_builder = new_code_builder()
        ft_idx = ctx.typeUse().accept(self)

        if ctx.embeddedIm() is not None:
            imp = ctx.embeddedIm().accept(self)
            imp.desc = ImportDesc(tag=ImportTagFunc, func_type=ft_idx)
            idx = self.module_builder.add_import(imp)
        else:
            for local in ctx.funcLocal():
                local.accept(self)
            expr = get_expr(ctx.expr(), self)
            locals_vec = self.code_builder.locals
            idx = self.module_builder.add_func(ft_idx,
                                               locals_vec=locals_vec,
                                               expr=expr)

        if ctx.embeddedEx() is not None:
            names = ctx.embeddedEx().accept(self)
            for name in names:
                self.module_builder.add_export(name, ExportTagFunc, idx)

        self.code_builder = None
        return None

    def visitFuncLocal(self, ctx: WASTParser.FuncLocalContext):
        name = ctx.NAME()
        if name is not None:
            vt = ctx.valType(0).accept(self)
            err = self.code_builder.add_local(name.text, vt)
            self.report_err(err, name)
        else:
            for vt in ctx.valType():
                self.code_builder.add_local("", vt.accept(self))

        return None

    def visitTable(self, ctx: WASTParser.TableContext):
        if ctx.embeddedIm() is not None:
            imp = ctx.embeddedIm().accept(self)
            imp.desc = ImportDesc(tag=ImportTagTable,
                                  table=ctx.tableType().accept(self))
            self.module_builder.add_import(imp)
        elif ctx.tableType() is not None:
            tt = ctx.tableType().accept(self)
            err = self.module_builder.add_table(tt)
            self.report_err(err, ctx.getChild(1))
        elif ctx.elemType() is not None:
            func_indices = ctx.funcVars().accept(self)
            err = self.module_builder.add_table_with_elems(func_indices)
            self.report_err(err, ctx.getChild(1))
        if ctx.embeddedEx() is not None:
            names = ctx.embeddedEx().accept(self)
            for name in names:
                self.module_builder.add_export(name, ExportTagTable, 0)

        return None

    def visitMemory(self, ctx: WASTParser.MemoryContext):
        if ctx.embeddedIm() is not None:
            imp = ctx.embeddedIm().accept(self)
            imp.desc = ImportDesc(tag=ImportTagMem,
                                  mem=ctx.memoryType().accept(self))
            self.module_builder.add_import(imp)
        elif ctx.memoryType() is not None:
            mt = ctx.memoryType().accept(self)
            err = self.module_builder.add_memory(mt)
            self.report_err(err, ctx.getChild(1))
        else:
            offset = [new_i32_const0()]
            init_data = get_all_str(ctx.STRING())
            min_value = math.ceil(len(init_data) / PageSize)
            mt = Limits(min=min_value)
            err = self.module_builder.add_memory(mt)
            self.report_err(err, ctx.getChild(1))
            self.module_builder.add_data("", offset, init_data)

        if ctx.embeddedEx() is not None:
            names = ctx.embeddedEx().accept(self)
            for name in names:
                self.module_builder.add_export(name, ExportTagMem, 0)

        return None

    def visitGlobal(self, ctx: WASTParser.GlobalContext):
        idx = 0
        if ctx.embeddedIm() is not None:
            imp = ctx.embeddedIm().accept(self)
            imp.desc = ImportDesc(tag=ImportTagGlobal,
                                  global_type=ctx.globalType().accept(self))
            idx = self.module_builder.add_import(imp)
        else:
            gt = ctx.globalType().accept(self)
            expr = get_expr(ctx.expr(), self)
            idx = self.module_builder.add_global(gt, expr)

        if ctx.embeddedEx() is not None:
            names = ctx.embeddedEx().accept(self)
            for name in names:
                self.module_builder.add_export(name, ExportTagGlobal, idx)

        return None

    def visitExport(self, ctx: WASTParser.ExportContext):
        idx = 0
        err = None

        name = get_str(ctx.STRING())
        kind_and_var = ctx.exportDesc().accept(self)
        if kind_and_var[0] == "func":
            idx, err = self.module_builder.get_func_idx(kind_and_var[1])
            self.module_builder.add_export(name, ImportTagFunc, idx)
        elif kind_and_var[0] == "table":
            idx, err = self.module_builder.get_table_idx(kind_and_var[1])
            self.module_builder.add_export(name, ImportTagTable, idx)
        elif kind_and_var[0] == "memory":
            idx, err = self.module_builder.get_mem_idx(kind_and_var[1])
            self.module_builder.add_export(name, ImportTagMem, idx)
        elif kind_and_var[0] == "global":
            idx, err = self.module_builder.get_global_idx(kind_and_var[1])
            self.module_builder.add_export(name, ImportTagGlobal, idx)
        else:
            raise Exception("unreachable")

        if err is not None:
            self.report_err(err, ctx.exportDesc().getChild(2).getChild(0))
        return None

    def visitExportDesc(self, ctx: WASTParser.ExportDescContext):
        return [ctx.kind.text, ctx.variable().text]

    def visitStart(self, ctx: WASTParser.StartContext):
        err = self.module_builder.ensure_no_start()
        self.report_err(err, ctx.getChild(1))
        _var = ctx.variable()
        err = self.module_builder.add_start(_var.text)
        self.report_err(err, _var)
        return None

    def visitElem(self, ctx: WASTParser.ElemContext):
        _var = ctx.variable()
        offset = ctx.expr().accept(self)
        init_data = ctx.funcVars().accept(self)
        err = self.module_builder.add_elem(get_text(_var), offset, init_data)
        self.report_err(err, _var)
        return None

    def visitData(self, ctx: WASTParser.DataContext):
        _var = ctx.variable()
        offset = ctx.expr().accept(self)
        init_data = get_all_str(ctx.STRING())
        err = self.module_builder.add_data(get_text(_var), offset, init_data)
        self.report_err(err, _var)
        return None

    def visitEmbeddedIm(self, ctx: WASTParser.EmbeddedImContext):
        return Import(module=get_str(ctx.STRING(0)),
                      name=get_str(ctx.STRING(1)))

    def visitEmbeddedEx(self, ctx: WASTParser.EmbeddedExContext):
        names = []
        for name in ctx.STRING():
            names.append(get_str(name))
        return names

    def visitTypeUse(self, ctx: WASTParser.TypeUseContext):
        ft = ctx.funcType().accept(self)
        _var = ctx.variable()
        if _var is not None:
            idx, err = self.module_builder.get_func_type_idx(_var.text)
            if err is not None:
                self.report_err(err, _var)
                return idx

            ft_use = self.module_builder.module.type_sec[idx]
            if len(ft.param_types) == 0 and len(ft.result_types) == 0:
                if self.code_builder is not None:
                    for _ in ft_use.param_types:
                        self.code_builder.add_param("")
            else:
                if ft.get_signature() != ft_use.get_signature():
                    msg = "type mismatch"
                    if ctx.parentCtx is not None:
                        msg += " in call_indirect"
                    err = new_verification_error(msg)
                    self.report_err(err, ctx.getChild(1))

            return idx

        return self.module_builder.add_type_use(ft)

    def visitFuncVars(self, ctx: WASTParser.FuncVarsContext):
        func_indices = []
        for _var in ctx.variable():
            idx, err = self.module_builder.get_func_idx(_var.text)
            self.report_err(err, _var)
            func_indices.append(idx)
        return func_indices

    def visitValType(self, ctx: WASTParser.ValTypeContext):
        text = ctx.getText()
        if text == 'i32':
            return ValTypeI32
        elif text == 'i64':
            return ValTypeI64
        elif text == 'f32':
            return ValTypeF32
        elif text == 'f64':
            return ValTypeF64
        else:
            raise Exception("unreachable")

    def visitBlockType(self, ctx: WASTParser.BlockTypeContext):
        if ctx.result() is not None:
            result = ctx.result().accept(self)
            if len(result) == 1:
                if result[0] == ValTypeI32:
                    return BlockTypeI32
                elif result[0] == ValTypeI64:
                    return BlockTypeI64
                elif result[0] == ValTypeF32:
                    return BlockTypeF32
                elif result[0] == ValTypeF64:
                    return BlockTypeF64
            ft = FuncType(result_types=result)
            ft_idx = self.module_builder.add_type_use(ft)
            return int(ft_idx)

        if ctx.typeUse() is not None:
            ft_idx = ctx.typeUse().accept(self)
            return int(ft_idx)

        return BlockTypeEmpty

    def visitGlobalType(self, ctx: WASTParser.GlobalTypeContext):
        pass


def new_wat_visitor():
    wat_visitor = WatVisitor()
    wat_visitor.reports_validation_error = True
    return wat_visitor
