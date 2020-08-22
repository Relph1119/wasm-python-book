#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: module.py
@time: 2020/8/18 16:50
@project: wasm-python-book
@desc: Wasm模块定义
"""

# 小端方式编码数值，魔数：0asm
from ch06.binary.types import BlockTypeI32, BlockTypeI64, BlockTypeF32, BlockTypeF64, BlockTypeEmpty, FuncType, ValTypeI32, \
    ValTypeI64, ValTypeF32, ValTypeF64

MagicNumber = 0x6D736100
# 版本号：1
Version = 0x00000001

# 12种段
# 自定义段ID
SecCustomID = 0
# 类型段ID
SecTypeID = 1
# 导入段ID
SecImportID = 2
# 函数段ID
SecFuncID = 3
# 表段ID
SecTableID = 4
# 内存段ID
SecMemID = 5
# 全局段ID
SecGlobalID = 6
# 导出段ID
SecExportID = 7
# 起始段ID
SecStartID = 8
# 元素段ID
SecElemID = 9
# 代码段ID
SecCodeID = 10
# 数据段ID
SecDataID = 11

ImportTagFunc = 0
ImportTagTable = 1
ImportTagMem = 2
ImportTagGlobal = 3

ExportTagFunc = 0
ExportTagTable = 1
ExportTagMem = 2
ExportTagGlobal = 3

# 内存页大小
PageSize = 65536  # 64KB
# 最大内存页数
MaxPageCount = 65536  # 2^16

# 索引空间
# 类型索引：类型段的有效索引范围就是类型索引空间
TypeIdx = int
# 函数索引：由外部函数和内部函数共同构成
FuncIdx = int
# 表和内存索引：只能导入或定义一份表和内存，所以索引空间内的唯一有效索引为0
TableIdx = int
MemIdx = int
# 全局变量索引：由外部和内部全局变量共同构成
GlobalIdx = int
# 局部变量索引：由函数的参数和局部变量共同构成
LocalIdx = int
# 跳转标签索引：每个函数有自己的跳转标签索引空间
LabelIdx = int


class Module:
    """模型"""

    def __init__(self):
        # 魔数
        self.magic = 0
        # 版本号
        self.version = 0
        # 自定义段 0
        # custom_sec: 0x00|byte_count|name|byte*
        self.custom_secs = []
        # 类型段 1
        # type_sec: 0x01|byte_count|vec<func_type>
        self.type_sec = []
        # 导入段 2
        # import_sec : 0x02|byte_count|vec<import>
        self.import_sec = []
        # 函数段 3
        # func_sec: 0x03|byte_count|vec<type_idx>
        self.func_sec = []
        # 表段 4
        # table_sec : 0x04|byte_count|vec<table_type>
        self.table_sec = []
        # 内存段 5
        # mem_sec : 0x05|byte_count|vec<mem_type> 目前vec长度只能是1
        self.mem_sec = []
        # 全局段 6
        # global_sec : 0x06|byte_count|vec<global>
        self.global_sec = []
        # 导出段 7
        # export_sec : 0x07|byte_count|vec<export>
        self.export_sec = []
        # 起始段 8
        # start_sec: 0x08|byte_count|func_idx
        self.start_sec = None
        # 元素段 9
        # elem_sec: 0x09|byte_count|vec<elem>
        self.elem_sec = []
        # 代码段 10
        # code_sec: 0x0A|byte_count|vec<code>
        self.code_sec = []
        # 数据段 11
        # data_sec: 0x0B|byte_count|vec<data>
        self.data_sec = []

    def get_block_type(self, bt):
        if bt == BlockTypeI32:
            return FuncType(result_types=[ValTypeI32])
        elif bt == BlockTypeI64:
            return FuncType(result_types=[ValTypeI64])
        elif bt == BlockTypeF32:
            return FuncType(result_types=[ValTypeF32])
        elif bt == BlockTypeF64:
            return FuncType(result_types=[ValTypeF64])
        elif bt == BlockTypeEmpty:
            return FuncType()
        else:
            return self.type_sec[bt]


class CustomSec:
    """自定义段"""

    def __init__(self, name="", custom_sec_bytes=None):
        if custom_sec_bytes is None:
            custom_sec_bytes = []
        self.name = name
        self.bytes = custom_sec_bytes


class Import:
    """
    导入类型：函数、表、内存、全局变量
    import     : module_name|member_name|import_desc
    """

    def __init__(self, module="", name="", desc=None):
        # 模块名（从哪个模块导入）
        self.module = module
        # 成员名
        self.name = name
        # 具体描述信息
        self.desc = desc


class ImportDesc:
    """
    import_desc: tag|[type_idx, table_type, mem_type, global_type]
    """

    def __init__(self, tag):
        # 0表示函数、1表示表、2表示内存、3表示全局变量
        self.tag = tag
        self.func_type = TypeIdx
        self.table = None
        self.mem = None
        self.global_type = None


class Global:
    """
    global     : global_type|init_expr
    """

    def __init__(self, global_type=None, init=None):
        self.type = global_type
        self.init = init


class Export:
    """
    export     : name|export_desc
    """

    def __init__(self, name="", export_desc=None):
        self.name = name
        self.desc = export_desc


class ExportDesc:
    """
    export_desc: tag|[func_idx, table_idx, mem_idx, global_idx]
    """

    def __init__(self, tag=0, idx=0):
        self.tag = tag
        self.idx = idx


class Elem:
    """
    elem    : table_idx|offset_expr|vec<func_idx>
    """

    def __init__(self, table_idx=0, offset_expr=None, vec_init=None):
        if vec_init is None:
            vec_init = []
        self.table = table_idx
        self.offset = offset_expr
        self.init = vec_init


class Code:
    """
    code    : byte_count|vec<locals>|expr
    """

    def __init__(self, locals_vec=None, expr=None):
        if locals_vec is None:
            locals_vec = []
        self.locals = locals_vec
        self.expr = expr

    def get_local_count(self) -> int:
        n = 0
        for locals_item in self.locals:
            n += locals_item.n
        return n


class Locals:
    """
    locals  : local_count|val_type
    """

    def __init__(self, local_count=0, val_type=0):
        self.n = local_count
        self.type = val_type


class Data:
    """
    data    : mem_idx|offset_expr|vec<byte>
    """

    def __init__(self, mem_idx=0, offset_expr=None, vec_init=None):
        if vec_init is None:
            vec_init = []
        self.mem = mem_idx
        self.offset = offset_expr
        self.init = vec_init
