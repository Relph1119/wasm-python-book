#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: error_reporter.py
@time: 2020/8/31 18:29
@project: wasm-python-book
@desc:
"""
from antlr4 import Token, TerminalNode

from text.errors import SemanticError, ValidationError
from text.parser.WASTParser import ParserRuleContext


class ErrorReporter:
    def __init__(self):
        self.reports_validation_error = None

    def report_err(self, err, node):
        if err is not None:
            if isinstance(err, SemanticError):
                err.token = get_token(node)
                raise err
            elif isinstance(err, ValidationError):
                err.token = get_token(node)
                if self.reports_validation_error:
                    raise err
            else:
                raise err


def get_token(node):
    if isinstance(node, Token):
        return node
    elif isinstance(node, TerminalNode):
        return node
    elif isinstance(node, ParserRuleContext):
        return get_token(node.getChild(0))
    else:
        raise Exception("TODO")
