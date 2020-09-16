#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: instr_memory.py
@time: 2020/8/21 17:09
@project: wasm-python-book
@desc: 内存指令
"""

from interpreter import int32, int8, int16, uint32, int64, uint64, uint16, uint8


def memory_size(vm, _):
    vm.push_u32(vm.memory.size)


def memory_grow(vm, _):
    old_size = vm.memory.grow(vm.pop_u32())
    vm.push_u32(old_size)


# load
def i32_load(vm, mem_arg):
    val = read_u32(vm, mem_arg)
    vm.push_u32(val)


def i64_load(vm, mem_arg):
    val = read_u64(vm, mem_arg)
    vm.push_u64(val)


def f32_load(vm, mem_arg):
    val = read_u32(vm, mem_arg)
    vm.push_u32(val)


def f64_load(vm, mem_arg):
    val = read_u64(vm, mem_arg)
    vm.push_u64(val)


def i32_load_8s(vm, mem_arg):
    val = read_u8(vm, mem_arg)
    vm.push_u32(int32(int8(val)))


def i32_load_8u(vm, mem_arg):
    val = read_u8(vm, mem_arg)
    vm.push_u32(uint32(val))


def i32_load_16s(vm, mem_arg):
    val = read_u16(vm, mem_arg)
    vm.push_s32(int32(int16(val)))


def i32_load_16u(vm, mem_arg):
    val = read_u16(vm, mem_arg)
    vm.push_u32(uint32(val))


def i64_load_8s(vm, mem_arg):
    val = read_u8(vm, mem_arg)
    vm.push_s64(int64(int8(val)))


def i64_load_8u(vm, mem_arg):
    val = read_u8(vm, mem_arg)
    vm.push_u64(uint64(val))


def i64_load_16s(vm, mem_arg):
    val = read_u16(vm, mem_arg)
    vm.push_s64(int64(int16(val)))


def i64_load_16u(vm, mem_arg):
    val = read_u16(vm, mem_arg)
    vm.push_u64(uint64(val))


def i64_load_32s(vm, mem_arg):
    val = read_u32(vm, mem_arg)
    vm.push_s64(int64(int32(val)))


def i64_load_32u(vm, mem_arg):
    val = read_u32(vm, mem_arg)
    vm.push_u64(uint64(val))


def read_u8(vm, mem_arg):
    buf = [0x00]
    offset = get_offset(vm, mem_arg)
    buf = vm.memory.read(offset, buf)
    return buf[0]


def read_u16(vm, mem_arg):
    buf = [0x00] * 2
    offset = get_offset(vm, mem_arg)
    buf = vm.memory.read(offset, buf)
    return uint16(int.from_bytes(bytearray(buf), byteorder='little'))


def read_u32(vm, mem_arg):
    buf = [0x00] * 4
    offset = get_offset(vm, mem_arg)
    buf = vm.memory.read(offset, buf)
    return uint32(int.from_bytes(bytearray(buf), byteorder='little'))


def read_u64(vm, mem_arg):
    buf = [0x00] * 8
    offset = get_offset(vm, mem_arg)
    buf = vm.memory.read(offset, buf)
    return uint64(int.from_bytes(bytearray(buf), byteorder='little'))


# store
def i32_store(vm, mem_arg):
    val = vm.pop_u32()
    write_u32(vm, mem_arg, val)


def i64_store(vm, mem_arg):
    val = vm.pop_u64()
    write_u64(vm, mem_arg, val)


def f32_store(vm, mem_arg):
    val = vm.pop_u32()
    write_u32(vm, mem_arg, val)


def f64_store(vm, mem_arg):
    val = vm.pop_u64()
    write_u64(vm, mem_arg, val)


def i32_store_8(vm, mem_arg):
    val = vm.pop_u32()
    write_u8(vm, mem_arg, uint8(val))


def i32_store_16(vm, mem_arg):
    val = vm.pop_u32()
    write_u16(vm, mem_arg, uint16(val))


def i64_store_8(vm, mem_arg):
    val = vm.pop_u64()
    write_u8(vm, mem_arg, uint8(val))


def i64_store_16(vm, mem_arg):
    val = vm.pop_u64()
    write_u16(vm, mem_arg, uint16(val))


def i64_store_32(vm, mem_arg):
    val = vm.pop_u64()
    write_u32(vm, mem_arg, uint32(val))


def write_u8(vm, mem_arg, n):
    buf = [n]
    offset = get_offset(vm, mem_arg)
    vm.memory.write(offset, buf)


def write_u16(vm, mem_arg, n):
    buf = int.to_bytes(n, 2, byteorder='little')
    buf = list(buf)
    offset = get_offset(vm, mem_arg)
    vm.memory.write(offset, buf)


def write_u32(vm, mem_arg, n):
    buf = int.to_bytes(n, 4, byteorder='little')
    buf = list(buf)
    offset = get_offset(vm, mem_arg)
    vm.memory.write(offset, buf)


def write_u64(vm, mem_arg, n):
    buf = int.to_bytes(n, 8, byteorder='little')
    buf = list(buf)
    offset = get_offset(vm, mem_arg)
    vm.memory.write(offset, buf)


def get_offset(vm, mem_arg):
    offset = mem_arg.offset
    return uint64(vm.pop_u32()) + uint64(offset)
