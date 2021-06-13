# encoding=utf-8
from enum import Enum


# 《MySQL技术内幕(InnoDB存储引擎)》- 4.4.1 File Header
#  源码地址：mysql-8.0.25/storage/innobase/include/page0types.h
#  分析的文件 链接: https://pan.baidu.com/s/1LXm56c7QqfIkJNJqu38A_A  密码: 8ckc

class FileHeader(Enum):
    # Field为名称，Value为(开始位置，偏移量)，偏移量可以认为是所占空间大小
    FIL_PAGE_SPACE_OR_CHECKSUM = (0, 4)  # 页的checksum值
    FIL_PAGE_OFFSET = (4, 4)  # 表空间中的页偏移值
    FIL_PAGE_PREV = (8, 4)  # 当前页的上一页
    FIL_PAGE_NEXT = (12, 4)  # 当前页的下一页
    FIL_PAGE_LSN = (16, 8)  # 代表该页最后被修改的日志序列位置
    FIL_PAGE_TYPE = (24, 2)  # InnoDB页的类型 0x45BF为B+树叶节点
    FIL_PAGE_FILE_FLUSH_LSN = (26, 8)  # 对于独立的表空间，为0
    FIL_PAGE_ARCH_LOG_NO_OR_SPACE = (34, 4)  # 代表页属于哪个表空间


'''
xxd -s 65536 -l 38 person.ibd

00010000: 182b fa85 0000 0004 ffff ffff ffff ffff  .+..............
00010010: 0000 0001 3ea3 2b38 45bf 0000 0000 0000  ....>.+8E.......
00010020: 0000 0000 04

FIL_PAGE_SPACE_OR_CHECKSUM = 182b fa85  - 数据页的Checksum值
FIL_PAGE_OFFSET = 0000 0004  - 页的偏移量，第4页
FIL_PAGE_PREV = ffff ffff  - 前一页，没有页，所以为ffff ffff
FIL_PAGE_NEXT = ffff ffff  - 后一页，没有页，所以为ffff ffff
FIL_PAGE_LSN = 0000 0001 3ea3 2b38 - 页的LSN
FIL_PAGE_TYPE = 45bf  - 代表为B+树节点
FIL_PAGE_TYPE = 0000 0000 0000 0000  - 该页最后被修改的日志序列位置
FIL_PAGE_ARCH_LOG_NO_OR_SPACE = 00 0000 04  - 表空间的SPACE ID
'''


class PageHeader(Enum):
    PAGE_N_DIR_SLOTS = (38, 2)  # 页目录中槽的数量
    PAGE_HEAP_TOP = (40, 2)  # 堆中第一个记录的指针
    PAGE_N_HEAP = (42, 2)  # 堆中的记录数
    PAGE_FREE = (44, 2)  # 指向可重用空间的首指针
    PAGE_GARBAGE = (46, 2)  # 已删除记录的字节数，行记录deleted_flag为1的记录大小的总数
    PAGE_LAST_INSERT = (48, 2)  # 最后记录插入的位置
    PAGE_DIRECTION = (50, 2)  # 最后插入的方向
    PAGE_N_DIRECTION = (52, 2)  # 一个方向连续插入记录的数量
    PAGE_N_RECS = (54, 2)  # 该页中记录的数量
    PAGE_MAX_TRX_ID = (56, 8)  # 修改当前页的最大事务，只在Secondary Index中定义
    PAGE_LEVEL = (64, 2)  # 当前页在索引树的位置
    PAGE_INDEX_ID = (66, 8)  # 索引ID，当前页属于哪个索引
    PAGE_BTR_SEG_LEAF = (74, 10)  # B+树数据页非叶子节点所在段的segment header
    PAGE_BTR_SEG_TOP = (84, 10)  # B+树数据页叶子节点所在段的segment header


