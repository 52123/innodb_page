from enum import Enum

# class Context:
#     def __int__(self, page, enums, num=-1):
#         self.page = page
#         self.enums = enums
#         self.num = -1


# class Strategy(str, Context):
#     def __init__(self, name: str, context: Context):
#         super().__init__()
#         if name == "default":
#             DefaultPrint(context)
#
#
#
# class DefaultPrint(Context):
#     def __init__(self, context: Context):
#         self.context = context

print_level_enable = True


def print_tree_level(page, page_type: Enum, page_level: Enum):
    global print_level_enable
    (page_type_start, page_type_offset) = page_type.value
    page_type_hex = page[page_type_start: page_type_start + page_type_offset].hex()
    if page_type_hex == '45bf' and print_level_enable:
        (page_level_start, page_level_offset) = page_level.value
        page_level_num = int(page[page_level_start:page_level_start + page_type_offset].hex(), 16)
        print("该B+树的高度为%d" % (page_level_num + 1))
        print_level_enable = False


idx_slot_num = 0
record_slot_num = 0

def count_tree_slot(page, page_type: Enum, num_enum: Enum, supremum_enum: Enum):
    global idx_slot_num,record_slot_num
    # 如果该页是数据页，45bf
    (page_type_start, page_type_offset) = page_type.value
    page_type_hex = page[page_type_start: page_type_start + page_type_offset].hex()
    if page_type_hex == '45bf':
        # 该页有多少记录
        (num_start, num_offset) = num_enum.value
        data_num = int(page[num_start: num_start + num_offset].hex(), 16)

        # 因为supremum紧接这的5个字节就是数据的记录头，记录头的第二个字节能区分是数据是索引还是行数据记录
        (supremum_start, supremum_offset) = supremum_enum.value
        record_type_begin = supremum_start + supremum_offset + 2

        # 判断该页存的是索引记录，还是行数据记录，decimal & 1为1代表节点指针，为0代表行数据记录
        decimal = int(page[record_type_begin: record_type_begin + 1].hex(), 16)
        if decimal & 1 == 1:
            idx_slot_num += data_num
        else:
            record_slot_num += data_num

def print_index_and_record_slot():
    print("所有非叶子节点的槽%d，所有叶子节点的槽%d" % (idx_slot_num, record_slot_num))


idx_page_num = 0
record_page_num = 0
idx_sum = 0
record_sum = 0


def count_the_index_and_record_num(page, page_type: Enum, num_enum: Enum, supremum_enum: Enum):
    global idx_page_num, record_page_num, idx_sum, record_sum

    # 如果该页是数据页，45bf
    (page_type_start, page_type_offset) = page_type.value
    page_type_hex = page[page_type_start: page_type_start + page_type_offset].hex()
    if page_type_hex == '45bf':
        # 该页有多少记录
        (num_start, num_offset) = num_enum.value
        data_num = int(page[num_start: num_start + num_offset].hex(), 16)

        # 因为supremum紧接这的5个字节就是数据的记录头，记录头的第二个字节能区分是数据是索引还是行数据记录
        (supremum_start, supremum_offset) = supremum_enum.value
        record_type_begin = supremum_start + supremum_offset + 2

        # 判断该页存的是索引记录，还是行数据记录，decimal & 1为1代表节点指针，为0代表行数据记录
        decimal = int(page[record_type_begin: record_type_begin + 1].hex(), 16)
        if decimal & 1 == 1:
            idx_sum += data_num
            idx_page_num += 1
        else:
            record_sum += data_num
            record_page_num += 1


def print_index_and_record_num():
    print("非叶子节点的数量为%d， 叶子节点的数量为%d" % (idx_page_num, record_page_num))
    print("索引记录的数量为%d， 行数据记录的数量为%d" % (idx_sum, record_sum))
