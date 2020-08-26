#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: convert_to_wasm.py
@time: 2020/8/25 17:14
@project: wasm-python-book
@desc: 转换成wasm文件
"""
import glob
import os
import sys

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

input_dir = os.path.join(os.path.dirname(os.path.dirname(root_path)), "spec", "test", "core")
wast_files = glob.glob(os.path.join(input_dir, "*.wast"))

output_dir = os.path.join(input_dir, "output")

if not os.path.exists(output_dir):
    os.mkdir(output_dir)

for file in wast_files:
    os.system()