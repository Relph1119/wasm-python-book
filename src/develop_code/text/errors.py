#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: errors.py
@time: 2020/8/31 10:26
@project: wasm-python-book
@desc:
"""
import platform

from antlr4 import Token


class ValidationError(Exception):
    def __init__(self, msg=""):
        self.msg = msg
        self.token = None

    @property
    def error(self):
        return self.msg

    def fill_detail(self, input):
        self.msg = get_err_detail(self.msg, self.token.symbol, input)


def new_verification_error(format_str, a=None):
    if a is None:
        return ValidationError(format_str)
    return ValidationError(msg=format_str % (tuple(a)))


class SemanticError(Exception):
    def __init__(self, msg=""):
        self.msg = msg
        self.token = None

    @property
    def error(self):
        return self.msg

    def fill_detail(self, input):
        self.msg = get_err_detail(self.msg, self.token.symbol, input)


def new_semantic_error(format_str, a=None):
    if a is None:
        return SemanticError(format_str)
    return SemanticError(msg=format_str % (tuple(a)))


class SyntaxError(Exception):
    def __init__(self, msg="", line=0, column=0, token=None):
        self.msg = msg
        self.line = line
        self.column = column
        self.token = token

    @property
    def error(self):
        return self.msg


class SyntaxErrors(list):
    def __init__(self):
        super().__init__()

    def fill_detail(self, input):
        for err in self:
            err.msg = get_err_detail(err.msg, err.token.symbol, input)

    @property
    def error(self):
        return '\n'.join(self)


def get_err_detail(msg, token: Token, input):
    source_name = "Obtained from string"
    if hasattr(input, "fileName"):
        source_name = input.fileName
    msg = "%s:%d:%d: error: %s" % (source_name, token.line, token.column + 1, msg)
    all_text = "%s" % input
    err_line = all_text.split("\n")[token.line - 1]
    under_line = get_under_line(token.column, token)
    if platform.system() == "Windows":
        return msg + "\r\n" + err_line + "\n" + under_line
    return msg + "\n" + err_line + "\n" + under_line


def get_under_line(column, token):
    if token is not None:
        return " " * token.column + "^" * len(token.text)
    return " " * column + "^"