'''
xxd -s 65574 -l 56  person.ibd

00010026: 000c 02c1 802f 0000 0000 02b9 0002 002c  ...../.........,
00010036: 002d 0000 0000 0000 0000 0002 0000 0000  .-..............
00010046: 0000 0adf 0000 04d9 0000 0002 0272 0000  .............r..
00010056: 04d9 0000 0002 01b2                      ........

PAGE_N_DIR_SLOTS = 000c  - 槽的数量，13个，每个槽占两个字节
PAGE_HEAP_TOP = 02c1 - 代表空闲空间开间位置的偏移量， 00010000 + 02c1 = 102C1，代表102C1的位置是空闲空间开始的位置
PAGE_N_HEAP = 802f  - 我这里默认格式为Dynamic，初始值为8002
PAGE_FREE = 0000  - 代表可重用的空间首地址，因为这里没有进行过任何删除操作
PAGE_GARBAGE = 0000  - 代表删除的记录字节为0，因为这里没有进行过删除
PAGE_LAST_INSERT = 02b9  - 最后插入的记录
PAGE_DIRECTION = 0002  - 最后插入的方向，代表PAGE_RIGHT
PAGE_N_DIRECTION = 002c  - 代表连续向这个方向插入记录的数量
PAGE_N_RECS = 002d  - 代表这个页有45条记录
PAGE_MAX_TRX_ID = 0000 0000 0000 0000  - 最大事务ID
PAGE_LEVEL = 0002  - 代表树的层数，PAGE_LEVEL + 1 = 3层，因为PAGE_LEVEL是从0开始算的，0是叶子节点
PAGE_INDEX_ID =  0000 0000 0000 0adf  - 表示索引ID
PAGE_BTR_SEG_LEAF = 0000 04d9 0000 0002 0272
PAGE_BTR_SEG_TOP = 0000 04d9 0000 0002 01b2
'''


class VirtualRecord(Enum):
    PAGE_INFIMUM = (94, 13)  # 记录了该页中主键值最小的值
    PAGE_SUPREMUM = (107, 13)  #

'''
xxd -s 65630 -l 26  person.ibd

0001005e: 0100 0200 1a69 6e66 696d 756d 00  .....infimum.  0100 0200
0001006e: 06 000b 0000 7375 7072 656d 756d  .....supremum

Infimum: 0100 0200 1a  - 记录头，最后两个字节1a表示下一条记录位置的偏移量, 0x1005e + 0x5 + 0x1a = 0x1007D = 65661
69 6e66 696d 756d 00 - 内容就是infimum，看后面ascii码也能看出啦

Supremum: 06 000b 0000 - 记录头，解释可看下面
7375 7072 656d 756d  - 内容就是supremum
'''


'''
由Infimum上面可知第一条记录的位置，但是我还想看看它的记录头，所以要向前偏移5个字节
xxd -s 65656 -l 100  person.ibd

00010078: 1000 1100 0d00 0000 0100 0000 2500 0019  ............%...
00010088: 000d 0004 ba63 0000 0026 0000 2100 0d00  .....c...&..!...
00010098: 0e33 2f00 0000 2704 0029 000d 0017 abfb  .3/...'..)......
000100a8: 0000 0028 0000 3100 0d00 2124 c700 0000  ...(..1...!$....
000100b8: 2900 0039 000d 002a 9d93 0000 002a 0000  )..9...*.....*..
000100c8: 4100 0d00 3416 5f00 0000 2b04 0049 000d  A...4._...+..I..
000100d8: 003d 8f2b                                .=.+

第一个字节 10  代表 00010000， 代表deleted_flag为0， min_rec_flag为1，n_owned为0
第二个和第三个字节要一起看，001100 - 0000000000010001 前十三位代表heap_no，为2，后三位代表记录的类型，001表示B+树节点指针
最后两个字节表示下一条记录的相对位置，0d - 13， 这个13是没有算上记录头的
                                从0d开始到下一条记录要偏移0d，所以这条记录的数据 + 下条数据的记录头 = 13，那么可知数据占 13 - 5 = 8个字节
                                又因为我定义的主键int占4个类型，所以页的偏移量占4个字节
00 00 00 01 为主键值，1
00 00 00 25 为页偏移量 接下来的数据都可以按照这个来分析
'''


def get_start(e: Enum) -> int:
    return e.value[0]


def get_offset(e: Enum) -> int:
    return e.value[1]
