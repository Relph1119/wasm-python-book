#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: instr_control.py
@time: 2020/8/20 17:31
@project: wasm-python-book
@desc:
"""
from ch08.binary.opcodes import Call, Block, Loop, If
from ch08.interpreter import uint32
from ch08.interpreter.errors import ErrTrap


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
    idx = uint32(args)
    imported_func_count = len(vm.module.import_sec)
    if idx < imported_func_count:
        # hack!
        call_assert_func(vm, args)
    else:
        call_internal_func(vm, idx - imported_func_count)


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


def call_internal_func(vm, idx):
    ft_idx = vm.module.func_sec[idx]
    ft = vm.module.type_sec[ft_idx]
    code = vm.module.code_sec[idx]
    vm.enter_block(Call, ft, code.expr)

    local_count = int(code.get_local_count())
    for _ in range(local_count):
        vm.push_u64(0)


def call_assert_func(vm, args):
    idx = int(args)
    name = vm.module.import_sec[idx].name
    if name == 'assert_true':
        __assert_equal(vm.pop_bool(), True)
    elif name == 'assert_false':
        __assert_equal(vm.pop_bool(), False)
    elif name == 'assert_eq_i32':
        __assert_equal(vm.pop_u32(), vm.pop_u32())
    elif name == 'assert_eq_i64':
        __assert_equal(vm.pop_u64(), vm.pop_u64())
    elif name == 'assert_eq_f32':
        __assert_equal(vm.pop_f32(), vm.pop_f32())
    elif name == 'assert_eq_f64':
        __assert_equal(vm.pop_f64(), vm.pop_f64())
    else:
        raise Exception("TODO")


def __assert_equal(a, b):
    if a != b:
        raise Exception("{} != {}".format(a, b))
