#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: compiler.py
@time: 2020/8/27 11:11
@project: wasm-python-book
@desc:
"""
from antlr4 import FileStream, CommonTokenStream

from text.error_listener import TextErrorListener
from text.parser.WASTLexer import WASTLexer
from text.parser.WASTParser import WASTParser
from text.visitor_wast import new_wast_visitor


def compile_script_file(file_name):
    err = None
    try:
        input = FileStream(file_name, encoding='utf8')
    except Exception as e:
        err = e
        return None, err
    return compile_script(input), err


def compile_script(input):
    err_listener = TextErrorListener()
    p = new_parser(input, err_listener)
    ctx = p.script()
    err = err_listener.get_errors(input)
    if err is not None:
        return None, err
    else:
        s = ctx.accept(new_wast_visitor())
        return s, err


def new_parser(input, err_listener):
    lexer = WASTLexer(input)
    stream = CommonTokenStream(lexer, 0)
    p = WASTParser(stream)
    p.removeErrorListeners()
    p.addErrorListener(err_listener)
    p.buildParseTrees = True
    return p
