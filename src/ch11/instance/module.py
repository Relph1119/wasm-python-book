#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: module.py
@time: 2020/8/23 19:43
@project: wasm-python-book
@desc: 模块实例
"""
from abc import ABCMeta, abstractmethod


class Module(metaclass=ABCMeta):
    @abstractmethod
    def get_member(self, name):
        pass

    @abstractmethod
    def invoke_func(self, name, args):
        pass

    @abstractmethod
    def get_global_val(self, name):
        pass

    @abstractmethod
    def set_global_var(self, name, val):
        pass


class Function(metaclass=ABCMeta):
    @abstractmethod
    def call(self, args):
        pass


class Table(metaclass=ABCMeta):
    @abstractmethod
    def size(self):
        pass

    @abstractmethod
    def grow(self, n):
        pass

    @abstractmethod
    def get_elem(self, idx):
        pass

    @abstractmethod
    def set_elem(self, idx, elem):
        pass


class Memory(metaclass=ABCMeta):
    @abstractmethod
    def size(self):
        pass

    @abstractmethod
    def grow(self, n):
        pass

    @abstractmethod
    def read(self, offset, buf):
        pass

    @abstractmethod
    def write(self, offset, buf):
        pass


class Global(metaclass=ABCMeta):
    @abstractmethod
    def get_as_u64(self):
        pass

    @abstractmethod
    def set_as_u64(self, val):
        pass

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def set(self, val):
        pass
