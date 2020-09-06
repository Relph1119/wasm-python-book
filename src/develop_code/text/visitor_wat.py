#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: wat_visitor.py
@time: 2020/8/31 18:25
@project: wasm-python-book
@desc:
"""
import contextlib
import math

from binary.instruction import BrTableArgs, MemArg
from binary.module import Import, ImportDesc, ImportTagFunc, ImportTagTable, ImportTagMem, ImportTagGlobal, \
    ExportTagFunc, ExportTagTable, PageSize, ExportTagMem, ExportTagGlobal
from binary.opcodes import *
from binary.types import Limits, ValTypeI32, ValTypeI64, ValTypeF32, ValTypeF64, BlockTypeI32, BlockTypeI64, \
    BlockTypeF32, BlockTypeF64, FuncType, BlockTypeEmpty, MutConst, MutVar, GlobalType, TableType
from text.builder_code import new_code_builder
from text.builder_instr import new_i32_const0, new_block_instr, new_instruction
from text.builder_module import new_module_builder
from text.error_reporter import ErrorReporter
from text.errors import new_verification_error
from text.num_parser import parse_u32, parse_i32, parse_i64, parse_f32, parse_f64
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
        self.error_reporter = ErrorReporter()
        super(ErrorReporter, self.error_reporter).__init__()

    def visitModule(self, ctx: WASTParser.ModuleContext):
        return ctx.watModule().accept(self).module

    def visitWatModule(self, ctx: WASTParser.WatModuleContext):
        name = get_text(ctx.NAME())
        self.module_builder = new_module_builder()
        self.module_builder.pass_ = 1
        nv = WatNamesVisitor(self.error_reporter)
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
                ctx.typeDef().accept(self)
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
            err = self.code_builder.add_local(name.getText(), vt)
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
        return [ctx.kind.text, ctx.variable().getText()]

    def visitStart(self, ctx: WASTParser.StartContext):
        err = self.module_builder.ensure_no_start()
        self.report_err(err, ctx.getChild(1))
        _var = ctx.variable()
        err = self.module_builder.add_start(_var.getText())
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
            idx, err = self.module_builder.get_func_type_idx(_var.getText())
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
                    if isinstance(ctx.parentCtx, WASTParser.PlainInstrContext):
                        msg += " in call_indirect"
                    err = new_verification_error(msg)
                    self.report_err(err, ctx.getChild(1))

            return idx

        return self.module_builder.add_type_use(ft)

    def visitFuncVars(self, ctx: WASTParser.FuncVarsContext):
        func_indices = []
        for _var in ctx.variable():
            idx, err = self.module_builder.get_func_idx(_var.getText())
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
        vt = ctx.valType().accept(self)
        mut = MutConst
        if ctx.getChildCount() > 1:
            mut = MutVar
        return GlobalType(val_type=vt, mut=mut)

    def visitMemoryType(self, ctx: WASTParser.MemoryTypeContext):
        return ctx.limits().accept(self)

    def visitTableType(self, ctx: WASTParser.TableTypeContext):
        return TableType(elem_type=FuncType,
                         limits=ctx.limits().accept(self))

    def visitLimits(self, ctx: WASTParser.LimitsContext):
        mt = Limits()
        mt.min = parse_u32(ctx.nat(0).getText())
        max_value = ctx.nat(1)
        if max_value is not None:
            mt.tag = 1
            mt.max = parse_u32(max_value.getText())
        return mt

    def visitFuncType(self, ctx: WASTParser.FuncTypeContext):
        ft = FuncType()
        for param in ctx.param():
            ft.param_types.extend(param.accept(self))
        for result in ctx.result():
            ft.result_types.extend(result.accept(self))
        return ft

    def visitParam(self, ctx: WASTParser.ParamContext):
        params = []
        name = ctx.NAME()
        if name is not None:
            vt = ctx.valType(0).accept(self)
            params.append(vt)
            if self.code_builder is not None:
                err = self.code_builder.add_param(name.getText())
                self.report_err(err, name)
        else:
            for vt in ctx.valType():
                params.append(vt.accept(self))
                if self.code_builder is not None:
                    self.code_builder.add_param("")

        return params

    def visitResult(self, ctx: WASTParser.ResultContext):
        vts = ctx.valType()
        results = []
        for vt in ctx.valType():
            results.append(vt.accept(self))
        return results

    def visitExpr(self, ctx: WASTParser.ExprContext):
        expr = []
        for instr in ctx.instr():
            instrs = instr.accept(self)
            expr.extend(instrs)
        return expr

    def visitInstr(self, ctx: WASTParser.InstrContext):
        if ctx.plainInstr() is not None:
            instr = ctx.plainInstr().accept(self)
            return [instr]
        if ctx.blockInstr() is not None:
            instr = ctx.blockInstr().accept(self)
            return [instr]
        return ctx.foldedInstr().accept(self)

    def visitFoldedInstr(self, ctx: WASTParser.FoldedInstrContext):
        instrs = []
        for floded_instr in ctx.foldedInstr():
            instr = floded_instr.accept(self)
            if isinstance(instr, list):
                instrs.extend(instr)

        op = ctx.op
        if op is not None:
            self.code_builder.enter_block()
            with contextlib.ExitStack() as stack:
                stack.callback(self.code_builder.exit_block)

            label = ctx.label
            if label is not None:
                self.code_builder.define_label(label.text)

            op = ctx.op.text
            rt = ctx.blockType().accept(self)
            expr1 = ctx.expr(0).accept(self)
            expr2 = get_expr(ctx.expr(1), self)
            instr = new_block_instr(op, rt, expr1, expr2)
        else:
            instr = ctx.plainInstr().accept(self)

        instrs.append(instr)
        return instrs

    def visitBlockInstr(self, ctx: WASTParser.BlockInstrContext):
        self.code_builder.enter_block()
        with contextlib.ExitStack() as stack:
            stack.callback(self.code_builder.exit_block)

        label = ctx.label
        if label is not None:
            self.code_builder.define_label(label.text)

        op = ctx.op.text
        rt = ctx.blockType().accept(self)
        expr1 = ctx.expr(0).accept(self)
        expr2 = get_expr(ctx.expr(1), self)
        return new_block_instr(op, rt, expr1, expr2)

    def visitPlainInstr(self, ctx: WASTParser.PlainInstrContext):
        if ctx.constInstr() is not None:
            return ctx.constInstr().accept(self)

        op = ctx.op.text
        instr = new_instruction(op)
        opcode = instr.opcode

        if opcode in [Br, BrIf]:
            _var = ctx.variable(0)
            idx, err = self.code_builder.get_br_label_idx(_var.getText())
            instr.args = idx
            self.report_err(err, ctx.variable(0))
        elif opcode == BrTable:
            labels = []
            for _var in ctx.variable():
                idx, err = self.code_builder.get_br_label_idx(_var.getText())
                labels.append(idx)
                self.report_err(err, _var)

            instr.args = BrTableArgs(labels=labels[:len(labels) - 1],
                                     default=labels[len(labels) - 1])
        elif opcode == Call:
            _var = ctx.variable(0)
            idx, err = self.module_builder.get_func_idx(_var.getText())
            instr.args = idx
            self.report_err(err, _var)
        elif opcode == CallIndirect:
            ft_idx = ctx.typeUse().accept(self)
            instr.args = ft_idx
            # TODO

        if LocalGet <= opcode <= LocalTee:
            _var = ctx.variable(0)
            if self.code_builder is not None:
                idx, err = self.code_builder.get_local_idx(_var.getText())
                instr.args = idx
                self.report_err(err, _var)
            else:
                instr.args = parse_u32(_var.getText())
        elif GlobalGet <= opcode <= GlobalSet:
            _var = ctx.variable(0)
            idx, err = self.module_builder.get_global_idx(_var.getText())
            instr.args = idx
            self.report_err(err, _var)
        elif I32Load <= opcode <= I64Store32:
            instr.args = ctx.memArg().accept(self)

        return instr

    def visitConstInstr(self, ctx: WASTParser.ConstInstrContext):
        instr = new_instruction(ctx.op.text)
        val = ctx.value().getText()
        opcode = instr.opcode
        if opcode == I32Const:
            instr.args = parse_i32(val)
        elif opcode == I64Const:
            instr.args = parse_i64(val)
        elif opcode == F32Const:
            instr.args = parse_f32(val)
        elif opcode == F64Const:
            instr.args = parse_f64(val)
        else:
            raise Exception("unreachable")
        return instr

    def visitMemArg(self, ctx: WASTParser.MemArgContext):
        mem_arg = MemArg()
        offset = ctx.offset
        if offset is not None:
            mem_arg.offset = parse_u32(offset.getText())
        align = ctx.align
        if align is not None:
            align_val = parse_u32(align.getText())
            if align_val == 1:
                mem_arg.align = 0
            elif align_val == 2:
                mem_arg.align = 1
            elif align_val == 4:
                mem_arg.align = 2
            elif align_val == 8:
                mem_arg.align = 3
            elif align_val == 16:
                mem_arg.align = 4
            elif align_val == 32:
                mem_arg.align = 5
            elif align_val == 64:
                mem_arg.align = 6
            else:
                raise Exception("invalid align")

        return mem_arg


def new_wat_visitor():
    wat_visitor = WatVisitor()
    wat_visitor.reports_validation_error = True
    return wat_visitor
