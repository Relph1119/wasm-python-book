#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: code_validator.py
@time: 2020/8/24 8:42
@project: wasm-python-book
@desc: 函数字节码验证
"""
from ch11.binary.opcodes import *
from ch11.binary.types import ValTypeI32, ValTypeI64, ValTypeF32, ValTypeF64

Unknown = 0
I32 = ValTypeI32
I64 = ValTypeI64
F32 = ValTypeF32
F64 = ValTypeF64


class CtrlFrame:
    def __init__(self, opcode=None, start_types=None, end_types=None, height=0, unreachable=False):
        if end_types is None:
            end_types = []
        if start_types is None:
            start_types = []
        # 记录与控制帧对应的指令
        self.opcode = opcode
        # 控制帧的参数
        self.start_types = start_types
        # 控制帧的结果类型
        self.end_types = end_types
        # 控制帧的高度（也就是控制块的深度）
        self.height = height

        self.unreachable = unreachable

    def label_types(self):
        if self.opcode == Loop:
            return self.start_types
        return self.end_types


class CodeValidator:
    def __init__(self, mv, code_idx, instr_path=None):
        if instr_path is None:
            instr_path = dict()
        self.opds = []
        self.ctrls = []
        self.mv = mv
        self.code_idx = code_idx
        self.local_count = None
        self.max_opds = 0
        # depth -> opname
        self.instr_path = instr_path

    def error(self, msg):
        raise Exception("code[%d], %s: %s" %
                        (self.code_idx, self.get_instr_path(), msg))

    def errorf(self, format_str, a: list):
        self.error(format_str % (tuple(a)))

    def get_instr_path(self):
        return "/".join(self.instr_path.values())

    def push_opd(self, vt):
        """单个操作数的压入操作数栈操作"""
        self.opds.append(vt)
        n = len(self.opds)
        if n > self.max_opds:
            self.max_opds = n

    def pop_opd(self):
        """单个操作数的弹出操作数栈操作：从栈顶弹出一个任意类型的操作数"""
        ctrl0 = self.get_ctrl(0)
        if len(self.opds) == ctrl0.height:
            if ctrl0.unreachable:
                return Unknown
            self.error("type mismatch")
        return self.opds.pop()

    def pop_opd_of(self, expect):
        """单个操作数的弹出操作数栈操作：从栈顶弹出一个指定类型的操作数"""
        actual = self.pop_opd()
        if actual == Unknown:
            return expect
        if expect == Unknown:
            return actual
        if actual != expect:
            # TODO
            self.error("type mismatch")
        return actual

    def push_opds(self, types):
        """批量压入操作数栈"""
        for t in types:
            self.push_opd(t)

    def pop_opds(self, types):
        """批量弹出操作数栈"""
        for i in range(len(types) - 1, -1, -1):
            self.pop_opd_of(types[i])

    def push_i32(self):
        self.push_opd(I32)

    def push_i64(self):
        self.push_opd(I64)

    def push_f32(self):
        self.push_opd(F32)

    def push_f64(self):
        self.push_opd(F64)

    def pop_i32(self):
        self.pop_opd_of(I32)

    def pop_i64(self):
        self.pop_opd_of(I64)

    def pop_f32(self):
        self.pop_opd_of(F32)

    def pop_f64(self):
        self.pop_opd_of(F64)

    def get_ctrl(self, n):
        if n >= len(self.ctrls):
            self.error("")
        return self.ctrls[len(self.ctrls) - 1 - n]

    def push_ctrl(self, opcode, in_val_types, out_val_types):
        """用于控制帧的压入"""
        frame = CtrlFrame(opcode=opcode,
                          start_types=in_val_types,
                          end_types=out_val_types,
                          height=len(self.opds),
                          unreachable=False)

        self.ctrls.append(frame)
        self.push_opds(in_val_types)

    def pop_ctrl(self):
        """用于控制帧的弹出"""
        if len(self.ctrls) == 0:
            self.error("")

        frame = self.get_ctrl(0)
        self.pop_opds(frame.end_types)
        if len(self.opds) != frame.height:
            self.error("type mismatch")

        self.ctrls.pop()
        return frame

    def unreachable(self):
        """将控制帧标记为不可达"""
        self.opds = self.opds[:self.get_ctrl(0).height]
        self.ctrls[len(self.ctrls) - 1].unreachable = True

    def validate_code(self, code, ft):
        self.push_opds(ft.param_types)
        self.local_count = len(ft.param_types)
        for local in code.locals:
            for _ in range(int(local.n)):
                self.push_opd(local.type)
                self.local_count += 1

        self.push_ctrl(Block, [], ft.result_types)
        self.validate_expr(code.expr)
        self.push_opds(self.pop_ctrl().end_types)

    def validate_expr(self, expr):
        depth = len(self.instr_path)
        for instr in expr:
            self.instr_path[depth] = instr.get_opname()
            self.validate_instr(instr)
        if depth in self.instr_path.keys():
            self.instr_path.pop(depth)

    def validate_instr(self, instr):
        opcode = instr.opcode
        if opcode == Unreachable:
            self.unreachable()
        elif opcode == Nop:
            pass
        elif opcode in [Block, Loop]:
            block_args = instr.args
            bt = self.mv.module.get_block_type(block_args.bt)
            self.pop_opds(bt.param_types)
            self.push_ctrl(instr.opcode, bt.param_types, bt.result_types)
            self.validate_expr(block_args.instrs)
            self.push_opds(self.pop_ctrl().end_types)
        elif opcode == If:
            if_args = instr.args
            bt = self.mv.module.get_block_type(if_args.bt)
            self.pop_i32()
            self.pop_opds(bt.param_types)
            self.push_ctrl(If, bt.param_types, bt.result_types)
            self.validate_expr(if_args.instrs1)

            # else
            frame = self.pop_ctrl()
            if frame.opcode != If:
                self.error("TODO")
            self.push_ctrl(Else_, frame.start_types, frame.end_types)
            self.validate_expr(if_args.instrs2)

            # end
            self.push_opds(self.pop_ctrl().end_types)
        elif opcode == Br:
            n = int(instr.args)
            if len(self.ctrls) < n:
                self.error("unknown label")
            self.pop_opds(self.get_ctrl(n).label_types())
            self.unreachable()
        elif opcode == BrIf:
            n = int(instr.args)
            if len(self.ctrls) < n:
                self.error("unknown label")
            self.pop_i32()
            self.pop_opds(self.get_ctrl(n).label_types())
            self.push_opds(self.get_ctrl(n).label_types())
        elif opcode == BrTable:
            br_table_args = instr.args
            m = int(br_table_args.default)
            if len(self.ctrls) < m:
                self.error("unknown label")
            for n in br_table_args.labels:
                if len(self.ctrls) < int(n):
                    self.error("unknown label")
                t1 = self.get_ctrl(int(n)).label_types()
                t2 = self.get_ctrl(m).label_types()
                if not is_val_types_eq(t1, t2):
                    self.error("type mismatch")

            self.pop_i32()
            self.pop_opds(self.get_ctrl(m).label_types())
            self.unreachable()
        elif opcode == Return:
            n = len(self.ctrls) - 1
            self.pop_opds(self.get_ctrl(n).label_types())
            self.unreachable()
        elif opcode == Call:
            f_idx = instr.args
            ft, ok = self.mv.get_func_type(int(f_idx))
            if not ok:
                self.error("unknown function")
            self.pop_opds(ft.param_types)
            self.push_opds(ft.result_types)
        elif opcode == CallIndirect:
            if self.mv.get_table_count() == 0:
                self.error("unknown table")
            ft_idx = instr.args
            if int(ft_idx) >= self.mv.get_type_count():
                self.error("unknown type")
            ft = self.mv.module.type_sec[ft_idx]
            self.pop_i32()
            self.pop_opds(ft.param_types)
            self.push_opds(ft.result_types)
        elif opcode == Drop:
            self.pop_opd()
        elif opcode == Select:
            self.pop_i32()
            t1 = self.pop_opd()
            t2 = self.pop_opd_of(t1)
            self.push_opd(t2)
        elif opcode == LocalGet:
            n = int(instr.args)
            if n >= self.local_count:
                self.errorf("unknown local: %d", [n])
            self.push_opd(self.opds[n])
        elif opcode == LocalSet:
            n = int(instr.args)
            if n >= self.local_count:
                self.errorf("unknown local: %d", [n])
            self.pop_opd_of(self.opds[n])
        elif opcode == LocalTee:
            n = int(instr.args)
            if n >= self.local_count:
                self.errorf("unknown local: %d", [n])
            self.pop_opd_of(self.opds[n])
            self.push_opd(self.opds[n])
        elif opcode == GlobalGet:
            n = int(instr.args)
            if n >= len(self.mv.global_types):
                self.errorf("unknown global: %d", [n])
            self.push_opd(self.mv.global_types[n].val_type)
        elif opcode == GlobalSet:
            n = int(instr.args)
            if n >= len(self.mv.global_types):
                self.errorf("unknown global: %d", [n])
            gt = self.mv.global_types[n]
            if gt.mut != 1:
                self.errorf("global is immutable: %d", [n])
            self.pop_opd_of(gt.val_type)
        elif opcode == I32Load:
            self.i32_load(instr.args, 32)
        elif opcode == F32Load:
            self.f32_load(instr.args, 32)
        elif opcode == I64Load:
            self.i64_load(instr.args, 64)
        elif opcode == F64Load:
            self.f64_load(instr.args, 64)
        elif opcode in [I32Load8S, I32Load8U]:
            self.i32_load(instr.args, 8)
        elif opcode in [I32Load16S, I32Load16U]:
            self.i32_load(instr.args, 16)
        elif opcode in [I64Load8S, I64Load8U]:
            self.i64_load(instr.args, 8)
        elif opcode in [I64Load16S, I64Load16U]:
            self.i64_load(instr.args, 16)
        elif opcode in [I64Load32S, I64Load32U]:
            self.i64_load(instr.args, 32)
        elif opcode == I32Store:
            self.i32_store(instr.args, 32)
        elif opcode == I64Store:
            self.i64_store(instr.args, 64)
        elif opcode == F32Store:
            self.f32_store(instr.args, 32)
        elif opcode == F64Store:
            self.f64_store(instr.args, 64)
        elif opcode == I32Store8:
            self.i32_store(instr.args, 8)
        elif opcode == I32Store16:
            self.i32_store(instr.args, 16)
        elif opcode == I64Store8:
            self.i64_store(instr.args, 8)
        elif opcode == I64Store16:
            self.i64_store(instr.args, 16)
        elif opcode == I64Store32:
            self.i64_store(instr.args, 32)
        elif opcode == MemorySize:
            self.check_mem()
            self.push_i32()
        elif opcode == MemoryGrow:
            self.check_mem()
            self.pop_i32()
            self.push_i32()
        elif opcode == I32Const:
            self.push_i32()
        elif opcode == I64Const:
            self.push_i64()
        elif opcode == F32Const:
            self.push_f32()
        elif opcode == F64Const:
            self.push_f64()
        elif opcode == I32Eqz:
            self.pop_i32()
            self.push_i32()
        elif opcode in [I32Eq, I32Ne, I32LtS, I32LtU,
                        I32GtS, I32GtU, I32LeS, I32LeU,
                        I32GeS, I32GeU]:
            self.pop_i32()
            self.pop_i32()
            self.push_i32()
        elif opcode == I64Eqz:
            self.pop_i64()
            self.push_i32()
        elif opcode in [I64Eq, I64Ne, I64LtS, I64LtU,
                        I64GtS, I64GtU, I64LeS, I64LeU,
                        I64GeS, I64GeU]:
            self.pop_i64()
            self.pop_i64()
            self.push_i32()
        elif opcode in [F32Eq, F32Ne, F32Lt, F32Gt,
                        F32Le, F32Ge]:
            self.pop_f32()
            self.pop_f32()
            self.push_i32()
        elif opcode in [F64Eq, F64Ne, F64Lt, F64Gt,
                        F64Le, F64Ge]:
            self.pop_f64()
            self.pop_f64()
            self.push_i32()
        elif opcode in [I32Clz, I32Ctz, I32PopCnt]:
            self.pop_i32()
            self.push_i32()
        elif opcode in [I32Add, I32Sub, I32Mul,
                        I32DivS, I32DivU,
                        I32RemS, I32RemU,
                        I32And, I32Or, I32Xor,
                        I32Shl, I32ShrS, I32ShrU,
                        I32Rotl, I32Rotr]:
            self.pop_opd_of(I32)
            self.pop_opd_of(I32)
            self.push_opd(I32)
        elif opcode in [I64Clz, I64Ctz, I64PopCnt]:
            self.pop_i64()
            self.push_i64()
        elif opcode in [I64Add, I64Sub, I64Mul,
                        I64DivS, I64DivU,
                        I64RemS, I64RemU,
                        I64And, I64Or, I64Xor,
                        I64Shl, I64ShrS, I64ShrU,
                        I64Rotl, I64Rotr]:
            self.pop_i64()
            self.pop_i64()
            self.push_i64()
        elif opcode in [F32Abs, F32Neg,
                        F32Ceil, F32Floor,
                        F32Trunc, F32Nearest,
                        F32Sqrt]:
            self.pop_f32()
            self.push_f32()
        elif opcode in [F32Add, F32Sub,
                        F32Mul, F32Div,
                        F32Min, F32Max,
                        F32CopySign]:
            self.pop_f32()
            self.pop_f32()
            self.push_f32()
        elif opcode in [F64Abs, F64Neg,
                        F64Ceil, F64Floor,
                        F64Trunc, F64Nearest,
                        F64Sqrt]:
            self.pop_f64()
            self.push_f64()
        elif opcode in [F64Add, F64Sub,
                        F64Mul, F64Div,
                        F64Min, F64Max,
                        F64CopySign]:
            self.pop_f64()
            self.pop_f64()
            self.push_f64()
        elif opcode == I32WrapI64:
            self.pop_i64()
            self.push_i32()
        elif opcode in [I32TruncF32S, I32TruncF32U]:
            self.pop_f32()
            self.push_i32()
        elif opcode in [I32TruncF64S, I32TruncF64U]:
            self.pop_f64()
            self.push_i32()
        elif opcode in [I64ExtendI32S, I64ExtendI32U]:
            self.pop_i32()
            self.push_i64()
        elif opcode in [I64TruncF32S, I64TruncF32U]:
            self.pop_f32()
            self.push_i64()
        elif opcode in [I64TruncF64S, I64TruncF64U]:
            self.pop_f64()
            self.push_i64()
        elif opcode in [F32ConvertI32S, F32ConvertI32U]:
            self.pop_i32()
            self.push_f32()
        elif opcode in [F32ConvertI64S, F32ConvertI64U]:
            self.pop_i64()
            self.push_f32()
        elif opcode == F32DemoteF64:
            self.pop_f64()
            self.push_f32()
        elif opcode in [F64ConvertI32S, F64ConvertI32U]:
            self.pop_i32()
            self.push_f64()
        elif opcode in [F64ConvertI64S, F64ConvertI64U]:
            self.pop_i64()
            self.push_f64()
        elif opcode == F64PromoteF32:
            self.pop_f32()
            self.push_f64()
        elif opcode == I32ReinterpretF32:
            self.pop_f32()
            self.push_i32()
        elif opcode == I64ReinterpretF64:
            self.pop_f64()
            self.push_i64()
        elif opcode == F32ReinterpretI32:
            self.pop_i32()
            self.push_f32()
        elif opcode == F64ReinterpretI64:
            self.pop_i64()
            self.push_f64()
        elif opcode in [I32Extend8S, I32Extend16S]:
            self.pop_i32()
            self.push_i32()
        elif opcode in [I64Extend8S, I64Extend16S, I64Extend32S]:
            self.pop_i64()
            self.push_i64()
        elif opcode == TruncSat:
            args = instr.args
            if args in [0, 1]:
                self.pop_f32()
                self.push_i32()
            elif args in [2, 3]:
                self.pop_f64()
                self.push_i32()
            elif args in [4, 5]:
                self.pop_f32()
                self.push_i64()
            elif args in [6, 7]:
                self.pop_f64()
                self.push_i64()
        else:
            self.errorf("unknown opcode: 0x%x", instr.opcode)

    def i32_load(self, args, bit_width):
        self.load(ValTypeI32, bit_width, args)

    def i64_load(self, args, bit_width):
        self.load(ValTypeI64, bit_width, args)

    def f32_load(self, args, bit_width):
        self.load(ValTypeF32, bit_width, args)

    def f64_load(self, args, bit_width):
        self.load(ValTypeF64, bit_width, args)

    def i32_store(self, args, bit_width):
        self.store(ValTypeI32, bit_width, args)

    def i64_store(self, args, bit_width):
        self.store(ValTypeI64, bit_width, args)

    def f32_store(self, args, bit_width):
        self.store(ValTypeF32, bit_width, args)

    def f64_store(self, args, bit_width):
        self.store(ValTypeF64, bit_width, args)

    def load(self, vt, bit_width, args):
        self.check_mem()
        self.check_align(bit_width, args)
        self.pop_i32()
        self.push_opd(vt)

    def store(self, vt, bit_width, args):
        self.check_mem()
        self.check_align(bit_width, args)
        self.pop_opd_of(vt)
        self.pop_i32()

    def check_mem(self):
        if self.mv.get_mem_count() == 0:
            self.error("unknown memory")

    def check_align(self, bit_width, args):
        align = args.align
        if (1 << align) > (bit_width / 8):
            self.errorf("alignment must not be larger than natural alignment (%d)",
                        [bit_width / 8])


def validate_code(mv, idx, code, ft):
    cv = CodeValidator(mv=mv, code_idx=idx, instr_path=dict())
    cv.validate_code(code, ft)


def is_val_types_eq(a, b) -> bool:
    if len(a) != len(b):
        return False
    for i, vt in enumerate(a):
        if vt != b[i]:
            return False
    return True
