#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: error_listener.py
@time: 2020/8/31 10:10
@project: wasm-python-book
@desc:
"""
from antlr4.error.ErrorListener import ErrorListener

from text.errors import SyntaxErrors, SyntaxError


class TextErrorListener(ErrorListener):
    def __init__(self):
        super().__init__()
        self.errors = SyntaxErrors()
        self.all_text = []

    def get_errors(self, input):
        if len(self.errors) > 0:
            errs = self.errors
            errs.fill_detail(input)
            return errs
        else:
            return None

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        err = SyntaxError(msg=msg,
                          line=line,
                          column=column,
                          token=offendingSymbol)
        self.errors.append(err)
