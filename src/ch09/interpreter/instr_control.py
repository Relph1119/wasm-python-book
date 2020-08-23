#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: instr_control.py
@time: 2020/8/20 17:31
@project: wasm-python-book
@desc:
"""
from ch09.binary.opcodes import Call, Block, Loop, If
from ch09.interpreter import uint32
from ch09.interpreter.errors import ErrTrap, ErrUndefinedElem, ErrTypeMismatch
from ch09.interpreter.val import warp_u64, unwrap_u64


def unreachable(vm, _):
    raise ErrTrap


def nop(vm, _):
    pass


def block(vm, args):
    block_args = args
    bt = vm.module.get_block_type(block_args.bt)
    vm.enter_block(Block, bt, block_args.instrs)


def loop(vm, args):
    block_args = args
    bt = vm.module.get_block_type(block_args.bt)
    vm.enter_block(Loop, bt, block_args.instrs)


def control_if(vm, args):
    if_args = args
    bt = vm.module.get_block_type(if_args.bt)
    if vm.pop_bool():
        vm.enter_block(If, bt, if_args.instrs1)
    else:
        vm.enter_block(If, bt, if_args.instrs2)


def br(vm, args):
    label_idx = args
    # 先弹出label_idx个控制帧
    for _ in range(label_idx):
        vm.pop_control_frame()
    cf = vm.top_control_frame
    if cf.opcode != Loop:
        # block或者if块，再弹出一个控制帧
        vm.exit_block()
    else:
        vm.reset_block(cf)
        cf.pc = 0


def br_if(vm, args):
    if vm.pop_bool():
        br(vm, args)


def br_table(vm, args):
    br_table_args = args
    n = vm.pop_u32()
    if n < len(br_table_args.labels):
        br(vm, br_table_args.labels[n])
    else:
        br(vm, br_table_args.default)


def control_return(vm, _):
    # 找到函数最外层块的标签索引（也就是当前控制块的深度）
    _, label_idx = vm.top_call_frame()
    br(vm, uint32(label_idx))


def call(vm, args):
    f = vm.funcs[args]
    call_func(vm, f)


def call_func(vm, f):
    if f.py_func is not None:
        call_external_func(vm, f)
    else:
        call_internal_func(vm, f)


def call_external_func(vm, f):
    # 先根据函数签名把参数从栈顶弹出
    args = pop_args(vm, f.type)
    # 调用本地函数，最后把返回值压栈
    results = f.py_func(args)
    if results is None:
        results = []
    push_results(vm, f.type, results)


def pop_args(vm, ft):
    param_count = len(ft.param_types)
    args = [None] * param_count
    for i in range(param_count - 1, -1, -1):
        args[i] = warp_u64(ft.param_types[i], vm.pop_u64())
    return args


def push_results(vm, ft, results):
    if len(ft.result_types) != len(results):
        raise Exception("TODO")
    for result in results:
        vm.push_u64(unwrap_u64(ft.result_types[0], result))


"""
operand stack:

+~~~~~~~~~~~~~~~+
|               |
+---------------+
|     stack     |
+---------------+
|     locals    |
+---------------+
|     params    |
+---------------+
|  ............ |
"""


def call_internal_func(vm, f):
    vm.enter_block(Call, f.type, f.code.expr)

    local_count = int(f.code.get_local_count())
    for _ in range(local_count):
        vm.push_u64(0)


def call_indirect(vm, args):
    type_idx = args
    ft = vm.module.type_sec[type_idx]

    i = vm.pop_u32()
    if i >= vm.table.size:
        raise ErrUndefinedElem

    f = vm.table.get_elem(i)
    if f.type.get_signature() != ft.get_signature():
        raise ErrTypeMismatch

    call_func(vm, f)
