#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: wast_tester.py
@time: 2020/8/31 11:01
@project: wasm-python-book
@desc:
"""
import math

from binary.opcodes import *
from binary.reader import decode
from interpreter import int32, int64, float32, float64
from spectest.native import new_spectest_instance
from spectest.wasm_impl import WasmImpl
from text.wast_script import *


class WastTester:
    def __init__(self, script, wasm_impl=None, instances=None):
        if instances is None:
            instances = dict()
        self.script = script
        if wasm_impl is None:
            wasm_impl = WasmImpl()
        self.wasm_impl = wasm_impl
        self.instances = instances
        self.instance = None

    def test(self):
        err = None
        for cmd in self.script.cmds:
            if isinstance(cmd, WatModule):
                err = self.instantiate(cmd)
            elif isinstance(cmd, BinaryModule):
                err = self.instantiate_bin(cmd)
            elif isinstance(cmd, QuotedModule):
                err = Exception("TODO")
            elif isinstance(cmd, Register):
                self.instances[cmd.module_name] = self.instance
            elif isinstance(cmd, Action):
                err = self.run_action(cmd)
            elif isinstance(cmd, Assertion):
                err = self.run_assertion(cmd)
            elif isinstance(cmd, Meta):
                err = Exception("TODO")
            else:
                err = Exception("unreachable")
        if err is not None:
            return err

    def instantiate(self, module):
        self.instance, err = self.wasm_impl.instantiate(module.module, self.instances)
        if err is None:
            if module.name != "":
                self.instances[module.name] = self.instance
        else:
            err = "line: %d, %s" % (module.line, err.error)
        return err

    def instantiate_bin(self, module):
        tmp, err = self.wasm_impl.instantiate_bin(module.data, self.instances)
        if err is not None:
            return err
        self.instance = tmp
        self.instances[module.name] = self.instance
        return None

    def run_assertion(self, assertion):
        kind = assertion.kind
        if kind == AssertReturn:
            results, err = self.run_action(assertion.action)
            return assert_return(assertion, results, err)
        elif kind == AssertTrap:
            if assertion.action is not None:
                results, err = self.run_action(assertion.action)
                return assert_trap(assertion, results, err)
            else:
                err = self.instantiate(assertion.module)
                return assert_trap(assertion, None, err)
        elif kind == AssertExhaustion:
            pass
        elif kind == AssertMalformed:
            module = assertion.module
            if isinstance(module, BinaryModule):
                _, err = decode(module.data)
                if assertion.failure != "length out of bounds":
                    return assert_error(assertion, err)
            elif isinstance(module, QuotedModule):
                pass
        elif kind == AssertInvalid:
            module = assertion.module
            err = self.wasm_impl.validate(module)
            return assert_error(assertion, err)
        elif kind == AssertUnlinkable:
            err = self.instantiate(assertion.module)
            return assert_error(assertion, err)
        else:
            err = Exception("unreachable")
            raise err
        return None

    def run_action(self, action):
        _i = self.instance
        if action.module_name != "":
            _i = self.instances[action.module_name]

        kind = action.kind
        if kind == ActionInvoke:
            return _i.invoke_func(action.item_name, get_consts(action.expr))
        elif kind == ActionGet:
            val, err = _i.get_global_val(action.item_name)
            return [val], err
        else:
            err = Exception("unreachable")
            raise err


def assert_return(assertion, results, err):
    expected_vals = get_consts(assertion.result)
    if err is not None:
        return "line: {}, expected return: {}, got: {}".format(assertion.line,
                                                               expected_vals,
                                                               err)
    if len(results) != len(expected_vals):
        return "line: {}, expected return: {}, got: {}".format(assertion.line,
                                                               expected_vals,
                                                               results)

    for i, result in enumerate(results):
        expected_val = expected_vals[i]
        if math.isnan(expected_val):
            if not math.isnan(result):
                return "line: {}, expected return: NaN, got: {}".format(assertion.line,
                                                                        result)
        elif result != expected_val:
            return "line: {}, expected return: {}, got: {}".format(assertion.line,
                                                                   expected_val,
                                                                   result)

    return None


def assert_trap(assertion, results, err):
    if err is None:
        return "line: {}, expected trap: {}, got: {}".format(assertion.line,
                                                             assertion.failure,
                                                             results)
    if err.args[0].find(assertion.failure) < 0:
        return "line: {}, expected trap: {}, got: {}".format(assertion.line,
                                                             assertion.failure,
                                                             err)
    return None


def assert_error(assertion, err):
    if err is None or err.args[0].find(assertion.failure) < 0:
        return "line: {}, expected: {}, got: {}".format(assertion.line,
                                                        assertion.failure,
                                                        err)
    return None


def get_consts(expr):
    vals = [None] * len(expr)
    for i, instr in enumerate(expr):
        opcode = instr.opcode
        if opcode == I32Const:
            vals[i] = int32(instr.args)
        elif opcode == I64Const:
            vals[i] = int64(instr.args)
        elif opcode == F32Const:
            vals[i] = float32(instr.args)
        elif opcode == F64Const:
            vals[i] = float64(instr.args)
        else:
            raise Exception("TODO")
    return vals


def test_wast(script):
    return new_wast_tester(script).test()


def new_wast_tester(script):
    return WastTester(script=script,
                      instances=dict({"spectest": new_spectest_instance()}))
