#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: reader.py
@time: 2020/8/18 22:57
@project: wasm-python-book
@desc:
"""
import ctypes
import struct

from ch08.binary.errors import ErrUnexpectedEnd
from ch08.binary.instruction import Instruction, BlockArgs, IfArgs, BrTableArgs, MemArg
from ch08.binary.leb128 import decode_var_uint, decode_var_int
from ch08.binary.module import Import, ImportDesc, ImportTagFunc, ImportTagTable, ImportTagMem, ImportTagGlobal, \
    Global, Export, ExportDesc, ExportTagFunc, ExportTagTable, ExportTagMem, ExportTagGlobal, Elem, Code, Locals, \
    Data, MagicNumber, Version, Module, SecCustomID, SecDataID, CustomSec, SecTypeID, SecImportID, SecFuncID, \
    SecTableID, SecMemID, SecGlobalID, SecExportID, SecStartID, SecElemID, SecCodeID
from ch08.binary.opcodes import *
from ch08.binary.opnames import opnames
from ch08.binary.types import ValTypeI32, ValTypeI64, ValTypeF32, ValTypeF64, FuncType, FtTag, TableType, FuncRef, \
    GlobalType, MutConst, MutVar, Limits, BlockTypeI32, BlockTypeI64, BlockTypeF32, BlockTypeF64, BlockTypeEmpty


def decode_file(file_name: str):
    data, err = None, None
    try:
        with open(file_name, 'rb') as f:
            data = f.read()
    except Exception as e:
        err = e

    if err is not None:
        return Module(), err

    return decode(data)


def decode(data):
    module, err = None, None
    try:
        module = Module()
        reader = WasmReader(data)
        reader.read_module(module)
    except Exception as e:
        err = e
    return module, err


class WasmReader:
    """
    用于封装二进制模块解码逻辑
    """

    def __init__(self, data=None):
        # 存放Wasm二进制模块的数据
        if data is None:
            data = []
        self.data = data

    def remaining(self):
        """查看剩余的字节数量"""
        return len(self.data)

    def read_byte(self):
        """读取字节"""
        if len(self.data) < 1:
            raise ErrUnexpectedEnd
        b = self.data[:1]
        self.data = self.data[1:]
        return b[0]

    def read_u32(self):
        """读取32位整数"""
        if len(self.data) < 4:
            raise ErrUnexpectedEnd
        b = int.from_bytes(self.data[:4], byteorder='little')
        self.data = self.data[4:]
        return ctypes.c_int32(b).value

    def read_f32(self):
        """读取32位浮点数"""
        if len(self.data) < 4:
            raise ErrUnexpectedEnd
        b = int.from_bytes(self.data[:4], byteorder='little')
        self.data = self.data[4:]
        return struct.unpack('>f', struct.pack('>L', b))[0]

    def read_f64(self):
        """读取64位浮点数"""
        if len(self.data) < 8:
            raise ErrUnexpectedEnd
        b = int.from_bytes(self.data[:8], byteorder='little')
        self.data = self.data[8:]
        return struct.unpack('>d', struct.pack('>Q', b))[0]

    def read_var_u32(self):
        """
        读取无符号32位整数，用来编码索引和向量长度
        """
        n, w = decode_var_uint(self.data, 32)
        self.data = self.data[w:]
        return n

    def read_var_s32(self):
        """读取有符号32位整数"""
        n, w = decode_var_int(self.data, 32)
        self.data = self.data[w:]
        return n

    def read_var_s64(self):
        """读取有符号64位整数"""
        n, w = decode_var_int(self.data, 64)
        self.data = self.data[w:]
        return n

    def read_bytes(self):
        """读取字节向量"""
        n = self.read_var_u32()
        if len(self.data) < int(n):
            raise ErrUnexpectedEnd
        bytes_data = self.data[:n]
        self.data = self.data[n:]
        return bytearray(bytes_data)

    def read_name(self):
        """读取名字"""
        data = self.read_bytes()
        try:
            data.decode('utf-8')
        except Exception:
            raise Exception("malformed UTF-8 encoding")

        return str(data, 'utf-8')

    def read_module(self, module: Module):
        if self.remaining() < 4:
            raise Exception("unexpected end of magic header")

        # 读取魔数
        module.magic = self.read_u32()
        if module.magic != MagicNumber:
            raise Exception("magic header not detected")
        if self.remaining() < 4:
            raise Exception("unexpected end of binary version")

        # 读取版本号
        module.version = self.read_u32()
        if module.version != Version:
            raise Exception("unknown binary version: %d" % module.version)

        # 读取段
        self.read_sections(module)
        if len(module.func_sec) != len(module.code_sec):
            raise Exception("function and code section have inconsistent lengths")
        if self.remaining() > 0:
            raise Exception("junk after last section")

    def read_sections(self, module: Module):
        prev_sec_id = 0
        while self.remaining() > 0:
            sec_id = self.read_byte()
            if sec_id == SecCustomID:
                if module.custom_secs is None:
                    module.custom_secs = []
                module.custom_secs.append(self.read_custom_sec())
                continue

            if sec_id > SecDataID:
                raise Exception("malformed section id: %d" % sec_id)

            if sec_id <= prev_sec_id:
                raise Exception("junk after last section, id: %d" % sec_id)
            prev_sec_id = sec_id

            n = self.read_var_u32()
            remaining_before_read = self.remaining()
            self.read_non_custom_sec(sec_id, module)
            if self.remaining() + int(n) != remaining_before_read:
                raise Exception("section size mismatch, id: %d" % sec_id)

    def read_custom_sec(self):
        sec_reader = WasmReader(data=self.read_bytes())
        return CustomSec(name=sec_reader.read_name(), custom_sec_bytes=sec_reader.data)

    def read_non_custom_sec(self, sec_id, module):
        if sec_id == SecTypeID:
            module.type_sec = self.read_type_sec()
        elif sec_id == SecImportID:
            module.import_sec = self.read_import_sec()
        elif sec_id == SecFuncID:
            module.func_sec = self.read_indices()
        elif sec_id == SecTableID:
            module.table_sec = self.read_table_sec()
        elif sec_id == SecMemID:
            module.mem_sec = self.read_mem_sec()
        elif sec_id == SecGlobalID:
            module.global_sec = self.read_global_sec()
        elif sec_id == SecExportID:
            module.export_sec = self.read_export_sec()
        elif sec_id == SecStartID:
            module.start_sec = self.read_start_sec()
        elif sec_id == SecElemID:
            module.elem_sec = self.read_elem_sec()
        elif sec_id == SecCodeID:
            module.code_sec = self.read_code_sec()
        elif sec_id == SecDataID:
            module.data_sec = self.read_data_sec()

    def read_type_sec(self):
        """读取类型段"""
        vec = []
        for _ in range(self.read_var_u32()):
            vec.append(self.read_func_type())
        return vec

    def read_import_sec(self):
        """读取导入段"""
        vec = []
        for _ in range(self.read_var_u32()):
            vec.append(self.read_import())
        return vec

    def read_import(self):
        return Import(self.read_name(), self.read_name(), self.read_import_desc())

    def read_import_desc(self):
        desc = ImportDesc(self.read_byte())
        tag = desc.tag
        if tag == ImportTagFunc:
            desc.func_type = self.read_var_u32()
        elif tag == ImportTagTable:
            desc.table = self.read_table_type()
        elif tag == ImportTagMem:
            desc.mem = self.read_limits()
        elif tag == ImportTagGlobal:
            desc.global_type = self.read_global_type()
        else:
            raise Exception("invalid import desc tag: %d" % tag)
        return desc

    def read_table_sec(self):
        """读取表段"""
        vec = []
        for _ in range(self.read_var_u32()):
            vec.append(self.read_table_type())
        return vec

    def read_mem_sec(self):
        """读取内存段"""
        vec = []
        for _ in range(self.read_var_u32()):
            vec.append(self.read_limits())
        return vec

    def read_global_sec(self):
        """读取全局段"""
        vec = []
        for _ in range(self.read_var_u32()):
            global_obj = Global(self.read_global_type(), self.read_expr())
            vec.append(global_obj)
        return vec

    def read_export_sec(self):
        """读取导出段"""
        vec = []
        for _ in range(self.read_var_u32()):
            vec.append(self.read_export())
        return vec

    def read_export(self):
        return Export(self.read_name(), self.read_export_desc())

    def read_export_desc(self):
        desc = ExportDesc(tag=self.read_byte(), idx=self.read_var_u32())
        tag = desc.tag
        if tag not in [ExportTagFunc, ExportTagTable, ExportTagMem, ExportTagGlobal]:
            raise Exception("invalid export desc tag: %d" % tag)
        return desc

    def read_start_sec(self):
        """读取起始段"""
        idx = self.read_var_u32()
        return idx

    def read_elem_sec(self):
        """读取元素段"""
        vec = []
        for _ in range(self.read_var_u32()):
            vec.append(self.read_elem())
        return vec

    def read_elem(self):
        return Elem(self.read_var_u32(), self.read_expr(), self.read_indices())

    def read_code_sec(self):
        """读取代码段"""
        vec = [Code()] * self.read_var_u32()
        for i in range(len(vec)):
            vec[i] = self.read_code(i)
        return vec

    def read_code(self, idx):
        n = self.read_var_u32()
        remaining_before_read = self.remaining()
        code = Code(self.read_locals_vec(), self.read_expr())
        if self.remaining() + int(n) != remaining_before_read:
            print("invalid code[%d]" % idx)
        if code.get_local_count() >= (1 << 32 - 1):
            raise Exception("too many locals: %d" % code.get_local_count())
        return code

    def read_locals_vec(self):
        vec = []
        for _ in range(self.read_var_u32()):
            vec.append(self.read_locals())
        return vec

    def read_locals(self):
        return Locals(self.read_var_u32(), self.read_val_type())

    def read_data_sec(self):
        """读取数据段"""
        vec = []
        for _ in range(self.read_var_u32()):
            vec.append(self.read_data())
        return vec

    def read_data(self):
        return Data(self.read_var_u32(), self.read_expr(), self.read_bytes())

    def read_val_types(self):
        vec = []
        for _ in range(self.read_var_u32()):
            vec.append(self.read_val_type())
        return vec

    def read_val_type(self):
        vt = self.read_byte()
        if vt not in [ValTypeI32, ValTypeI64, ValTypeF32, ValTypeF64]:
            raise Exception("malformed value type: %d" % vt)
        return vt

    def read_block_type(self):
        bt = self.read_var_s32()
        if bt < 0:
            if bt not in [BlockTypeI32, BlockTypeI64, BlockTypeF32, BlockTypeF64, BlockTypeEmpty]:
                raise Exception("malformed block type: %d" % bt)

        return bt

    def read_func_type(self):
        ft = FuncType(self.read_byte(), self.read_val_types(), self.read_val_types())
        if ft.tag != FtTag:
            raise Exception("invalid functype tag: %d" % ft.tag)
        return ft

    def read_table_type(self):
        tt = TableType(self.read_byte(), self.read_limits())
        if tt.elem_type != FuncRef:
            raise Exception("invalid elemtype: %d" % tt.elem_type)
        return tt

    def read_global_type(self):
        gt = GlobalType(self.read_val_type(), self.read_byte())
        if gt.mut not in [MutConst, MutVar]:
            raise Exception("malformed mutability: %d" % gt.mut)
        return gt

    def read_limits(self):
        limits = Limits(self.read_byte(), self.read_var_u32())
        if limits.tag == 1:
            limits.max = self.read_var_u32()
        return limits

    def read_indices(self):
        vec = []
        for _ in range(self.read_var_u32()):
            vec.append(self.read_var_u32())
        return vec

    def read_expr(self):
        instrs, end = self.read_instructions()
        if end != End_:
            raise Exception("invalid expr end: %d" % end)
        return instrs

    def read_instructions(self):
        """
        读取并收集指令，直到遇到else或者end指令为止
        :return:
        """
        instrs = []
        while True:
            instr = self.read_instruction()
            if instr.opcode == Else_ or instr.opcode == End_:
                end = instr.opcode
                return instrs, end
            instrs.append(instr)

    def read_instruction(self):
        """
        先读取操作码，然后根据操作码读取立即数
        :return:
        """
        instr = Instruction()
        instr.opcode = self.read_byte()
        if opnames[instr.opcode] == "":
            raise Exception("undefined opcode: 0x%02x" % instr.opcode)

        instr.args = self.read_args(instr.opcode)
        return instr

    def read_args(self, opcode):
        if opcode in [Block, Loop]:
            return self.read_block_args()
        elif opcode == If:
            return self.read_if_args()
        elif opcode in [Br, BrIf]:
            return self.read_var_u32()
        elif opcode == BrTable:
            return self.read_br_table_args()
        elif opcode == Call:
            return self.read_var_u32()
        elif opcode == CallIndirect:
            return self.read_call_indirect_args()
        elif opcode in [LocalGet, LocalSet, LocalTee]:
            return self.read_var_u32()
        elif opcode in [GlobalGet, GlobalSet]:
            return self.read_var_u32()
        elif opcode in [MemorySize, MemoryGrow]:
            return self.read_zero()
        elif opcode == I32Const:
            return self.read_var_s32()
        elif opcode == I64Const:
            return self.read_var_s64()
        elif opcode == F32Const:
            return self.read_f32()
        elif opcode == F64Const:
            return self.read_f64()
        elif opcode == TruncSat:
            return self.read_byte()
        else:
            if I32Load <= opcode <= I64Store32:
                return self.read_mem_arg()
            return None

    def read_block_args(self):
        """读取block参数"""
        args = BlockArgs()
        args.bt = self.read_block_type()
        args.instrs, end = self.read_instructions()
        if end != End_:
            raise Exception("invalid block end: %d" % end)
        return args

    def read_if_args(self):
        """读取if参数"""
        args = IfArgs()
        args.bt = self.read_block_type()
        args.instrs1, end = self.read_instructions()
        if end == Else_:
            args.instrs2, end = self.read_instructions()
            if end != End_:
                raise Exception("invalid block end: %d" % end)
        return args

    def read_br_table_args(self):
        """读取br_table参数"""
        return BrTableArgs(self.read_indices(), self.read_var_u32())

    def read_call_indirect_args(self):
        """读取call indirect参数"""
        type_idx = self.read_var_u32()
        self.read_zero()
        return type_idx

    def read_mem_arg(self):
        """读取内存的参数"""
        return MemArg(self.read_var_u32(), self.read_var_u32())

    def read_zero(self):
        b = self.read_byte()
        if b != 0:
            raise Exception("zero flag expected, got %d" % b)
        return 0
