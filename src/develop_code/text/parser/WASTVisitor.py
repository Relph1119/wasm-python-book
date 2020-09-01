# Generated from WAST.g4 by ANTLR 4.8
from antlr4 import *

if __name__ is not None and "." in __name__:
    from .WASTParser import WASTParser
else:
    from text.parser.WASTParser import WASTParser


# This class defines a complete generic visitor for a parse tree produced by WASTParser.

class WASTVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by WASTParser#script.
    def visitScript(self, ctx: WASTParser.ScriptContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WASTParser#cmd.
    def visitCmd(self, ctx: WASTParser.CmdContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WASTParser#wastModule.
    def visitWastModule(self, ctx: WASTParser.WastModuleContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WASTParser#action_.
    def visitAction_(self, ctx: WASTParser.Action_Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WASTParser#assertion.
    def visitAssertion(self, ctx: WASTParser.AssertionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WASTParser#expected.
    def visitExpected(self, ctx: WASTParser.ExpectedContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WASTParser#meta.
    def visitMeta(self, ctx: WASTParser.MetaContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WASTParser#module.
    def visitModule(self, ctx: WASTParser.ModuleContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WASTParser#watModule.
    def visitWatModule(self, ctx: WASTParser.WatModuleContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WASTParser#moduleField.
    def visitModuleField(self, ctx: WASTParser.ModuleFieldContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WASTParser#typeDef.
    def visitTypeDef(self, ctx: WASTParser.TypeDefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WASTParser#import_.
    def visitImport_(self, ctx: WASTParser.Import_Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WASTParser#importDesc.
    def visitImportDesc(self, ctx: WASTParser.ImportDescContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WASTParser#func_.
    def visitFunc_(self, ctx: WASTParser.Func_Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WASTParser#funcLocal.
    def visitFuncLocal(self, ctx: WASTParser.FuncLocalContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WASTParser#table.
    def visitTable(self, ctx: WASTParser.TableContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WASTParser#memory.
    def visitMemory(self, ctx: WASTParser.MemoryContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WASTParser#global.
    def visitGlobal(self, ctx: WASTParser.GlobalContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WASTParser#export.
    def visitExport(self, ctx: WASTParser.ExportContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WASTParser#exportDesc.
    def visitExportDesc(self, ctx: WASTParser.ExportDescContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WASTParser#start.
    def visitStart(self, ctx: WASTParser.StartContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WASTParser#elem.
    def visitElem(self, ctx: WASTParser.ElemContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WASTParser#data.
    def visitData(self, ctx: WASTParser.DataContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WASTParser#embeddedIm.
    def visitEmbeddedIm(self, ctx: WASTParser.EmbeddedImContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WASTParser#embeddedEx.
    def visitEmbeddedEx(self, ctx: WASTParser.EmbeddedExContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WASTParser#typeUse.
    def visitTypeUse(self, ctx: WASTParser.TypeUseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WASTParser#funcVars.
    def visitFuncVars(self, ctx: WASTParser.FuncVarsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WASTParser#valType.
    def visitValType(self, ctx: WASTParser.ValTypeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WASTParser#blockType.
    def visitBlockType(self, ctx: WASTParser.BlockTypeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WASTParser#globalType.
    def visitGlobalType(self, ctx: WASTParser.GlobalTypeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WASTParser#memoryType.
    def visitMemoryType(self, ctx: WASTParser.MemoryTypeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WASTParser#tableType.
    def visitTableType(self, ctx: WASTParser.TableTypeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WASTParser#elemType.
    def visitElemType(self, ctx: WASTParser.ElemTypeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WASTParser#limits.
    def visitLimits(self, ctx: WASTParser.LimitsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WASTParser#funcType.
    def visitFuncType(self, ctx: WASTParser.FuncTypeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WASTParser#param.
    def visitParam(self, ctx: WASTParser.ParamContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WASTParser#result.
    def visitResult(self, ctx: WASTParser.ResultContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WASTParser#expr.
    def visitExpr(self, ctx: WASTParser.ExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WASTParser#instr.
    def visitInstr(self, ctx: WASTParser.InstrContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WASTParser#foldedInstr.
    def visitFoldedInstr(self, ctx: WASTParser.FoldedInstrContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WASTParser#blockInstr.
    def visitBlockInstr(self, ctx: WASTParser.BlockInstrContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WASTParser#plainInstr.
    def visitPlainInstr(self, ctx: WASTParser.PlainInstrContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WASTParser#constInstr.
    def visitConstInstr(self, ctx: WASTParser.ConstInstrContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WASTParser#memArg.
    def visitMemArg(self, ctx: WASTParser.MemArgContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WASTParser#nat.
    def visitNat(self, ctx: WASTParser.NatContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WASTParser#value.
    def visitValue(self, ctx: WASTParser.ValueContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WASTParser#variable.
    def visitVariable(self, ctx: WASTParser.VariableContext):
        return self.visitChildren(ctx)


del WASTParser
