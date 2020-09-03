#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: build_instr.py
@time: 2020/8/31 19:22
@project: wasm-python-book
@desc:
"""
from binary.instruction import Instruction, BlockArgs, IfArgs
from binary.opcodes import *
from binary.opnames import get_opcode


def new_instruction(opname):
    try:
        opcode = get_opcode(opname)
        return Instruction(opcode)
    except Exception:
        return new_trunc_sat(opname)


def new_trunc_sat(opname):
    instr = Instruction(opcode=TruncSat)
    if opname == "i32.trunc_sat_f32_s":
        instr.args = 0x00
    elif opname == "i32.trunc_sat_f32_u":
        instr.args = 0x01
    elif opname == "i32.trunc_sat_f64_s":
        instr.args = 0x02
    elif opname == "i32.trunc_sat_f64_u":
        instr.args = 0x03
    elif opname == "i64.trunc_sat_f32_s":
        instr.args = 0x04
    elif opname == "i64.trunc_sat_f32_u":
        instr.args = 0x05
    elif opname == "i64.trunc_sat_f64_s":
        instr.args = 0x06
    elif opname == "i64.trunc_sat_f64_u":
        instr.args = 0x07
    else:
        raise Exception("unreachable")
    return instr


def new_i32_const0():
    instr = Instruction()
    instr.opcode = I32Const
    instr.args = 0


def new_block_instr(opname, bt, expr1, expr2):
    instr = new_instruction(opname)
    opcode = instr.opcode
    if opcode in [Block, Loop]:
        instr.args = BlockArgs(bt, expr1)
    elif opcode == If:
        if_args = IfArgs()
        if_args.bt = bt
        if_args.instrs1 = expr1
        if_args.instrs2 = expr2
        instr.args = if_args
    else:
        raise Exception("unreachable")

    return instr
