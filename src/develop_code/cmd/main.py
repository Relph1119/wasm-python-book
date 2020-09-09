#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: Main.py
@time: 2020/8/18 16:23
@desc: 主函数
"""
import glob
import os
from optparse import OptionParser

import binary
from cmd.dumper import dump
from cmd.test_env import new_test_env
from spectest import wast_tester
from text import compiler


def main(input_args):
    # 设置传入参数
    parser = OptionParser(usage="usage:%prog [option] filename")

    parser.add_option("-d", "--dump", action="store_true", default=False, dest="dump_flag",
                      help="dump .wasm file.")
    parser.add_option("-c", "--check", action="store_true", default=False, dest="check_flag",
                      help="check .wasm file.")
    parser.add_option("--test-one", action="store_true", default=False, dest="test_one_file_flag",
                      help="check one .wast file.")
    parser.add_option("-t", "--test-all", action="store_true", default=False, dest="test_all_file_flag",
                      help="need files path, check all .wast file.")
    # 解析参数
    (options, args) = parser.parse_args(input_args)
    file_name = args[0]

    if options.dump_flag:
        dump_wasm(file_name)
    elif options.check_flag:
        check_wasm(file_name)
    elif options.test_one_file_flag:
        test_wast(file_name)
    elif options.test_all_file_flag:
        test_wast_files(args[0])
    else:
        exec_wasm(file_name)


def dump_wasm(file_name):
    print("file: \n  %s\n" % file_name)
    module, err = binary.decode_file(file_name)

    if err is not None:
        raise err

    dump(module)
    return None


def test_wast(file_name):
    print("test " + file_name)
    s, err = compiler.compile_script_file(file_name)
    if err is not None:
        return err
    else:
        return wast_tester.test_wast(s)


def test_wast_files(path):
    wast_files = glob.glob(os.path.join(path, "*.wast"))
    for file in wast_files:
        test_wast(file)


def check_wasm(file_name):
    from validator.module_validator import validate
    module, err = binary.decode_file(file_name)

    err = validate(module)
    if err is not None:
        # 打印异常信息
        print(*err.args)
        raise err
    print("Check OK!")


def exec_wasm(file_name):
    from interpreter.vm import new
    module, err = binary.decode_file(file_name)

    mm = dict({"env": new_test_env()})
    m, err = new(module, mm)
    if err is None:
        _, err = m.invoke_func("main")
    if err is not None:
        raise err


if __name__ == '__main__':
    # 打印帮助
    # fake_args = ['-h']
    # main(fake_args)

    # 使用输入参数测试
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

    # check
    # file_name = os.path.join(os.path.dirname(root_path), "..\\js", "ch01_hw.wasm")
    # fake_args = ["-c", file_name]

    # test_one_files
    test_wast_file_path = os.path.join(os.path.dirname(os.path.dirname(root_path)),
                                       "spec", "test", "core", "table.wast")
    fake_args = ['--test-one', test_wast_file_path]

    # test_all_files
    # test_wast_file_dir = os.path.join(os.path.dirname(os.path.dirname(root_path)), "spec", "test", "core")
    # fake_args = ['-t', test_wast_file_dir]
    print("main.py", *fake_args, end='\n\n')
    main(fake_args)
