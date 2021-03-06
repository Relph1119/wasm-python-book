#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: Main.py
@time: 2020/8/18 16:23
@desc: 主函数
"""
import os
from optparse import OptionParser

from ch10 import binary
from ch10.cmd.dumper import dump
from ch10.cmd.native import new_env


def main(input_args):
    # 设置传入参数
    parser = OptionParser(usage="usage:%prog [-d] filename")

    parser.add_option("-d", "--dump", action="store_true", default=False, dest="dump_flag",
                      help="dump Wasm file.")
    parser.add_option("--verbose", action="store_true", default=False, dest="verbose_flag",
                      help="enable verbose output")
    # 解析参数
    (options, args) = parser.parse_args(input_args)
    module, err = binary.decode_file(args[0])

    if err is not None:
        raise err

    if options.dump_flag:
        dump(module)
    else:
        instantiate_and_exec_main_func(module)


def instantiate_and_exec_main_func(module):
    from ch10.interpreter.vm import new

    mm = dict({"env": new_env()})
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

    file_name = os.path.join(os.path.dirname(root_path), "..\\js", "ch01_hw.wasm")
    fake_args = [file_name]
    print("main.py", *fake_args, end='\n\n')
    main(fake_args)
