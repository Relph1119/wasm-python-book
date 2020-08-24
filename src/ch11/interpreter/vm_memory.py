#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: vm_memory.py
@time: 2020/8/21 16:01
@project: wasm-python-book
@desc: 内存实现
"""
from ch11.binary.module import PageSize, MaxPageCount
from ch11.interpreter.errors import ErrMemOutOfBounds


class Memory:
    def __init__(self, mem_type=None):
        self.type = mem_type
        # 内存初始页分配
        self.data = [0x00] * mem_type.min * PageSize

    @property
    def size(self):
        return int(len(self.data) / PageSize)

    def grow(self, n):
        old_size = self.size
        if n == 0:
            return old_size

        # 检查页数，防止超出限制
        max = self.type.max
        max_page_count = max if max > 0 else MaxPageCount
        if old_size + n > max_page_count:
            return -1

        self.data.extend([0x00] * n * PageSize)
        return old_size

    def read(self, offset, buf):
        self.check_offset(offset, len(buf))
        buf = self.data[offset:(offset + len(buf))]
        return buf

    def write(self, offset, data):
        self.check_offset(offset, len(data))
        self.data[offset:(offset + len(data))] = data

    def check_offset(self, offset, length):
        """检查边界"""
        if len(self.data) - length < offset:
            raise ErrMemOutOfBounds
